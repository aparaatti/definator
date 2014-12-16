# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from pathlib import Path
import pytest
import shutil
import tempfile
import os
import src.terms_controller
from src.data.term import Term

unicode = str

class TestTermsController:
    prev_name = "1. Startup"
    prev_name2 = "2. View term"

    @classmethod
    def setup_class(cls):
        Path("test-generated-project/").mkdir()
        tc = src.terms_controller.TermsController()
        tc.load_project(Path("help-project"))
        tc.save_project_as(Path("test-generated-project"))

    @pytest.mark.randomize(name=str, str_attrs=("digits", "punctuation",
                                                "whitespace", "ascii_letters"),
                           ncalls=10)
    def test_rename_and_save(self, name):
        # min_length apparently not implemented for python 3
        if len(name) == 0:
            return

        tc = src.terms_controller.TermsController()
        tc.load_project(Path("test-generated-project/"))
        term = tc.get_term(TestTermsController.prev_name)

        term.initialize_next_term()
        new_term = term.next_term
        new_term.term = name

        tc.update_term(new_term)
        tc.save_project()
        tc.load_project(Path("test-generated-project/"))
        term = tc.get_term(name)
        TestTermsController.prev_name = name
        assert isinstance(term, Term)


    """
    B3: 0cd22ed885bf209e99e68acf11004900addc3573
    file in term folder:
        unsaved-changes-kf5.png
        linked-terms-and-files-kf5.png
    """
    @pytest.mark.randomize(name2=str, str_attrs=("digits", "punctuation",
                                                "whitespace", "ascii_letters"),
                           ncalls=10)
    def test_save_rename_and_save(self, name2):
        # min_length apparently not implemented for python 3
        if len(name2) == 0:
            return
        tc = src.terms_controller.TermsController()
        tc.load_project(Path("test-generated-project/"))
        term = tc.get_term(TestTermsController.prev_name2)

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
        tc.update_term(new_term)
        tc.save_project()
        os.remove(file.name)

        assert Path(term.path / term.term / tmp_path.name).exists()

        term = tc.get_term(TestTermsController.prev_name2)

        assert term.term == TestTermsController.prev_name2

        term.initialize_next_term()
        second_new_term = term.next_term
        second_new_term.term = name2
        tc.update_term(second_new_term)
        tc.save_project()

        term = tc.get_term(name2)
        assert term.term == name2
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

        assert file2
        assert file3
        assert file1

        TestTermsController.prev_name2 = name2

    @classmethod
    def teardown_class(cls):
        shutil.rmtree("test-generated-project/", ignore_errors=False,
                      onerror=None)
