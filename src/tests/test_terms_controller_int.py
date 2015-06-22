# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from pathlib import Path
import os
import unittest
import shutil
import tempfile
import src.terms_controller
import src.data.term

# To run these tests, run:
# ..as .as

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
        tc.load_project(Path("../help-project"))
        tc.save_project_as(Path("test-generated-project"))

    def setUp(self):
        self.tc = src.terms_controller.TermsController()
        self.tc.load_project(Path("test-generated-project/"))

    def test_rename_and_save(self):
        term = self.tc.get_term("1. Startup")
        self.assertEqual(term.term, "1. Startup")
        term.initialize_next_term()
        new_term = term.next_term
        new_term.term = "1. Not at all the same"
        self.assertIsNotNone(new_term.previous_term)
        self.tc.update_term(new_term)
        self.tc.save_project()
        term = self.tc.get_term("1. Not at all the same")
        self.assertEqual(term.term, "1. Not at all the same")


    """
    B3: 0cd22ed885bf209e99e68acf11004900addc3573
    file in term folder:
        unsaved-changes-kf5.png
        linked-terms-and-files-kf5.png
    """
    def test_save_rename_and_save(self):
        term = self.tc.get_term("2. View term")

        file = tempfile.NamedTemporaryFile(suffix="txt",
                                                     prefix="def-test-file",
                                                     delete=False)
        file.close()

        tmp_path = Path(file.name)
        # index 0 : file handle
        # index 1 : absolute path
        term.link_file(tmp_path)
        term.initialize_next_term()
        new_term = term.next_term
        self.tc.update_term(new_term)
        self.tc.save_project()
        os.remove(file.name)
        self.assertTrue(Path(term.path / term.term / tmp_path.name)
                        .exists())

        term = self.tc.get_term("2. View term")
        self.assertEqual(term.term, "2. View term")
        term.initialize_next_term()
        second_new_term = term.next_term
        second_new_term.term = "new name"
        self.tc.update_term(second_new_term)
        self.tc.save_project()

        term = self.tc.get_term("new name")
        self.assertEqual(term.term, "new name")
        path = Path(term.path / term.term)

        file1 = False
        file2 = False
        file3 = False

        for file in path.iterdir():
            if file.name == 'unsaved-changes-kf5.png':
                file1 = True

            if file.name == 'linked-terms-and-files-kf5.png':
                file2 = True

            if file.name == tmp_path.name:
                file3 = True

        self.assertTrue(file2)
        self.assertTrue(file3)
        self.assertTrue(file1)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("test-generated-project/", ignore_errors=False,
                      onerror=None)
