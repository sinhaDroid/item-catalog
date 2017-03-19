from db.database_setup import Item

def item_from_request_post(request):
	if request.form['name']:
		item = Item()
		item.name = request.form['name']

		if request.form['description']:
			item.description = request.form['description']
			return item

		return None