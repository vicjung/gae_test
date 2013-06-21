import webapp2
import json
import datetime
import time
import logging
from google.appengine.ext import db
from google.appengine.api import users


class Media(db.Model):
	m_name = db.StringProperty(required=True)
	media_type = db.StringProperty(required=False)		# youtube, ..
	def to_dict(self):
		return dict([(p, unicode(getattr(self, p))) for p in self.properties()])


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, ')

class JsonPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']= 'application/json'
        self.response.out.write(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))

class TestPage(webapp2.RequestHandler):
	def get(self):
		t1= Media(key_name="test", m_name="asdf")
		t1.put()

		t2= Media(m_name="noname")
		t2.put()

		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Hello, TestPage')


app = webapp2.WSGIApplication([('/', MainPage), ('/json', JsonPage)
								, ('/test', TestPage)
								], debug=True)