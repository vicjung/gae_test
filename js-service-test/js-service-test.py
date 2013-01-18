import webapp2
import json
import datetime
import time
from google.appengine.ext import db
from google.appengine.api import users
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import OAuth2WebServerFlow
from oauth2client.appengine import OAuth2Decorator

decorator = OAuth2Decorator(
  client_id='your_client_id',
  client_secret='your_client_secret',
  scope='https://www.googleapis.com/auth/calendar')

service = build('calendar', 'v3')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, ')

class GAuthPage(webapp2.RequestHandler):
	@decorator.oauth_required
	def get(self):
		# Get the authorized Http object created by the decorator.
		http = decorator.http()
		# Call the service using the authorized Http object.
		request = service.events().list(calendarId='primary')
		response = request.execute(http=http)	
			
		# auth_uri = "http:// /auth_return"
		# flow = flow_from_clientsecrets('path_to_directory/client_secrets.json',
  #                              scope='https://www.googleapis.com/auth/calendar',
  #                              redirect_uri='http://example.com/auth_return')
		# flow = OAuth2WebServerFlow(client_id='your_client_id',
		#                            client_secret='your_client_secret',
		#                            scope='https://www.googleapis.com/auth/calendar',
		#                            redirect_uri='http://example.com/auth_return')		


class GAuthReturnPage(webapp2.RequestHandler):
	def get(self):
		# http://example.com/auth_return/?code=kACAH-1Ng1MImB...AA7acjdY9pTD9M
		# http://example.com/auth_return/?error=access_denied



class TestPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Test, ')

class ArgTestPage(webapp2.RequestHandler):
	def post(self):
		name = self.request.get("name")

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Test, ')


class JsonPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']= 'application/json'
        self.response.out.write(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))

# SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)
# def to_dict(model):
#     output = {}

#     for key, prop in model.properties().iteritems():
#         value = getattr(model, key)

#         if value is None or isinstance(value, SIMPLE_TYPES):
#             output[key] = value
#         elif isinstance(value, datetime.date):
#             # Convert date/datetime to ms-since-epoch ("new Date()").
#             ms = time.mktime(value.utctimetuple())
#             ms += getattr(value, 'microseconds', 0) / 1000
#             output[key] = int(ms)
#         elif isinstance(value, db.GeoPt):
#             output[key] = {'lat': value.lat, 'lon': value.lon}
#         elif isinstance(value, db.Model):
#             output[key] = to_dict(value)
#         else:
#             raise ValueError('cannot encode ' + repr(prop))

#     return output

class Employee(db.Model):
	name = db.StringProperty(required=True)
	role = db.StringProperty(required=True,
	                       choices=set(["executive", "manager", "producer"]))
	hire_date = db.DateProperty()
	new_hire_training_completed = db.BooleanProperty(indexed=False)
	email = db.StringProperty()      
	def to_dict(self):
		return dict([(p, unicode(getattr(self, p))) for p in self.properties()])


class SaveEmployee(webapp2.RequestHandler):
	def get(self):
		e = Employee(name="John",
		             role="manager",
		             email="test")#users.get_current_user().email())
		e.hire_date = datetime.datetime.now().date()
		e.put()

		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Save Employee')

class LoadEmployee(webapp2.RequestHandler):
	def get(self):
		training_registration_list = ["Alfred.Smith@example.com",
		                              "jharrison@example.com",
		                              "budnelson@example.com"]
		employees_trained = db.GqlQuery("SELECT * FROM Employee ")
        
		if (employees_trained.count() > 0):
			self.response.headers['Content-Type']= 'application/json'
		 	self.response.out.write(json.dumps([p.to_dict() for p in employees_trained]))			
		else:
			self.response.headers['Content-Type']= 'application/json'
			self.response.out.write('')
		# self.response.out.write(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))
		# for e in employees_trained:
			# e.new_hire_training_completed = True
			# db.put(e)

		



app = webapp2.WSGIApplication([('/', MainPage), ('/test', TestPage), ('/json', JsonPage)
									, ('/load', LoadEmployee), ('/save', SaveEmployee)
									, (decorator.callback_path, decorator.callback_handler())
									]
								, debug=True)