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
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
	return EMAIL_RE.match(email)

def build_page(orig_username, error_username, error_password, error_passwordverify, orig_email, error_email):
	top = ("<head>"
		"<title>Sign Up To Learn More</title>"
		"<style type='text/css'>"
			".error {color: red}"
		"</style>"
		"</head>")

	header = "<h2>Signup</h2>"

	table1 = ("<table>"
		"<tr>"
			"<td>Username</td>"
			"<td><input type='text' name='username' value='" + orig_username + "'></input></td>"
			"<td class='error'>" + error_username + "</td>"
		"</tr>"

		"<tr>"
			"<td>Password</td>"
			"<td><input type='password' name='password'></input></td>"
			"<td class='error'>" + error_password + "</td>"
		"</tr>"

		"<tr>"
			"<td>Verify Password</td>"
			"<td><input type='password' name='password_verify'></input></td>"
			"<td class='error'>" + error_passwordverify + "</td>"
		"</tr>"

		"<tr>"
			"<td>Email (optional)</td>"
			"<td><input type='text' name='email' value='" + orig_email + "'></input></td>"
			"<td class='error'>" + error_email + "</td>"
		"</tr>"
	"</table>")

	submit_button = "<input type='submit'/>"

	form = top + "<form method='post'>" + table1 + submit_button + "</form>"

	return form

class MainHandler(webapp2.RequestHandler):
	def get(self):
		content = build_page("", "", "", "", "", "")
		self.response.write(content)

	def post(self):
		errorcount = 0
		username = self.request.get("username")
		username = cgi.escape(username, quote=True)
		password = self.request.get("password")
		password_verify = self.request.get("password_verify")
		email = self.request.get("email")
		email = cgi.escape(email, quote=True)
		error_username = ""
		error_password = ""
		error_passwordverify = ""
		error_email = ""

		if not username or not valid_username(username):
			error_username = "Username not valid."
			errorcount += 1
		if not password or not valid_password(password):
			error_password = "That's not a valid password."
			errorcount += 1
		if password != password_verify:
			error_passwordverify = "The passwords don't match."
			errorcount += 1
		if not email or not valid_email(email):
			error_email = "That's not a valid email address."
			errorcount += 1

		if errorcount > 0:
			content = build_page(username, error_username, error_password, error_passwordverify, email, error_email)
			self.response.write(content)
		else:
			self.redirect("/welcome?username=" + username)

class Welcome(webapp2.RequestHandler):
	def get(self):
		username = self.request.get("username")
		header = "<h2>Welcome, " + username + "!" + "</h2>"
		self.response.write(header)

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/welcome', Welcome)
], debug=True)
