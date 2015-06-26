from pathlib import Path
from hypothesis import *
from hypothesis import strategies
from hypothesis import settings
import pytest
import shutil
import tempfile
import os
import sys

from PyQt5.QtWidgets import QApplication


class TestStarter:
    @pytest.mark.randomize(argument=str,
                           str_attrs=("punctuation", "ascii_letters"),
                           ncalls=10)
    def test_argument(self, argument):
        sys.argv = ['./definator.py', argument]
        do_quit = True
        try:
            import definator
            definator.run()
        except SystemExit:
            do_quit = False

        if do_quit:
            assert isinstance(definator.app, PyQt5.QtWidgets.QApplication)
            definator.app.quit()


@given(strategies.text(), settings=Settings(max_examples=500))
def test_argument(argument):
    sys.argv = ['./definator.py', argument]
    app = QApplication(sys.argv)
    assert(app.arguments, sys.argv)
    app.quit()
