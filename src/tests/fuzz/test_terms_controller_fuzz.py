# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from pathlib import Path

import pytest
import os

from tests import helper_for_tests
from terms_controller import TermsController
from data.term import Term
from data.term_exceptions import IllegalCharacterInTermNameException

class TestTermsController:

    @pytest.mark.randomize(name=str, name2=str,
                           str_attrs=("digits", "ascii_letters", "whitespace"),
                           ncalls=15)
    def test_save_rename_and_save(self, name, name2):
        helper_for_tests.make_tmp_project()
        TMP = helper_for_tests.TMP

        tc = TermsController()
        try:
            tc.add_term(Term(name))
        except IllegalCharacterInTermNameException as ie:
            print('Illegal character was "%s".' % ie.value)
            return

        tc.save_project_as(TMP)
        tc.load_project(TMP)

        term = tc.get_term(name)

        term.initialize_next_term()
        new_term = term.next_term
        try:
            new_term.term = name2
        except IllegalCharacterInTermNameException as ie:
            print('Illegal character was "%s".' % ie.value)
            return

        tc.update_term(new_term)
        tc.save_project()
        tc.load_project(TMP)
        tc.get_term(name2)

    @pytest.mark.randomize(fileprefix=str,
                           str_attrs=("digits", "whitespace", "punctuation",
                           "ascii_letters"),
                           ncalls=150)
    def test_link_jibberish_file_name(self, fileprefix):
        helper_for_tests.make_tmp_project()
        TMP = helper_for_tests.TMP

        try:
            tmp_file_name = helper_for_tests.make_tmp_file(fileprefix)
        except (FileNotFoundError, PermissionError):
            return

        tmp_path = Path(tmp_file_name)
        # index 0 : file handle
        # index 1 : absolute path
        tc = TermsController()
        try:
            tc.add_term(Term("filecontainer"))
        except IllegalCharacterInTermNameException as ie:
            print('Illegal character was "%s".' % ie.value)
            return
        tc.save_project_as(TMP)
        tc.load_project(TMP)
        term = tc.get_term("filecontainer")
        # We make new term and test linking of tmp file
        term.initialize_next_term()
        new_term = term.next_term

        new_term.link_file(tmp_path)

        # We have linked a file
        tc.update_term(new_term)

        tc.save_project()
        os.remove(tmp_file_name)

        assert Path(term.path / term.term / tmp_path.name).exists()

    @pytest.mark.randomize(name1=str, name2=str,
                           str_attrs=("digits", "ascii_letters", "whitespace"),
                           ncalls=15)
    def test_save_and_load_link_jibberish(self, name1, name2):
        helper_for_tests.make_tmp_project()
        TMP = helper_for_tests.TMP

        tc = TermsController()

        try:
            tc.add_term(Term(name1))
            tc.add_term(Term(name2))
        except IllegalCharacterInTermNameException as ie:
            print('Illegal character was "%s".' % ie.value)
            return

        tc.save_project_as(TMP)
        term = tc.get_term(name1)
        term2 = tc.get_term(name2)

        term.initialize_next_term()
        new_term = term.next_term
        new_term.link_term(term2)

        tc.update_term(new_term)
        tc.save_project()

    @pytest.mark.randomize(jibberish=str,
                           str_attrs=("digits", "punctuation", "whitespace",
                                      "ascii_letters"),
                           ncalls=150)
    def test_describe_jibberish_save_and_load(self, jibberish):
        name = "jibberish_description"
        helper_for_tests.make_tmp_project()
        TMP = helper_for_tests.TMP

        tc = TermsController()

        try:
            tc.add_term(Term(name))
        except IllegalCharacterInTermNameException as ie:
            print('Illegal character was "%s".' % ie.value)
            return

        tc.save_project_as(TMP)

        # We add jibberish to term description
        term = tc.get_term(name)

        # Increment term version
        term.initialize_next_term()
        new_term = term.next_term

        # Set the description.
        new_term.description = jibberish

        # Update the term to a new one.
        tc.update_term(new_term)

        tc.save_project()

        tc2 = TermsController()
        tc2.load_project(Path(TMP))

        term = tc2.get_term(term.term)

        assert term.description == new_term.description


