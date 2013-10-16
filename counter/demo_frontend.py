#!/usr/bin/env python
#
# Copyright 2011 Google Inc. All Rights Reserved.
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
# vim: set ts=4 sw=4 et tw=79:
"""The sample frontend that was shown in the backends talk."""

from google.appengine.api import backends
from google.appengine.api import urlfetch

url = '%s/backend/counter/inc' % (
        backends.get_url('counter'))

count = urlfetch.fetch(url, method='GET',
                       payload='name=visitor&delta=1').content

print 'Content-Type: text/plain'
print ''
print 'Welcome visitor %s' % count
