# -*- coding: utf-8 -*-
import webapp2
import json
import datetime
import time
from google.appengine.ext import db
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		# output = 'test'
		output = '''
				<html>
				<head><title>%s</title></head>
				<body>
				<h1>%s</h1><p>%s</p>
				</body>
				</html>
				''' % (
				'연습',
				'h1 화면',
				'p 화면'
				)

		self.response.out.write(output)
		self.response.out.write('Hello, ')

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

class TrainingQuestion(db.Model):
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
									, ('/load', LoadEmployee), ('/save', SaveEmployee)]
								, debug=True)