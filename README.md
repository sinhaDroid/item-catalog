# Item Catalog Project

This repository implements the third project (Item Catalog App) in the Udacity Full Stack Nanodegree program.

A user of this project can add, edit, and delete items belonging to a particular category.  

Authentication is handled by Google OAuth.  User can only edit or delete items they created.

# Prerequisites
Requires Python, pip, and git.

# How to Install
To download and install this program, you will need git installed.

At the command line, enter:
```
git clone git@github.com:sinhaDroid/item-catalog.git
```

Change directory to item-catalog.

# How to Use Google Authentication Services
You need to supply a client_secret.json file. You can create an application to use
Google's OAuth service at https://console.developers.google.com. 

After creating and downloading your client_secret.json file, move it to the 
item-catalog directory so it is accessible to the Item Catalog application.

# How to Initialize Database and Load Initial Categories
To initialize the SQLite database (create empty tables) enter
```
python db/database_setup.py
```

To load the initial sporting good categories enter
```
python db/database_load.py
```

# Starting Application
To start the application enter:
```
python __init__.py
```

Then bring up a browser and point it to localhost:5000.

# Adding, Editing, and Deleting Items
Adding, editing, and deleting items requires the user to log in. 
Logins are handled by Google OAuth.  

Users can see all items but can only edit and delete their own items.
This has been tested with two users.
