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
<<<<<<< HEAD
=======
# from bs4 import BeautifulSoup

fact_list = []
>>>>>>> ba8a18f44ca3ce2e75c010cdb0514cde3c296976

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

<<<<<<< HEAD
class ToDoList(ndb.Model):
	pass

		

=======

# with open("/templates/spotify.html") as fp:
#     soup = BeautifulSoup(fp)

# soup = BeautifulSoup("<html>data</html>")

class ToDoList(ndb.Model):
	pass

>>>>>>> ba8a18f44ca3ce2e75c010cdb0514cde3c296976
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class DecadeHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('/templates/spotify.html')
		self.response.write(template.render())
		self.response.write('Decades')
	def post(self):
<<<<<<< HEAD
		template = jinja_environment.get_template('/templates/to_do_list.html')
		saved_fact = self.request.get("saved_fact")
		print saved_fact
		variables = {"saved_fact":saved_fact}
=======
		template = jinja_environment.get_template('/templates/spotify.html')
		saved_fact = self.request.get("saved_fact")
		fact_list.append(saved_fact)
		print saved_fact
		variables = {"fact_list":fact_list}
>>>>>>> ba8a18f44ca3ce2e75c010cdb0514cde3c296976
		print variables
		self.response.write(template.render(variables))

class ToDoListHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('/templates/to_do_list.html')
<<<<<<< HEAD
		self.response.write(template.render())
=======
		self.response.write(template.render(variables))
>>>>>>> ba8a18f44ca3ce2e75c010cdb0514cde3c296976
		self.response.write('To Do List')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/decade', DecadeHandler),
    ('/todolist', ToDoListHandler)
], debug=True)
