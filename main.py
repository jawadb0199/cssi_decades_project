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

login_dict = {"header": None}
bookmarks_dict = {"bookmarks": []}
global bookmarks_dict

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


# DataStore Entity Class to store feedback
class Feedback(ndb.Model):
    # Feedback Properties
    email = ndb.StringProperty()
    name = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    comment = ndb.StringProperty()


# DataStore Entity Class to store user information
class UserProperties(ndb.Model):
    # User Properties
    username = ndb.StringProperty()
    bookmarks = ndb.StringProperty()


# UserLogin function to be run on every page, so user can be logged in on every page
# and be able to add bookmarks and log out
def UserLogin(user_bookmarks_dict=bookmarks_dict):
    user = users.get_current_user()
    # if the user is logged in
    if user:
        nickname = user.nickname()
        global nickname
        # HTML to display username and sign out button
        logout_url = users.create_logout_url("/")
        greeting = "<p id='username' >Welcome, {}! <a id='login_link' href='{}'>Sign Out</a></p>".format(nickname, logout_url)
        # search DataStore for specific user, to see if this is their first login
        user_entity_query = UserProperties.query(UserProperties.username == nickname).fetch()
        # if list of user entities returned by query is empty (current user doesn"t exist), make new user entity
        if user_entity_query == []:
            # bookmarks made before logging in are added to the user"s list of bookmarks
            user_bookmarks_dict_json = json.dumps(user_bookmarks_dict)
            new_user = UserProperties(username=nickname, bookmarks=user_bookmarks_dict_json)
            new_user.put()
    # if no user logged in
    else:
        # HTML to display sign in button
        login_url = users.create_login_url("/")
        greeting = "<a id='login_link' href='{}'>Log in to save your Bookmarks!</a>.".format(login_url)
    # Dictionary to pass to template to display log in/out url
    login_dict = {"header": greeting}
    return login_dict


# Function to add new bookmark to user"s bookmarks property
def AddUserBookmark(self):
    # if user is logged in
    if users.get_current_user():
        # Get user"s bookmarks property, then add bookmark to user_bookmarks_dict, then update user"s bookmark property
        user_bookmarks_dict = LoadUserBookmarks()
        user_bookmarks_dict = AddToBookmarkDict(self, user_bookmarks_dict)
        DumpUserBookmarks(self, user_bookmarks_dict)
    # if user not logged in
    else:
        # add bookmark without Load/Dump user entity json
        AddToBookmarkDict(self)


def DeleteUserBookmark(self, rendered_dict):
    if users.get_current_user():
        user_bookmarks_dict = LoadUserBookmarks()
        user_bookmarks_dict = DeleteFromBookmarkDict(self, user_bookmarks_dict)
        DumpUserBookmarks(self, user_bookmarks_dict)
        rendered_dict["bookmarks_dict"] = user_bookmarks_dict
    else:
        bookmarks_dict = DeleteFromBookmarkDict(self)


# Load user"s bookmarks dictionary
def LoadUserBookmarks():
    # fetch user"s bookmarks via username
    user_entity_query = UserProperties.query(UserProperties.username == nickname).get()
    user_bookmarks_dict_json = user_entity_query.bookmarks
    user_bookmarks_dict = json.loads(user_bookmarks_dict_json)
    return user_bookmarks_dict


# Dump user  user's bookmarks dictionary
def DumpUserBookmarks(self, user_bookmarks_dict=bookmarks_dict):
    user_entity = UserProperties.query(UserProperties.username == nickname).get()
    user_bookmarks_dict_json = json.dumps(user_bookmarks_dict)
    user_entity.bookmarks = user_bookmarks_dict_json
    user_entity.put()


def AddToBookmarkDict(self, bookmarks_dict=bookmarks_dict):
    # get caption and fact url from fixed html input values
    saved_fact = self.request.get("saved_fact")
    new_caption = self.request.get("caption")
    # check if item being added is already in bookmarks
    # if no bookmarks exists = False
    if len(bookmarks_dict["bookmarks"]) == 0:
        exists = False
    else:
        # check to see if item is already in list of of boomarks using item caption
        for bookmark in bookmarks_dict["bookmarks"]:
            if bookmark["caption"] == new_caption:
                exists = True
            else:
                exists = False
    # if exists == False, function ends wihout changing bookmarks list
    # if exists == True then item type is determined
    if not exists:
        fact_type = None
        if "spotify" in saved_fact:
            fact_type = "spotify"
        elif "youtube" in saved_fact:
            fact_type = "youtube"
        elif "jpg" in saved_fact or "png" in saved_fact:
            fact_type = "picture"
        if fact_type is not None:
            # Dictionary with caption, item url, and type is added to bookmarks list
            bookmarks_dict["bookmarks"].append({"caption": new_caption, "fact_url": saved_fact, "type": fact_type})
    return bookmarks_dict


def DeleteFromBookmarkDict(self, bookmarks_dict):
    deleted_fact = self.request.get("deleted_fact")
    for bookmark in bookmarks_dict["bookmarks"]:
        if deleted_fact == bookmark["caption"]:
            bookmarks_dict["bookmarks"].remove(bookmark)
            break


class BookmarkHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/bookmarks.html")
        login_dict = UserLogin()
        rendered_dict = {"login_dict": login_dict, "bookmarks_dict": bookmarks_dict}
        if users.get_current_user():
            user_bookmarks_dict = LoadUserBookmarks()
            rendered_dict["bookmarks_dict"] = user_bookmarks_dict
        self.response.write(template.render(rendered_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/bookmarks.html")
        login_dict = UserLogin()
        rendered_dict = {"login_dict": login_dict, "bookmarks_dict": bookmarks_dict}
        # DeleteUserBookmark(self, rendered_dict)
        if users.get_current_user():
            user_bookmarks_dict = LoadUserBookmarks()
            DeleteFromBookmarkDict(self, user_bookmarks_dict)
            DumpUserBookmarks(self, user_bookmarks_dict)
            rendered_dict["bookmarks_dict"] = user_bookmarks_dict
        else:
            DeleteFromBookmarkDict(self, bookmarks_dict)
        self.response.write(template.render(rendered_dict))


class FeedbackHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/input_feedback.html")
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template("/templates/output_feedback.html")
        # retrieving user responses from html form
        name = self.request.get("name")
        email = self.request.get("email")
        rating = int(self.request.get("rating"))
        comment = self.request.get("comment")
        # putting user responses into datastore
        new_feedback = Feedback(name=name, email=email, rating=rating, comment=comment)
        new_feedback.put()
        self.response.write(template.render())


class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/homepage.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))


# 1990s Handlers (121-179)
class NintiesPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/1990s.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))


class NintiesEntertainmentHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/90sEntertainment.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/90sEntertainment.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class NintiesScientificDiscHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/90sScientificDisc.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/90sScientificDisc.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class NintiesFunFactsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/90sFunFacts.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/90sFunFacts.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class NintiesSpecialEventsNewsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/90sSpecialEventsNews.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/90sSpecialEventsNews.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))
# End of 90s Handlers


# 2000s Handlers (182-231)
class TwoThousandsPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/2000s.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))


class TwoThousandsEntertainmentHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/00sEntertainment.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/00sEntertainment.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class TwoThousandsScientificDiscHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/00sScientificDiscoveries.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/00sScientificDiscoveries.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class TwoThousandsFunFactsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/00sFunfacts.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/00sFunfacts.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class TwoThousandsSpecialEventsNewsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/00sSpecialEventsNews.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/00sSpecialEventsNews.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))
# End of 2000s Handlers


# 1980s Handlers (234-284)
class EightiesPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/1980s.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))


class EightiesEntertainmentHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/80sEntertainment.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))
        # AddUserBookmark(self)

    def post(self):
        template = jinja_environment.get_template("/templates/80sEntertainment.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class EightiesScientificDiscHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/80sScientificDisc.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/80sScientificDisc.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class EightiesFunFactsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/80sFunFacts.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/80sFunFacts.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))


class EightiesSpecialEventsNewsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/80sSpecialEventsNews.html")
        login_dict = UserLogin()
        self.response.write(template.render(login_dict))

    def post(self):
        template = jinja_environment.get_template("/templates/80sSpecialEventsNews.html")
        login_dict = UserLogin()
        AddUserBookmark(self)
        self.response.write(template.render(login_dict))
# End of 80s Handlers


class DecadeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("/templates/spotify.html")
        self.response.write(template.render())
        self.response.write("Decades")

    def post(self):
        template = jinja_environment.get_template("/templates/spotify.html")
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ("/", HomePageHandler),
    # 1990s Handlers
    ("/1990", NintiesPageHandler),
    ("/1990/Entertainment", NintiesEntertainmentHandler),
    ("/1990/ScientificDisc", NintiesScientificDiscHandler),
    ("/1990/FunFacts", NintiesFunFactsHandler),
    ("/1990/SpecialEventsNews", NintiesSpecialEventsNewsHandler),
    # 2000s Handlers
    ("/2000", TwoThousandsPageHandler),
    ("/2000/Entertainment", TwoThousandsEntertainmentHandler),
    ("/2000/Funfacts", TwoThousandsFunFactsHandler),
    ("/2000/ScientificDisc", TwoThousandsScientificDiscHandler),
    ("/2000/SpecialEventsNews", TwoThousandsSpecialEventsNewsHandler),
    # 1980s Hanlders
    ("/1980", EightiesPageHandler),
    ("/1980/Entertainment", EightiesEntertainmentHandler),
    ("/1980/FunFacts", EightiesFunFactsHandler),
    ("/1980/ScientificDisc", EightiesScientificDiscHandler),
    ("/1980/SpecialEventsNews", EightiesSpecialEventsNewsHandler),
    # Other Handlers
    ("/decade", DecadeHandler),
    ("/bookmarks", BookmarkHandler),
    ("/feedback", FeedbackHandler)
], debug=True)
