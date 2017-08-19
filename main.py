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
import pickle
import json
import logging
import urllib2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users

login_dict = {}
user = ''
# user_key = ''
# nickname = ''
variables = {"bookmarks": [
]}
i = 1

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


def AddUserBookmark(self):
    if user:
        current_user = UserBookmarks.get_by_id(user_key)
        variables["bookmarks"] = current_user.user_bookmarks
        for bookmark in variables["bookmarks"]:
            print bookmark["caption"]
        AddBookmark(self)
        current_user.put()
        print i
        i += 1
    else:
        AddBookmark(self)


def AddBookmark(self):
    saved_fact = self.request.get("saved_fact")
    new_caption = self.request.get('caption')
    logging.info(saved_fact)
    logging.info(new_caption)
    if len(variables['bookmarks']) == 0:
        logging.info(new_caption)
        exists = False
    else:
        logging.info(new_caption)
        for bookmark in variables['bookmarks']:
            if bookmark['caption'] == new_caption:
                exists = True
            else:
                exists = False
    logging.info(exists)
    if not exists:
        fact_type = None
        if 'spotify' in saved_fact:
            fact_type = 'spotify'
        elif 'youtube' in saved_fact:
            fact_type = 'youtube'
            logging.info(fact_type)
        elif 'jpg' in saved_fact or 'png' in saved_fact:
            logging.info(fact_type)
            fact_type = 'picture'
        if fact_type is not None:
            variables['bookmarks'].append({'caption': new_caption, 'fact_url': saved_fact, 'type': fact_type})
    return variables


class UserBookmarks(ndb.Model):
    username = ndb.StringProperty()
    user_bookmarks = ndb.PickleProperty()


def UserLogin(login_dict={}):
    user = users.get_current_user()
    nickname = ''
    user_key = ''
    if user:
        print user
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        greeting = '<p id="username" >Welcome, {}! <a id="login_link" href="{}">Sign Out</a></p>'.format(nickname, logout_url)
        user_list = UserBookmarks.query().fetch()
        print user_list
        for user_kind in user_list:
            for user_items in user_kind:
                if nickname not in user_items:
                    new_user = UserBookmarks(username=nickname, user_bookmarks=variables["bookmarks"])
                    user_key = new_user.put()
    else:
        login_url = users.create_login_url('/')
        greeting = '<a id="login_link" href="{}">Log in to save your Bookmarks!</a>.'.format(login_url)
        variables["bookmarks"] = []
    login_dict['header'] = greeting
    return login_dict, user, nickname, user_key


class Feedback(ndb.Model):
    # Feedback to send to datastore
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
        new_feedback = Feedback(name=name, email=email, rating=rating, comment=comment)
        new_feedback.put()
        self.response.write(template.render())


class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/homepage.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))


# 1990s Handlers (121-179)
class NintiesPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/1990s.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))


class NintiesEntertainmentHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/90sEntertainment.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/90sEntertainment.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class NintiesScientificDiscHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/90sScientificDisc.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/90sScientificDisc.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class NintiesFunFactsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/90sFunFacts.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/90sFunFacts.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class NintiesSpecialEventsNewsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/90sSpecialEventsNews.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/90sSpecialEventsNews.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))
# End of 90s Handlers


# 2000s Handlers (182-231)
class TwoThousandsPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/2000s.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))


class TwoThousandsEntertainmentHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/00sEntertainment.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/00sEntertainment.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class TwoThousandsScientificDiscHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/00sScientificDiscoveries.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/00sScientificDiscoveries.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class TwoThousandsFunFactsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/00sFunfacts.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/00sFunfacts.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class TwoThousandsSpecialEventsNewsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/00sSpecialEventsNews.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/00sSpecialEventsNews.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))
# End of 2000s Handlers


# 1980s Handlers (234-284)
class EightiesPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/1980s.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))


class EightiesEntertainmentHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/80sEntertainment.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))
        # AddUserBookmark(self)

    def post(self):
        template = jinja_environment.get_template('/templates/80sEntertainment.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class EightiesScientificDiscHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/80sScientificDisc.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/80sScientificDisc.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class EightiesFunFactsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/80sFunFacts.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/80sFunFacts.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class EightiesSpecialEventsNewsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/80sSpecialEventsNews.html')
        UserLogin(login_dict)
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/80sSpecialEventsNews.html')
        UserLogin(login_dict)
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))
# End of 80s Handlers


class DecadeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/spotify.html')
        self.response.write(template.render())
        self.response.write('Decades')

    def post(self):
        template = jinja_environment.get_template('/templates/spotify.html')
        self.response.write(template.render())


class BookmarkHandler(webapp2.RequestHandler):
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
    ('/', HomePageHandler),
    # 1990s Handlers
    ('/1990', NintiesPageHandler),
    ('/1990/Entertainment', NintiesEntertainmentHandler),
    ('/1990/ScientificDisc', NintiesScientificDiscHandler),
    ('/1990/FunFacts', NintiesFunFactsHandler),
    ('/1990/SpecialEventsNews', NintiesSpecialEventsNewsHandler),
    # 2000s Handlers
    ('/2000', TwoThousandsPageHandler),
    ('/2000/Entertainment', TwoThousandsEntertainmentHandler),
    ('/2000/Funfacts', TwoThousandsFunFactsHandler),
    ('/2000/ScientificDisc', TwoThousandsScientificDiscHandler),
    ('/2000/SpecialEventsNews', TwoThousandsSpecialEventsNewsHandler),
    # 1980s Hanlders
    ('/1980', EightiesPageHandler),
    ('/1980/Entertainment', EightiesEntertainmentHandler),
    ('/1980/FunFacts', EightiesFunFactsHandler),
    ('/1980/ScientificDisc', EightiesScientificDiscHandler),
    ('/1980/SpecialEventsNews', EightiesSpecialEventsNewsHandler),
    # Other Handlers
    ('/decade', DecadeHandler),
    ('/bookmarks', BookmarkHandler),
    ('/feedback', FeedbackHandler)
], debug=True)
