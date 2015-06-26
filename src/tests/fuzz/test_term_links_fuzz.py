#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#

from terms_controller import TermsController
from data.term_links import Links

from pathlib import Path
import pytest

__author__ = 'Niko Humalamäki'


class TestTermLinks:

    @pytest.mark.randomize(name=str,
                           str_attrs=("digits", "whitespace", "ascii_letters"),
                           ncalls=10)
    def test_link_unlink_term(self, name):
        links = Links()
        links.link_term(name)
        assert name in links.linked_terms

    @pytest.mark.randomize(name=str,
                           str_attrs=("digits", "whitespace", "ascii_letters"),
                           ncalls=300)
    def test_link_save_load(self, name):
        links = Links()
        links.link_term(name)
        assert name in links.linked_terms

        links.save(Path("/tmp/"), [])

        links = Links()
        links.load(Path("/tmp/"))

        assert name in links.linked_terms