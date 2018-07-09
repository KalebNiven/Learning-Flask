
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Testaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = create_engine
DBSession = Sessionmaker(bind = engine)

session = DBSession()

#newEntry = ClassName(property = "value")
myFirstRestaurant = Restaurant(name = "Pizza Palace")

#session.add(newEntry)
session.add(myFirstRestaurant)

session.commit()

session.query(Restaurant.all())

cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozerella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
