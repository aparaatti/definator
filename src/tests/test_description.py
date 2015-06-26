__author__ = 'aparaatti'

# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import unittest
import data.description
import data.term


class DescriptionTestCases(unittest.TestCase):
    """ Tähän voisi tulla str-template, johon sitten tykitetään eri tekstejä
    eri paikkoihin ja katsotaan meneekö round robin läpi... """

    """
    unittest methods:
     setUp()
       the test runner will run that method prior to each test.
     tearDown() method is invoked after each test.

     assertEqual() to check for an expected result
     assertTrue() to verify a condition
     assertRaises() to verify that right exception is raised

    """

    @classmethod
    def setUpClass(cls):
        return

    def setUp(self):
        self.description = data.description.Description()
        self.description.content_text = """A cat is a cat animal. It likes to purr.

Other things a cat could like to do are:

##LIST##
run
sit
eat
##END##

There might be also other thing, a cat enjoys to do. Maybe
it could also be like this:

##ASCII##
^--^
|oo|
( .)
  ^
##END##

Or is it a cow?"""
        print(self.description.content_text)

    def test_confirm_conversion(self):
        html = self.description.content_html
        print(html)
        self.maxDiff = None
        self.assertEqual(html,
                         """<p>A cat is a cat animal. It likes to purr.</p>
<p>Other things a cat could like to do are:</p>
<ul>
    <li>run</li>
    <li>sit</li>
    <li>eat</li>
</ul>
<p>There might be also other thing, a cat enjoys to do. Maybe
it could also be like this:</p>
<pre>
^--^
|oo|
( .)
  ^
</pre>
<p>Or is it a cow?</p>
""")

    @classmethod
    def tearDownClass(cls):
        pass

