# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from pathlib import Path
import unittest
import shutil
import src.terms_controller
import src.data.term

# To run these tests, run:
# python -m unittest discover -v
# at project root


class TermsControllerBackendTestCases(unittest.TestCase):

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
        Path("test-generated-project/").mkdir()
        tc = src.terms_controller.TermsController()
        terms = tc.load_project(Path("help-project"))
        tc.save_project_as(Path("test-generated-project"))

    def setUp(self):
        self.tc = src.terms_controller.TermsController()
        self.tc.load_project(Path("test-generated-project/"))

    def test_rename_and_save(self):
        term = self.tc.get_term("2. View term")
        self.assertEqual(term.term, "2. View term")
        term.initialize_next_term()
        new_term = term.next_term
        new_term.term = "2. Not at all the same"
        self.assertIsNotNone(new_term.previous_term)
        self.tc.update_term(new_term)
        self.tc.save_project()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("test-generated-project/", ignore_errors=False,
                      onerror=None)
