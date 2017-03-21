import random
import string
import httplib2
import json

from flask import (Flask, render_template, request)
from flask import (redirect, make_response, url_for, flash, jsonify)
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from db.database_setup import Category, Item, User
from db.database_access import db_create_session, db_categories, db_category
from db.database_access import db_items_in_category, db_item, db_save_item
from db.database_access import db_delete_item, db_latest_items, db_update_user

from util import item_from_request_post, json_response
from login import (upgrade_to_credentials, token_info, is_already_logged_in)
from login import (is_logged_in_as_owner, get_user_info, update_login_session)

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
session = db_create_session()


# Routes for home page
@app.route('/')
@app.route('/index/')
@app.route('/catalog/')
def catalog():
    categories = db_categories(session)
    latest_items = db_latest_items(session)

    return render_template(
        'catalog.html', categories=categories, latest_items=latest_items,
        is_logged_in=is_already_logged_in(login_session))


@app.route('/catalog/json/')
def catalog_as_json():
    categories = db_categories(session)
    categories = [c.serialize for c in categories]

    latest_items = db_latest_items(session)
    latest_items = [i.serialize for i in latest_items]

    return json.dumps(
        {'categories': categories, 'latest_items': latest_items})


# Routes for items in specified category
@app.route('/catalog/category/<int:category_id>/')
def show_items_in_category(category_id):
    category = db_category(session, category_id)
    items = db_items_in_category(session, category_id)

    return render_template(
        'category.html', category=category, items=items,
        is_logged_in=is_already_logged_in(login_session))


@app.route('/catalog/category/<int:category_id>/json/')
def items_in_category_as_json(category_id):
    category = db_category(session, category_id)
    items = db_items_in_category(session, category_id)
    items = [i.serialize for i in items]

    return flask.jsonify({'category': category.serialize, 'items': items})


# Routes for specified category and item
@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/')
def show_item(category_id, item_id):
    category = db_category(session, category_id)
    item = db_item(session, item_id)

    return render_template(
        'item.html', category=category, item=item,
        is_logged_in=is_already_logged_in(login_session),
        is_logged_in_owner=is_logged_in_as_owner(login_session, item.user_id))


@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/json/')
def item_as_json(category_id, item_id):
    item = db_item(session, item_id)
    return json.dumps(item.serialize)


# Routes for add item to category
@app.route(
    '/catalog/category/<int:category_id>/item/add/', methods=['GET', 'POST'])
def add_item(category_id):
    if request.method == 'POST':
        item = item_from_request_post(request)
        if item and is_already_logged_in(login_session):
            item.category_id = category_id
            item.user_id = login_session['id']
            db_save_item(session, item)
            return redirect(url_for(
                'show_items_in_category', category_id=category_id))
        else:
            return redirect(url_for('add_item', category_id=category_id))
    else:
        if is_already_logged_in(login_session):
            category = db_category(session, category_id)
            return render_template('additem.html', category=category)
        else:
            flash("To add an item, you must first log in.")
            return redirect(url_for('showLogin'))


# Route to edit item in category
@app.route(
    '/catalog/category/<int:category_id>/item/<int:item_id>/edit/', methods=[
        'GET', 'POST'
        ]
    )
def edit_item(category_id, item_id):
    if request.method == 'POST':
        item_from_database = db_item(session, item_id)
        item_from_form = item_from_request_post(request)
        if item_from_form and is_logged_in_as_owner(
                login_session, item_from_database.user_id):
            item_from_database.name = item_from_form.name
            item_from_database.description = item_from_form.description

            session.commit()
            return redirect(url_for(
                'show_items_in_category', category_id=category_id))
        else:
            # problem with item, try again
            return redirect(url_for(
                'edit_item', category_id=category_id, item_id=item_id))
    else:
        category = db_category(session, category_id)
        item = db_item(session, item_id)
        if is_logged_in_as_owner(login_session, item):
            url = '/catalog/category/' + str(item.category_id)
            cancel_url = url + '/item/' + str(item_id)
            log_in = is_already_logged_in(login_session)
            return render_template(
                'edititem.html', category=category, item=item,
                cancel_url=cancel_url, is_logged_in=log_in)
        else:
            msg = "To edit an item, you must first be"
            msgs = msg + " logged in as the item's owner."
            flash(msgs)
            return redirect(url_for('showLogin'))


# Route to delete item in category
@app.route(
    '/catalog/category/<int:category_id>/item/<int:item_id>/delete/', methods=[
        'GET', 'POST'
        ]
    )
def delete_item(category_id, item_id):
    if request.method == 'POST':
        item = db_item(session, item_id)
        if item and is_logged_in_as_owner(login_session, item.user_id):
            db_delete_item(session, item)
            return redirect(url_for('show_items_in_category',
                                    category_id=category_id))
        else:
            # problem with item, try again
            return redirect(url_for('delete_item', category_id=category_id,
                                    item_id=item_id))
    else:
        category = db_category(session, category_id)
        item = db_item(session, item_id)
        if is_logged_in_as_owner(login_session, item):
            log_in = is_already_logged_in(login_session)
            return render_template('deleteitem.html', category=category,
                                   item=item, is_logged_in=log_in)
        else:
            msg = "To delete an item, you must first be"
            msgs = msg + " logged as the item's owner."
            flash(msgs)
            return redirect(url_for('showLogin'))


# login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        return json_response('Invalid state parameter', 400)

    authorization_code = request.data

    try:
        credentials = upgrade_to_credentials(authorization_code)
    except FlowExchangeError:
        return json_response('Failed to upgrade the authorization code.', 401)

    access_token_info = token_info(credentials.access_token)
    if access_token_info.get('error') is not None:
        error = access_token_info.get('error')
        return json_response(error, 500)

    gplus_id = credentials.id_token['sub']
    if access_token_info['user_id'] != gplus_id:
        return json_response(
            "Token's user ID doesn't match given user ID.", 401)

    if access_token_info['issued_to'] != CLIENT_ID:
        return json_response("Token's client ID does not match this app.", 401)

    if is_already_logged_in(login_session):
        return json_response("Current user is already connected.", 401)

    user_info = get_user_info(credentials.access_token)
    update_login_session(login_session, credentials, gplus_id, user_info)
    db_update_user(session, login_session)

    flash("You are now logged in as %s" % login_session['username'])
    return '<html></html>'

# DISCONNECT - Revoke a current user's token and reset their login_session.


# code from github for gdisconnect (and gconnect)
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['id']
        del login_session['picture']

        flash("You are now logged out.")
        return redirect(url_for('catalog'))
    else:
        # For whatever reason, the given token was invalid.
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['id']
        del login_session['picture']

        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'

        return response


@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    print 'state = ' + state
    return render_template('login.html', STATE=state)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, debug=True)
