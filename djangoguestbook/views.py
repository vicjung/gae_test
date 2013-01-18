#!/usr/bin/env python
#
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from google.appengine.api import users

from models import Post
from forms import GuestbookForm

def index(request):
  query = Post.gql('ORDER BY date DESC')
  form = GuestbookForm()
  return render_to_response('index.html',
                            {'posts': query.fetch(20),
                             'form': form
                            }
                           )

def sign(request):
  form = GuestbookForm(request.POST)
  if form.is_valid():
    post = Post(message=form.clean_data['message'])
    if users.GetCurrentUser():
      post.author = users.GetCurrentUser()
  
    post.put()

  return HttpResponseRedirect('/')
