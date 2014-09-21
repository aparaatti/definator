# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import os
import logging
import copy
from pathlib import Path

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QKeySequence, QIcon
from .term_linker import TermLinker
from ..widgets.qt_helper_functions import make_action_helper
from ..data.term import Term
from .qtdesigner.ui_QTermEditor import Ui_TermEditor
from .key_press_eater import KeyPressEater
from .str_chooser import StrChooser


class TermEditor(QWidget):
    signal_term_was_changed = pyqtSignal(Term)
    signal_stopped_editing_new_term = pyqtSignal(Term)

    # Undo, redo
    signal_can_undo = pyqtSignal(bool)
    signal_can_redo = pyqtSignal(bool)

    signal_undo_event = pyqtSignal()
    signal_redo_event = pyqtSignal()

    # sent when term links have been changed:
    add_links_to_term = pyqtSignal(Term, list)
    remove_links_from_term = pyqtSignal(Term, list)

    signal_current_term_is_valid = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._redo_text_edit = False
        self._undo_text_edit = False

        self.ui = Ui_TermEditor()
        self.ui.setupUi(self)
        # This is used for detecting if the term content has changed:
        self._old_term = Term()

        # Dialogs:
        self.term_chooser = StrChooser(self)
        self.term_remover = StrChooser(self)
        self.file_chooser = QFileDialog()
        self.file_remover = StrChooser(self)
        self.file_remover.set_title("Unlinkable files")
        self.term_chooser.set_title("Linkable terms")
        self.term_remover.set_title("Unlinkable terms")
        self.file_chooser.setLabelText(QFileDialog.Accept, "Link")
        self.file_chooser.setWindowTitle("Choose files to link.")
        self.term_linker = TermLinker()
        self.ui.verticalLayout.addWidget(self.term_linker)
        self._init_actions()

        self.ui.lineEditTitle.text = ""
        self._current_term = Term()
        self._current_term_has_changed = False

        # Hook into undo/redo of term_editor
        self.eventFilter = KeyPressEater(QKeySequence.Undo, self)
        self.eventFilter2 = KeyPressEater(QKeySequence.Redo, self)
        self.ui.textEditContent.installEventFilter(self.eventFilter)
        self.ui.textEditContent.installEventFilter(self.eventFilter2)
        self.ui.lineEditTitle.installEventFilter(self.eventFilter)
        self.ui.lineEditTitle.installEventFilter(self.eventFilter2)

        self._init_term_linker()
        self._init_signals()

    def set_term(self, term: Term):
        """
        Sets the current term to be edited.

        :param term: Term to edit
        """
        self.clear()
        self._current_term = copy.copy(term)
        self._check_undo_redo()
        self._old_term = term
        if self._old_term.term is "":
            logging.debug("new term")
            self.signal_current_term_is_valid.emit(False)
            self.term_linker.term_linking_enabled(False)
            self.ui.lineEditTitle.setFocus()
        else:
            logging.debug("old term")
            self.term_linker.update_links(term)
            self.term_linker.term_linking_enabled(True)
            self.ui.lineEditTitle.setText(term.term)
            self.ui.textEditContent.setText(term.description)
            self.ui.textEditContent.setFocus()

    def show(self):
        """
        Hooks in to the super class show method and enables
        file linking and unlinking actions when term editor
        is shown.
        """
        self.act_link_files.setEnabled(True)
        self.act_unlink_files.setEnabled(True)
        super().show()

    def hide(self):
        """
        When term editor is hidden the changes need to be saved. In other words
        this is the place, that updates the content of a term or sends a new
        term to the TermController.

        A new term object is always emitted when editing a new term stops and
        the term has non empty term string (Term.term).

        If we are editing already existing term, term editor sets a
        _current_term_has_changed to True if the content, term string or linked
        things have changed. Signal signal_term_was_changed(Term) is emitted if
        the term has changed. Also the undo-redo history of the editing session
        is forgotten and the undo is set to the version of the term that
        existed before the start of the editing session.

        Before hiding term editing related actions are enabled (undo, redo,
        linking/unlinking of files and linking/unlinking of terms).
        """
        if self._old_term.term is "" and \
                self.ui.lineEditTitle.displayText() is not "":
            self._current_term = self._fill_term(self._current_term)
            self.signal_stopped_editing_new_term.emit(self._current_term)
            self.clear()
        else:
            self._increment_term_version()
            if self._current_term_has_changed:
                self._old_term.next_term = self._current_term
                self._current_term.next_term = None
                self.signal_term_was_changed.emit(self._current_term)
            self.clear()

        self.act_undo.setEnabled(False)
        self.act_redo.setEnabled(False)
        self.act_link_files.setEnabled(False)
        self.act_unlink_files.setEnabled(False)
        self.term_linker.term_linking_enabled(False)
        super().hide()

    def _increment_term_version(self, force: bool=False):
        """
        This creates a new Term object of current term, if the content
        of the term (eg. term string or description of the term) have changed
        or if the increment is forced.

        :param force: increments version anyway if True
        :return: True if the version was incremented.
        """
        if (self.ui.lineEditTitle.displayText() != self._old_term.term
                or self.ui.textEditContent.toPlainText() !=
                self._old_term.description or force):
            self._current_term.initialize_next_term()
            self._current_term = self._current_term.next_term
            self._fill_term(self._current_term)
            self._current_term_has_changed = True
            return True
        return False

    def clear(self):
        """
        This method clears all the text in term editor, linked things in
        term_linker and set's _current_term to an empty Term object.
        """
        self.ui.lineEditTitle.clear()
        self.ui.textEditContent.clear()
        self.term_linker.clear()
        self._current_term = Term()
        self._current_term_has_changed = False

    def _fill_term(self, term: Term):
        """
        This method read the content of Term.term input field and
        Term.description editor to a Term object.

        :param term: Term to fill
        :return: filled term
        """
        logging.debug("Filling the term")
        term.term = self.ui.lineEditTitle.displayText()
        text = self.ui.textEditContent.toPlainText()
        white_space_removed = list()

        [white_space_removed.append(line.strip())
            for line in text.splitlines()]
        term.description = os.linesep.join(white_space_removed)

        return term

    def _trigger_event(self, sequence: QKeySequence):
        """
        This is triggered when KeyPressEater filter has caught undo or redo key
        combination on term line editor or term description editor and
        delegates the undo/redo action to this class's undo/redo methods.

        :param sequence: captured key combination as QKeySequence
        """
        if sequence is QKeySequence.Undo:
            self.undo()

        if sequence is QKeySequence.Redo:
            self.redo()

    @pyqtSlot()
    def _validate_term(self):
        """
        This slot checks the validity of the filled term on term editor e.g.
        it ensures that the filled value for Term.term is not "".

        If Term is valid signal_current_term_is_valid(True) is emitted and
        if it's not signal_current_term_is_valid(False) is emitted.
        """
        if self.ui.lineEditTitle.displayText() is "":
            self.signal_current_term_is_valid.emit(False)
        else:
            self.signal_current_term_is_valid.emit(True)

    ########
    # TAGS #
    ########

    @pyqtSlot(str, str)
    def _add_tag(self, item_str: str, group_name: str):
        """
        This is triggered when an item in term linker is activated. We set
        in _init_term_linker method the different item groups for the term
        linker. So we can add the appropriate tag based on the group name we
        have given.
        """
        if group_name == "Image":
            self.add_image_tag(
                self._current_term.get_non_project_file_path(item_str))

    @pyqtSlot()
    def add_image_tag(self, path: Path=Path("/path/to/image"),
                      str_title: str="Image title"):
        """
        This adds an image tag to term description editor at the current
        position of the caret.

        :param path: Optional parameter. Path to the image to show.
        :param str_title: Caption for the image.
        """
        self.ui.textEditContent.insertPlainText('#img("' + str(path) + '","'
                                                + str_title + '")')

    @pyqtSlot()
    def add_title_tag(self, str_title: str="Title"):
        """
        This adds an title tag to term description editor at the current
        position of the caret.

        :param str_title: text for title.
        """
        self.ui.textEditContent.insertPlainText(
            "##" + str_title + "##" + os.linesep + os.linesep)

    @pyqtSlot()
    def add_bullet_list_tag(self):
        """
        Add Bullet list tag to editor
        """
        self.ui.textEditContent.insertPlainText(
            os.linesep + "##LIST##" + os.linesep + "item1" + os.linesep +
            "item2" + os.linesep + "item3" + os.linesep + "##END##"
            + os.linesep
            )

    @pyqtSlot()
    def add_ASCII_tag(self):
        """
        Add ASCII tag to editor
        """
        self.ui.textEditContent.insertPlainText(
            os.linesep + "##ASCII##" + os.linesep + "+---+" + os.linesep
            + "|    |" + os.linesep + "+---+" + os.linesep + "##END##" +
            os.linesep
            )

    ##############################
    # LINKING OF TERMS AND FILES #
    ##############################
    @pyqtSlot()
    def link_terms(self):
        """
        A slot that invokes linking of terms to current term.

        When raised term_chooser dialog (StrChooser) is accepted execution
        continues from _link_terms_accepted method.
        """
        a_list = self.parent().term_str_browser.get_list()
        black_list = []

        if self._current_term.term:
            black_list.append(self._current_term.term)
        if self._current_term.related_terms:
            [black_list.append(term_str)
             for term_str in self._current_term.related_terms]

        [a_list.remove(item) for item in black_list]

        self.term_chooser.set_list(a_list)
        self.term_chooser.show()

    @pyqtSlot(list)
    def _link_terms_accepted(self, str_list):
        """
        Links terms given as a list of strings to current term.
        When list of terms to add is given the linking is delegated
        by emitting add_links_to_term(Term, str_list of terms) signal.
        When terms have been linked the list of linked
        things is updated by invoking term_linker.update_links(current_term).

        :param str_list: list of terms as a string to link
        """
        if len(str_list) > 0:
            self._increment_term_version(True)
            self.add_links_to_term.emit(self._current_term, str_list)
            self.term_linker.update_links(self._current_term)

    @pyqtSlot()
    def unlink_terms(self):
        """
        A slot that invokes unlinking of terms from current term.

        When raised term_remover dialog (StrChooser) is accepted execution
        continues from _unlink_terms_accepted method.
        """
        self.term_remover.set_list(self._current_term.related_terms)
        self.term_remover.show()

    @pyqtSlot(list)
    def _unlink_terms_accepted(self, str_list):
        """
        Unlinks terms given as a list of strings to current term.
        When list of terms to remove is given the unlinking is delegated
        by emitting remove_links_from_term(Term, str_list of terms) signal.

        When terms have been un linked the list of linked
        things is updated by invoking term_linker.update_links(current_term).

        :param str_list: list of terms as a string to link
        """
        if len(str_list) > 0:
            self._increment_term_version(True)
            self.remove_links_from_term.emit(self._current_term, str_list)
            self.term_linker.update_links(self._current_term)

    @pyqtSlot()
    def unlink_files(self):
        """
        A slot that invokes unlinking of files from current term.

        When raised file_remover dialog (StrChooser) is accepted execution
        continues from _unlink_files_accepted method.
        """
        all_files = list()
        [all_files.append(file.name)
            for file in self._current_term.linked_files]
        [all_files.append(image.name)
            for image in self._current_term.linked_images]

        self.file_remover.set_list(all_files)
        self.file_remover.show()

    @pyqtSlot(list)
    def _unlink_files_accepted(self, str_list):
        """
        Unlinks files given as a list of strings containing the filename
        from current term. When files have been removed the list of linked
        things is updated by invoking term_linker.update_links(current_term).

        :param str_list: list of file names as a string to unlink.
        """
        if len(str_list) > 0:
            self._increment_term_version(True)
            [self._current_term.unlink_file(Path(str_file))
                for str_file in str_list]
            self.term_linker.update_links(self._current_term)

    @pyqtSlot()
    def link_files(self):
        """
        A slot that invoke linking of files to current term.

        After the files have been linked to current term the term_linker is
        updated by invoking term_linker.update_links(current_term) method.
        """
        file_names = self.file_chooser.getOpenFileNames(
            self, "Select a file", '', "All Files (*)", '')
        if file_names is not None and file_names[0] is not None:
            self._increment_term_version(True)
            [self._current_term.link_file(Path(file_name))
                for file_name in file_names[0]]
            self.term_linker.update_links(self._current_term)

    ####################################
    # UNDO - REDO and COPY, CUT, PASTE #
    ####################################
    @pyqtSlot()
    def _copy(self):
        """
        This slot routes copying to right widget when copy action is invoked
        (when copy is chosen from main window menu).
        """
        if self.ui.textEditContent.hasFocus():
            self.ui.textEditContent.copy()
        if self.ui.lineEditTitle.hasFocus():
            self.ui.lineEditTitle.copy()

    @pyqtSlot()
    def _paste(self):
        """
        This slot routes paste to right widget when paste action is invoked
        (when paste is chosen from main window menu).
        """
        if self.ui.textEditContent.hasFocus():
            self.ui.textEditContent.paste()
        if self.ui.lineEditTitle.hasFocus():
            self.ui.lineEditTitle.paste()

    @pyqtSlot()
    def _cut(self):
        """
        This slot routes cut to right widget when cut action is invoked (when
        cut is chosen from main window menu).
        """
        if self.ui.textEditContent.hasFocus():
            self.ui.textEditContent.cut()
        if self.ui.lineEditTitle.hasFocus():
            self.ui.lineEditTitle.cut()

    @pyqtSlot()
    def undo(self):
        """
        Undoes edit.

        If undo is available in text editor for term content, it is undone. If
        undo is not available in text editor for content it is checked if the
        title field for Term.term has undo available. If it has, term title
        edits are undone. When term field runs out of undoes it is checked if
        the term it self has older version linked to it. When we run out of
        undo for current term signal_can_undo(False) is emitted.
        """
        if self._undo_text_edit:
            self.ui.textEditContent.undo()
        elif self.ui.lineEditTitle.isUndoAvailable():
            self.ui.lineEditTitle.undo()
        elif not self._current_term or not self._current_term.can_undo:
            self.act_undo.setEnabled(False)
        else:
            self.set_term(self._current_term.previous_term)
        self.check_if_can_undo()

    @pyqtSlot()
    def redo(self):
        """
        Redoes undone edit.

        If redo is available in term title field for term, it is redone. If
        redo is not available in term title field for Term.term, it is checked
        if the term text editor for term content has redo available. If it has,
        content edits are redone. When term text editor runs out of redoes it
        is checked if the term it self has newer version linked to it. When we
        run out of redo for current term signal_can_redo(False) is emitted.
        """
        if self.ui.lineEditTitle.isRedoAvailable():
            self.ui.lineEditTitle.redo()
        elif self._redo_text_edit:
            self.ui.textEditContent.redo()
        elif not self._current_term or not self._current_term.can_redo:
            self.act_redo.setEnabled(False)
        else:
            self.set_term(self._current_term.next_term)
        self.check_if_can_redo()

    @pyqtSlot(bool)
    def _redo_available_in_text_edit(self, boolean):
        """
        This slot is triggered from term content editor when it runs out of
        redo (boolean=False) or becomes able to redo (boolean=True).

        :param boolean: True if textEditContent can redo, False if can't.
        """
        self._redo_text_edit = boolean
        self.check_if_can_redo()

    @pyqtSlot(bool)
    def _undo_available_in_text_edit(self, boolean):
        """
        This slot is triggered from term content editor when it runs out of
        undo (boolean=False) or becomes able to undo (boolean=True).

        :param boolean: True if textEditContent can undo, False if can't.
        """
        self._undo_text_edit = boolean
        self.check_if_can_undo()

    @pyqtSlot()
    def _check_undo_redo(self):
        """
        This is a helper method to check if there are undoes and redoes left.
        """
        self.check_if_can_undo()
        self.check_if_can_redo()

    def check_if_can_undo(self):
        """
        If term text editor or term title line edit can undo undo
        (action act_undo) is enabled. if they can't undo it is checked if the
        current term is None and if so undo action is disabled. If current term
        is not None the term is queried if undo is available and the boolean
        value for the query is set for action undo availability.
        """

        if self._undo_text_edit or self.ui.lineEditTitle.isUndoAvailable():
            self.act_undo.setEnabled(True)
        else:
            self.act_undo.setEnabled(self._current_term.can_undo)

    def check_if_can_redo(self):
        """
        If term text editor or term title line edit can redo action act_redo
        for redo is enabled. if they can't redo it is checked if the current
        term is None and if so the redo action is disabled. If current term is
        not None the term is queried if redo is available and the boolean value
        for the query set as the value of availability of redo.
        """
        if self._redo_text_edit or self.ui.lineEditTitle.isRedoAvailable():
            self.act_redo.setEnabled(True)
        else:
            self.act_redo.setEnabled(self._current_term.can_redo)

    ##########################
    # INITIALIZATION METHODS #
    ##########################
    def _init_actions(self):
        # Edit
        self.act_copy = make_action_helper(
            self, "Copy", "Copy to clipboard", QKeySequence.Copy,
            QIcon.fromTheme('edit-copy'))
        self.act_copy.triggered.connect(self._copy)
        self.act_paste = make_action_helper(
            self, "Paste", "Paste from clipboard", QKeySequence.Paste,
            QIcon.fromTheme('edit-paste'))
        self.act_paste.triggered.connect(self._paste)
        self.act_cut = make_action_helper(
            self, "Cut", "Cut to clipboard", QKeySequence.Cut,
            QIcon.fromTheme('edit-cut'))
        self.act_cut.triggered.connect(self._cut)
        self.act_undo = make_action_helper(
            self, "Undo", "Undo previous change", QKeySequence.Undo,
            QIcon.fromTheme('edit-undo'))
        self.act_undo.triggered.connect(self.undo)
        self.act_redo = make_action_helper(
            self, "Redo", "Redo undone change", QKeySequence.Redo,
            QIcon.fromTheme('edit-redo'))
        self.act_redo.triggered.connect(self.redo)

        # Linking of files
        self.act_link_files = make_action_helper(
            self, "Link &files", "Link files to current term", "ctrl+l",
            QIcon.fromTheme('list-add'))
        self.act_link_files.triggered.connect(self.link_files)
        self.act_unlink_files = make_action_helper(
            self, "U&nlink files", "Unlink files from current term", "ctrl+u",
            QIcon.fromTheme('list-remove'))
        self.act_unlink_files.triggered.connect(self.unlink_files)

    def _init_term_linker(self):
        self.term_linker.ui_link_list.add_item_group("Term", "Yellow", "Black")
        self.term_linker.ui_link_list.add_item_group("Image", "Cyan", "Black")
        self.term_linker.ui_link_list.add_item_group(
            "File", "Magenta", "Black")

    def _init_signals(self):
        # Editing
        self.ui.addImageToolButton.clicked.connect(self.add_image_tag)
        self.ui.addTitleToolButton.clicked.connect(self.add_title_tag)
        self.ui.addASCIIToolButton.clicked.connect(self.add_ASCII_tag)
        self.ui.addBulletListToolButton.clicked.connect(
            self.add_bullet_list_tag)
        self.ui.lineEditTitle.textChanged.connect(self._validate_term)

        self.ui.lineEditTitle.textChanged.connect(self._check_undo_redo)
        self.ui.textEditContent.textChanged.connect(self._check_undo_redo)

        self.ui.textEditContent.redoAvailable.connect(
            self._redo_available_in_text_edit)
        self.ui.textEditContent.undoAvailable.connect(
            self._undo_available_in_text_edit)

        # Linking of terms
        self.term_linker.linkTermsClicked.connect(self.link_terms)
        self.term_linker.unlinkTermsClicked.connect(self.unlink_terms)
        self.term_chooser.str_list_accepted.connect(self._link_terms_accepted)
        self.term_remover.str_list_accepted.connect(
            self._unlink_terms_accepted)

        # Linking of files
        self.term_linker.add_file.connect(self.link_files)
        self.term_linker.remove_files.connect(self.unlink_files)
        self.file_remover.str_list_accepted.connect(
            self._unlink_files_accepted)
        self.term_linker.ui_link_list.signal_item_activated.connect(
            self._add_tag)
