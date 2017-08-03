#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
import webapp2
import json
import logging
import urllib2
import jinja2
import os
from google.appengine.ext import ndb

# exists = False
variables = {'bookmarks':[

]}

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Feedback(ndb.Model):
    # Feedback to send to datastoe
    email = ndb.StringProperty()
    name = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    comment = ndb.StringProperty()

class FeedbackHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/input_feedback.html')
        self.response.write(template.render())
    def post(self):
        template = jinja_environment.get_template('/templates/output_feedback.html')
        name = self.request.get('name')
        email = self.request.get('email')
        rating = int(self.request.get('rating'))
        comment = self.request.get('comment')
        new_feedback = Feedback(name = name, email = email, rating = rating, comment = comment)
        new_feedback.put()
        self.response.write(template.render())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class HomePageHandler(webapp2.RequestHandler):
    def get(self):
		template = jinja_environment.get_template('/templates/homepage.html')
		self.response.write(template.render())
    def post (self):
        template = jinja_environment.get_template('/templates/1990s.html')
        self.response.write(template.render())

# this section is just for the 1990s Handlers
class NintiesPageHandler(webapp2.RequestHandler):
    def get(self):
		template = jinja_environment.get_template('/templates/1990s.html')
		self.response.write(template.render())
    def post (self):
        template = jinja_environment.get_template('/templates/90sEntertainment.html')
        self.response.write(template.render())

class NintiesEntertainmentHandler(webapp2.RequestHandler):
    def get(self):
		template = jinja_environment.get_template('/templates/90sEntertainment.html')
		self.response.write(template.render())

class NintiesScientificDiscHandler(webapp2.RequestHandler):
    def get(self):
		template = jinja_environment.get_template('/templates/90sScientificDisc.html')
		self.response.write(template.render())

class NintiesFunFactsHandler(webapp2.RequestHandler):
    def get(self):
		template = jinja_environment.get_template('/templates/90sFunFacts.html')
		self.response.write(template.render())


class NintiesSpecialEventsNewsHandler(webapp2.RequestHandler):
    def get(self):
		template = jinja_environment.get_template('/templates/90sSpecialEventsNews.html')
		self.response.write(template.render())
# End of 90s Handlers

class DecadeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/spotify.html')
        self.response.write(template.render())
        self.response.write('Decades')
    def post(self):
        template = jinja_environment.get_template('/templates/spotify.html')
        saved_fact = self.request.get("saved_fact")
        new_caption = self.request.get('caption')
        logging.info(saved_fact)
        logging.info(new_caption)
        if len(variables['bookmarks']) == 0:
        	exists = False
        else:
            for bookmark in variables['bookmarks']:
                if bookmark['caption'] == new_caption:
                    exists = True
                else:
                    exists = False
                    break
        # else:
        #     exists = False
        if not exists:
            if 'spotify' in saved_fact:
                fact_type = 'spotify'
            elif 'youtube' in saved_fact:
                fact_type = 'youtube'
            elif 'jpg' in saved_fact or 'png' in saved_fact:
                fact_type = 'picture'
            variables['bookmarks'].append({'caption':new_caption, 'fact_url':saved_fact, 'type':fact_type})
        logging.info(variables)
        self.response.write(template.render())

class ToDoListHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('/templates/to_do_list.html')
		logging.info(variables)
		self.response.write(template.render(variables))
	def post(self):
		template = jinja_environment.get_template('/templates/to_do_list.html')
		deleted_fact = self.request.get("deleted_fact")
		# logging.info(deleted_fact) 
		for bookmark in variables['bookmarks']:
			if deleted_fact == bookmark['caption']:
				variables['bookmarks'].remove(bookmark)
				break
		logging.info(variables)
		self.response.write(template.render(variables))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/homepage', HomePageHandler),
    ('/1990s', NintiesPageHandler),
    ('/90sEntertainment', NintiesEntertainmentHandler),
    ('/90sScientificDisc', NintiesScientificDiscHandler),
    ('/90sFunFacts', NintiesFunFactsHandler),
    ('/90sSpecialEventsNews', NintiesSpecialEventsNewsHandler),
    ('/decade', DecadeHandler),
    ('/todolist', ToDoListHandler),
    ('/feedback', FeedbackHandler)
], debug=True)
