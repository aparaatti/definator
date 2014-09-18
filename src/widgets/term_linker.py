# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import collections

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from ..data.term import Term
from .link_buttons import LinkButtons
from .key_list import KeyList


class TermLinker(QWidget):
    linkTermsClicked = pyqtSignal()
    unlinkTermsClicked = pyqtSignal()
    add_file = pyqtSignal()
    remove_files = pyqtSignal()

    """
    Signals do not pass current term, since the module doesn't need to know it.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = list()
        self._item_dictionary = collections.OrderedDict()
        self.ui_buttons = LinkButtons(self)
        self.ui_link_list = KeyList(self)

        layout_h = QHBoxLayout()
        layout_h.addWidget(self.ui_link_list)
        layout_h.addWidget(self.ui_buttons)
        self.setLayout(layout_h)

        self.ui_buttons.form.buttonLinkTerms.clicked.connect(self.linkTermsClicked)
        self.ui_buttons.form.buttonUnlinkTerms.clicked.connect(self.unlinkTermsClicked)
        self.ui_buttons.form.buttonAddFile.clicked.connect(self.add_file)
        self.ui_buttons.form.buttonRemoveFiles.clicked.connect(self.remove_files)

    def update_links(self, term: Term):
        self.ui_link_list.update_item_group("Term", term.related_terms)
        self.ui_link_list.update_item_group("Image", [path.name for path in term.linked_images])
        self.ui_link_list.update_item_group("File", [path.name for path in term.linked_files])
        self.ui_link_list.populate()

    def clear(self):
        self.ui_link_list.clear()

    def term_linking_enabled(self, boolean: bool):
        self.ui_buttons.form.buttonLinkTerms.setEnabled(boolean)
        self.ui_buttons.form.buttonUnlinkTerms.setEnabled(boolean)
