# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtWidgets import QWidget

from .qtdesigner.ui_QLinkButtons import Ui_Form


class LinkButtons(QWidget):
    """
    This is a widget containing 4 buttons, link/unlink term and link/unlink file.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form = Ui_Form()
        self.form.setupUi(self)
