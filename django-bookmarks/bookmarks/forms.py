import re
from django import newforms as forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegistrationForm(forms.Form):
  username = forms.CharField(label='Username', max_length=30)
  email = forms.EmailField(label='Email')
  password1 = forms.CharField(
    label='Password',
    widget=forms.PasswordInput()
  )
  password2 = forms.CharField(
    label='Password (Again)',
    widget=forms.PasswordInput()
  )

  def clean_username(self):
    username = self.clean_data['username']
    if not re.search(r'^\w+$', username):
      raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
    try:
      User.objects.get(username=username)
    except:
      return username
    raise forms.ValidationError('Username is already taken.')

  def clean_password2(self):
    if 'password1' in self.clean_data:
      password1 = self.clean_data['password1']
      password2 = self.clean_data['password2']
      if password1 == password2:
        return password2
    raise forms.ValidationError('Passwords do not match.')


class BookmarkSaveForm(forms.Form):
  url = forms.URLField(
    label='URL',
    widget=forms.TextInput(attrs={'size': 64})
  )
  title = forms.CharField(
    label='Title',
    widget=forms.TextInput(attrs={'size': 64})
  )
  tags = forms.CharField(
    label='Tags',
    required=False,
    widget=forms.TextInput(attrs={'size': 64})
  )


class SearchForm(forms.Form):
  query = forms.CharField(
    label='Enter a keyword to search for',
    widget=forms.TextInput(attrs={'size': 32})
  )


class FriendInviteForm(forms.Form):
  name = forms.CharField(label=_("Friend's Name"))
  email = forms.EmailField(label=_("Friend's Email"))

