import webapp2
import cgi
import urllib
import logging

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import users


class Greeting(db.Model):
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    avatar = db.BlobProperty()
    avatar1 = db.BlobProperty()
    avatar2 = db.BlobProperty()
    avatar3 = db.BlobProperty()


def guestbook_key(guestbook_name=None):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("<html>"
			  "<head>"
				"<link rel=""stylesheet"" type=""text/css"" href=""css/style.css"" />"
				"<script type=""text/javascript"" src=""lib/jquery-1.9.0.min.js""></script>"
				"<link rel=""stylesheet"" href=""redactor/redactor.css"" />"
				"<script src=""redactor/redactor.js""></script>"

				"<script type=""text/javascript"">"
				"$(document).ready("
					"function() {$('#redactor_content').redactor({ lang: 'ko' });}"
				");"
				"</script>"    
			  "</head>"        	
        	"<body>")
        guestbook_name=self.request.get('guestbook_name')

        greetings = db.GqlQuery('SELECT * '
                                'FROM Greeting '
                                'WHERE ANCESTOR IS :1 '
                                'ORDER BY date DESC LIMIT 10',
                                guestbook_key(guestbook_name))

        for greeting in greetings:
            if greeting.author:
                self.response.out.write(
                    '<b>%s</b> wrote:' % greeting.author)
            else:
                self.response.out.write('An anonymous person wrote:')
            self.response.out.write('<div><img src="img?img_id=%s"></img>' %
                                    greeting.key())
            self.response.out.write('<blockquote>%s</blockquote></div>' %
                                    cgi.escape(greeting.content))

        self.response.out.write("""
              <form action="/sign?%s" enctype="multipart/form-data" method="post">
                <div><textarea name="content" rows="3" cols="60"></textarea></div>
                <div><label>Avatar:</label></div>
                <div><input type="file" name="img"/></div>
                <div><input type="submit" value="Sign Guestbook"></div>
              </form>
              <hr>
              <form>Guestbook name: <input value="%s" name="guestbook_name">
              <input type="submit" value="switch"></form>
            </body>
          </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                        cgi.escape(guestbook_name)))


class InputPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
		      <form action="/sign?%s" enctype="multipart/form-data" method="post">
		        <div><textarea name="content" rows="3" cols="60"></textarea></div>
		        <div><input type="submit" value="Sign Guestbook"></div>
		      </form>
		      <hr>
		      <form>Guestbook name: <input value="%s" name="guestbook_name">
		      <div><label>Avatar:</label></div>
		      <div><input type="file" name="img"/></div>
		      <input type="submit" value="switch"></form>
		    </body>
		  </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
		                cgi.escape(guestbook_name)))


class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        avatar = self.request.get('img')
        logging.info('len => %d' % len(avatar))
        if len(avatar) > 1000000:
        	greeting.avatar = db.Blob(avatar[:1000000])
        	greeting.avatar1 = db.Blob(avatar[1000000:])
        else:
	        greeting.avatar = db.Blob(avatar)
        greeting.put()
        self.redirect('/?' + urllib.urlencode(
            {'guestbook_name': guestbook_name}))

class Image(webapp2.RequestHandler):
    def get(self):
        greeting = db.get(self.request.get('img_id'))
        if greeting.avatar:
            self.response.headers['Content-Type'] = 'image/png'
            avatar = greeting.avatar
            logging.info('type => %s' % type(greeting.avatar1))
            logging.info('len => %d' % len(greeting.avatar1))
            if greeting.avatar1 != None:
            	avatar = avatar + greeting.avatar1
            self.response.out.write(avatar)
        else:
            self.error(404)

class BlobHandler(webapp2.RequestHandler):
  def get(self):
    upload_url = blobstore.create_upload_url('/upload')
    self.response.out.write('<html><body>')
    self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
    self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
        name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    self.redirect('/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    resource = str(urllib.unquote(resource))
    blob_info = blobstore.BlobInfo.get(resource)
    self.send_blob(blob_info)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blob', BlobHandler),
                               ('/upload', UploadHandler),
                               ('/serve/([^/]+)?', ServeHandler),
                               ('/img', Image),
                               ('/sign', Guestbook)],
                              debug=True)
