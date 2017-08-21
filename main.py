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
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users

login_dict = {}
bookmarks_dict = {"bookmarks": [
]}
# user_bookmarks_dict = {"bookmarks": [
# ]}

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


def UserLogin(login_dict={}, user_bookmarks_dict=bookmarks_dict):
    user = users.get_current_user()
    global user
    if user:
        nickname = user.nickname()
        global nickname
        logout_url = users.create_logout_url('/')
        greeting = '<p id="username" >Welcome, {}! <a id="login_link" href="{}">Sign Out</a></p>'.format(nickname, logout_url)
        user_list = UserProperties.query(UserProperties.username == nickname).fetch()
        print user_list
        if user_list == []:
            user_bookmarks_dict_json = json.dumps(user_bookmarks_dict)
            new_user = UserProperties(username=nickname, bookmarks=user_bookmarks_dict_json)
            new_user.put()
    else:
        login_url = users.create_login_url('/')
        greeting = '<a id="login_link" href="{}">Log in to save your Bookmarks!</a>.'.format(login_url)
        # bookmarks_dict["bookmarks"] = []
    login_dict['header'] = greeting
    return login_dict


def AddUserBookmark(self):
    if user:
        LoadUserBookmarks()
        AddToBookmarkDict(self, user_bookmarks_dict)
        DumpUserBookmarks()
    else:
        AddToBookmarkDict(self)


def DumpUserBookmarks():
    user_bookmarks_dict_json = json.dumps(user_bookmarks_dict)
    current_user.bookmarks = user_bookmarks_dict_json
    current_user.put()


def LoadUserBookmarks():
    user_results = UserProperties.query(UserProperties.username == nickname).fetch(limit=1)
    for current_user in user_results:
        global current_user
        user_bookmarks_dict_json = current_user.bookmarks
    user_bookmarks_dict = json.loads(user_bookmarks_dict_json)
    global user_bookmarks_dict
    return user_bookmarks_dict


def AddToBookmarkDict(self, bookmarks_dict=bookmarks_dict):
    # get caption and fact url from fixed html input values
    saved_fact = self.request.get("saved_fact")
    new_caption = self.request.get('caption')
    logging.info(saved_fact)
    logging.info(new_caption)
    # check if item being added is already in bookmarks
    # if no bookmarks exists = False
    if len(bookmarks_dict['bookmarks']) == 0:
        logging.info(new_caption)
        exists = False
    else:
        logging.info(new_caption)
        # check to see if item is already in list of of boomarks using item caption
        for bookmark in bookmarks_dict['bookmarks']:
            if bookmark['caption'] == new_caption:
                exists = True
            else:
                exists = False
    logging.info(exists)
    # if exists == False, function ends wihout changing bookmarks list
    # if exists == True then item type is determined
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
            # Dictionary with caption, item url, and type is added to bookmarks list
            bookmarks_dict['bookmarks'].append({'caption': new_caption, 'fact_url': saved_fact, 'type': fact_type})
    return bookmarks_dict


def DeleteUserBookmark(self, template):
    bookmark_page_rendered_dict = {"login_dict": login_dict, "bookmarks_dict": bookmarks_dict}
    if user:
        LoadUserBookmarks()
        DeleteFromBookmarkDict(self, user_bookmarks_dict)
        DumpUserBookmarks()
        bookmark_page_rendered_dict["bookmarks_dict"] = user_bookmarks_dict
        self.response.write(template.render(bookmark_page_rendered_dict))
    else:
        DeleteFromBookmarkDict(self)
        self.response.write(template.render(bookmark_page_rendered_dict))


def DeleteFromBookmarkDict(self, bookmarks_dict=bookmarks_dict):
    deleted_fact = self.request.get("deleted_fact")
    for bookmark in bookmarks_dict['bookmarks']:
        if deleted_fact == bookmark['caption']:
            bookmarks_dict['bookmarks'].remove(bookmark)
            break
    return bookmarks_dict


class BookmarkHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/bookmarks.html')
        UserLogin(login_dict)
        bookmark_page_rendered_dict = {"login_dict": login_dict, "bookmarks_dict": bookmarks_dict}
        if user:
            LoadUserBookmarks()
            DumpUserBookmarks()
            bookmark_page_rendered_dict["bookmarks_dict"] = user_bookmarks_dict
            self.response.write(template.render(bookmark_page_rendered_dict))
        else:
            self.response.write(template.render(bookmark_page_rendered_dict))

    def post(self):
        template = jinja_environment.get_template('/templates/bookmarks.html')
        UserLogin(login_dict)
        DeleteUserBookmark(self, template)


class FeedbackHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/input_feedback.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('/templates/output_feedback.html')
        # retrieving user responses from html form
        name = self.request.get('name')
        email = self.request.get('email')
        rating = int(self.request.get('rating'))
        comment = self.request.get('comment')
        # putting user responses into datastore
        new_feedback = Feedback(name=name, email=email, rating=rating, comment=comment)
        new_feedback.put()
        self.response.write(template.render())


class Feedback(ndb.Model):
    # Feedback to send to datastore
    email = ndb.StringProperty()
    name = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    comment = ndb.StringProperty()


class UserProperties(ndb.Model):
    username = ndb.StringProperty()
    bookmarks = ndb.StringProperty()


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
