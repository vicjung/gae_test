import webapp2
import json
import datetime
import time
import logging
from google.appengine.ext import db
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, ')

class JsonPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']= 'application/json'
        self.response.out.write(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))


class Media(db.Model):
	name = db.StringProperty(required=True)
	media_type = db.StringProperty(required=True)		# youtube, ..
	picture_addr = db.StringProperty(required=False)
	media_addr = db.StringProperty(required=True)
	description = db.StringProperty(required=True)
	group_id = db.StringProperty(required=True)
	def to_dict(self):
		return dict([(p, unicode(getattr(self, p))) for p in self.properties()])


class MediaGroup(db.Model):
	group_name = db.StringProperty(required=True)
	group_type = db.StringProperty(required=True)		# player, famous, user
	picture = db.StringProperty(required=True)	
	# hire_date = db.DateProperty()
	# new_hire_training_completed = db.BooleanProperty(indexed=False)
	# email = db.StringProperty()      
	def to_dict(self):
		return dict([(p, unicode(getattr(self, p))) for p in self.properties()])


class UpdateMedia(webapp2.RequestHandler):
	def post(self):
		name = self.request.get("name")
		media_type = self.request.get("media_type") 
		picture_addr = self.request.get("picture_addr")
		media_addr = self.request.get("media_addr")
		description = self.request.get("description")
		group_id = self.request.get("group_id")

		# try:
		#     offset = self.request.get('offset') or None
		#     if offset:
		#         offset = base64.urlsafe_b64decode(str(offset))
		# except TypeError:
		#     offset = None
		

		e = Media(name=name,
		             media_type=media_type,
		             media_addr=media_addr,
		             picture_addr=picture_addr,
		             description=description,
		             group_id=group_id)#users.get_current_user().email())
		e.put()

		self.response.headers['Content-Type']= 'application/json'
		self.response.out.write(json.dumps(['result', 'success']))

class LoadMedia(webapp2.RequestHandler):
	def post(self):
		group_id = self.request.get("group_id")
		media_list = db.GqlQuery("SELECT * FROM Media where group_id = :1", group_id)
        
		if (media_list.count() > 0):
			self.response.headers['Content-Type']= 'application/json'
		 	self.response.out.write(json.dumps([p.to_dict() for p in media_list]))			
		else:
			self.response.headers['Content-Type']= 'application/json'
			self.response.out.write('')
		# self.response.out.write(json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]))
		# for e in employees_trained:
			# e.new_hire_training_completed = True
			# db.put(e)

class UpdateMediaGroup(webapp2.RequestHandler):
	def post(self):
		logging.info('Starting Main handler')

		group_name = self.request.get("group_name")
		group_type = self.request.get("group_type") 
		picture = self.request.get("picture")

		logging.info("group_name => ", group_name)

		e = MediaGroup(group_name=group_name,
		             group_type=group_type,
		             picture=picture)
		e.put()

		self.response.headers['Content-Type']= 'application/json'
		self.response.out.write(json.dumps(['result', 'success']))


class LoadMediaGroup(webapp2.RequestHandler):
	def get(self):
		group_list = db.GqlQuery("SELECT * FROM MediaGroup")
        
		if (group_list.count() > 0):
			self.response.headers['Content-Type']= 'application/json'
		 	self.response.out.write(json.dumps([p.to_dict() for p in group_list]))			
		else:
			self.response.headers['Content-Type']= 'application/json'
			self.response.out.write('')
		



app = webapp2.WSGIApplication([('/', MainPage), ('/json', JsonPage)
									, ('/load_media', LoadMedia), ('/save_media', UpdateMedia)
									, ('/load_mediagroup', LoadMediaGroup), ('/save_mediagroup', UpdateMediaGroup)]
								, debug=True)