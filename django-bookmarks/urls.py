import os.path
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from bookmarks.views import *
from bookmarks.feeds import *

site_media = os.path.join(os.path.dirname(__file__), 'site_media')

feeds = {
  'recent': RecentBookmarks,
  'user': UserBookmarks
}

urlpatterns = patterns('',
  # Browsing
  (r'^$', main_page),
  (r'^user/(\w+)/$', user_page),
  (r'^tag/([^\s]+)/$', tag_page),
  (r'^tag/$', tag_cloud_page),
  (r'^search/$', search_page),

  # Session management
  (r'^login/$', 'django.contrib.auth.views.login'),
  (r'^logout/$', logout_page),
  (r'^register/$', register_page),
  (r'^register/success/$', direct_to_template, 
    {'template': 'registration/register_success.html'}),

  # Media files
  (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
    {'document_root': site_media}),

  # Account management
  (r'^save/$', bookmark_save_page),

  # Ajax
  (r'^ajax/tag/autocomplete/$', ajax_tag_autocomplete),

  # Admin interface
  (r'^admin/', include('django.contrib.admin.urls')),

  # Feeds
  (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
    {'feed_dict': feeds}),

  # Friends
  (r'^friends/(\w+)/$', friends_page),
  (r'^friend/add/$', friend_add),
  (r'^friend/invite/$', friend_invite),
  (r'^friend/accept/(\w+)/$', friend_accept),

  # Localization
  (r'^i18n/', include('django.conf.urls.i18n')),
)

