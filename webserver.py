from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += "<html>"
                output += '<head>'
                output += '<meta http-equiv="refresh" content="0; url=/restaurants" />'
                output += '</head>'
                output += "</html>"
                self.wfile.write(output)
            # Objective 3 Step 2 - Create /restarants/new page
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                #Objective 3 Step 1 = Create a Link to create a new menu MenuItem
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                output += '<html><head> <link rel="stylesheet" type="text/css" href="styles.css"></head><body>'
                output += "<h1>Restaurants</h1>"
                for restaurant in restaurants:
                    output += "<p class='bold'>" + restaurant.name + "</p>"
                    output += '<a href=restaurants/%s/edit> Edit</a>' % restaurant.id
                    output += "</br>"
                    output += "<a href=restaurants/%s/delete> Delete </a>" % restaurant.id
                    output += "</br></br>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurant_path_id = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurant_path_id).one()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>%s</h1>" % myRestaurantQuery.name
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurant_path_id
                output += "<input name = 'changeRestaurantName' type='text' placeholder= '%s' > " % myRestaurantQuery.name
                output += "<input type='submit' value='Submit'>"
                output += "</form></body></html>"
                self.wfile.write(output)

            if self.path.endswith("/delete"):
                restaurant_path_id = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurant_path_id).one()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1> Are you sure you want to delete %s?</h1>" % myRestaurantQuery.name
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/delete' >" % restaurant_path_id
                output += "<input name='deleteRestaurant' type='submit' value='Delete'>"
                output += "</br></br>"
                output += "<h2><a href = '/restaurants' > Go Back </a></h2>" #Go back to previous page
                output += "</form></body></html>"
                self.wfile.write(output)
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:

            #Delete Restaurant from Database
            if self.path.endswith('/delete'):
                    restaurant_path_id = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurant_path_id).one()

                    if myRestaurantQuery != []:
                        session.delete(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            #Edit name of Restaurant
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('changeRestaurantName')
                    restaurant_path_id = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurant_path_id).one()

                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            #Create new Resaurant Object
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s, Open localhost:%s/restaurants in your browser" % (port, port)
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
