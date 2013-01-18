from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
import settings


class Link(models.Model):
  url = models.URLField(unique=True)

  def __str__(self):
    return self.url

  class Admin:
    pass


class Bookmark(models.Model):
  title = models.CharField(maxlength=200)
  user = models.ForeignKey(User)
  link = models.ForeignKey(Link)

  def __str__(self):
    return '%s, %s' % (self.user.username, self.link.url)

  def get_absolute_url(self):
    return self.link.url

  class Admin:
    list_display = ('title', 'link', 'user')
    list_filter = ('user', )
    ordering = ('title', )
    search_fields = ('title', )


class Tag(models.Model):
  name = models.CharField(maxlength=64, unique=True)
  bookmarks = models.ManyToManyField(Bookmark)

  def __str__(self):
    return self.name

  class Admin:
    pass


class Friendship(models.Model):
  from_friend = models.ForeignKey(User, related_name='friend_set')
  to_friend = models.ForeignKey(User, related_name='to_friend_set')
  
  def __str__(self):
    return '%s, %s' % (self.from_friend.username, self.to_friend.username)

  class Admin:
    pass

  class Meta:
    unique_together = (('to_friend', 'from_friend'), )


class Invitation(models.Model):
  name = models.CharField(maxlength=50)
  email = models.EmailField()
  code = models.CharField(maxlength=20)
  sender = models.ForeignKey(User)

  def __str__(self):
    return '%s, %s' % (self.sender.username, self.email)

  class Admin:
    pass

  def send(self):
    subject = 'Invitation to join Django Bookmarks'
    link = 'http://%s/friend/accept/%s/' % (
      settings.SITE_HOST,
      self.code
    )
    template = get_template('invitation_email.txt')
    context = Context({
      'name': self.name,
      'link': link,
      'sender': self.sender.username,
    })
    message = template.render(context)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])

