from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def start_page():
    # restaurant = session.query(Restaurant).filter_by(id=1)
    # render_template('all_menus.html', restaurant=restaurant)
    return "please navigate to '/restaurants/{restaurant_id}' to see that restaurants menu"

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Menu Item has been edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCITON BELOW TO SEE THE VARIABLES YOU
        #SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('edit_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)



# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("menu item has been deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('delete_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, item=itemToDelete)
    # return "page to delete a new menu item."


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
