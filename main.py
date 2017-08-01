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


fact_list = []
variables = {'fact_list': fact_list}

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


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
        if saved_fact not in fact_list:
            fact_list.append(saved_fact)
        print saved_fact
        print variables
        self.response.write(template.render())

class ToDoListHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('/templates/to_do_list.html')
		print variables
		self.response.write(template.render(variables))
	def post(self):
		template = jinja_environment.get_template('/templates/to_do_list.html')
		deleted_fact = self.request.get("deleted_fact")
		fact_list.remove(deleted_fact)
		print deleted_fact
		# variables["fact_list"] = fact_list
		print variables
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
    ('/todolist', ToDoListHandler)
], debug=True)
