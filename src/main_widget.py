# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QMessageBox
from PyQt5.QtGui import QKeySequence, QIcon

from .action_helper import make_action_helper
from .data.term import Term

from .widgets.str_browser import StrBrowser
from .widgets.term_display import TermDisplay
from .widgets.term_editor import TermEditor
from .widgets.term_linker import TermLinker
from .widgets.str_chooser import StrChooser
from .widgets.link_list import LinkList


class MainWidget(QWidget):
    """
    Wrapper widget which contains the term handling widgets and routing of
    events between them and to the parent widget. Also knows the current term
    being examined
    """
    #sent when a exist term content is updated (termEditor knows this)
    update_term = pyqtSignal(Term)
    term_updated = pyqtSignal(Term)

    #sent when term links have been changed:
    add_links_to_term = pyqtSignal(str, list)
    remove_links_from_term = pyqtSignal(str, list)

    #sent when file links have been changed:
    add_files_to_term = pyqtSignal(str, list)
    remove_files_from_term = pyqtSignal(str, list)

    #sent when user wants to add a new term (needed to be public?)
    create_term = pyqtSignal()
    #sent when a new term has been created, can use str?
    add_new_term = pyqtSignal(Term)
    remove_term = pyqtSignal(Term)
    save_changes = pyqtSignal()

    term_str_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.current_term = None

        #Modules:
        self.term_str_browser = StrBrowser("Term Browser")
        self.term_display = TermDisplay()
        self.related_terms = LinkList("Related terms")
        self.term_editor = TermEditor()
        self.term_linker = TermLinker()

        #Dialogs:
        self.term_chooser = StrChooser(self)
        self.term_remover = StrChooser(self)
        self.file_chooser = QFileDialog()
        self.file_remover = StrChooser(self)

        self.term_linker.add_item_group("Term", "Yellow", "Black")
        self.term_linker.add_item_group("Image", "Cyan", "Black")
        self.term_linker.add_item_group("File", "Magenta", "Black")

        self.setMinimumSize(QSize(750, 200))

        self._init_actions()
        self._init_layout()
        #New project state:
        self._init_state()

        # Inner interaction logic:
        self.term_editor.signal_stopped_editing.connect(self._stopped_editing)
        self.term_editor.signal_stopped_editing_new_term.connect(
            self._stopped_editing_new_term)
        self.term_editor.signal_valid.connect(self.act_view_term.setEnabled)

        self.term_str_browser.str_selected.connect(self._change_term)
        self.related_terms.link_selected.connect(self._change_term)
        self.term_str_browser.list_is_empty.connect(self.reset)

        #Linking of terms
        self.term_linker.linkTermsClicked.connect(self.link_terms)
        self.term_linker.unlinkTermsClicked.connect(self.unlink_terms)
        self.term_chooser.str_list_accepted.connect(self._link_terms_accepted)
        self.term_remover.str_list_accepted.connect(self._unlink_terms_accepted)

        #Linking of files
        self.term_linker.add_file.connect(self.link_files)
        self.term_linker.remove_files.connect(self.unlink_files)
        self.file_remover.str_list_accepted.connect(self._unlink_files_accepted)

        #Undo - redo
        self.term_editor.signal_can_undo.connect(self._undo_available_in_text_edit)
        self.term_editor.signal_can_redo.connect(self._redo_available_in_text_edit)

    def _set_current_term(self, term: Term):
        self.term_str_browser.set_current_str(term.term)
        self.term_display.set_term(term)
        self.term_linker.update_item_group("Term", term.related_terms)
        self.term_linker.update_item_group("Image", [path.name for path in term.linked_images])
        self.term_linker.update_item_group("File", [path.name for path in term.linked_files])
        self.term_linker.populate()
        self.term_editor.set_term(term)
        self.related_terms.set_current_html(term.related_terms_as_html)
        self.current_term = term
        self.act_undo.setEnabled((self.current_term.previous_term is not None))
        self.act_redo.setEnabled((self.current_term.next_term is not None))

    def _adding_enabled(self, boolean: bool):
        self.act_add_term.setEnabled(boolean)

    def _removing_enabled(self, boolean: bool):
        self.act_rem_term.setEnabled(boolean)

    def _editing_enabled(self, boolean: bool):
        self.act_edit_term.setEnabled(boolean)

    def _linkin_enabled(self, boolean: bool):
        self.act_link_terms.setEnabled(boolean)
        self.act_unlink_terms.setEnabled(boolean)
        self.act_link_files.setEnabled(boolean)
        self.act_unlink_files.setEnabled(boolean)
        if boolean:
            self.term_linker.edit_mode()
        else:
            self.term_linker.display_mode()

    def _show_term_editor(self):
        if self.term_display.isVisible():
            self.term_display.hide()
            self.related_terms.hide()
            self.term_editor.show()
            self.term_linker.show()
            self._adding_enabled(False)
            self._removing_enabled(False)
            self._editing_enabled(False)
            self.act_view_term.setEnabled(True)

    @pyqtSlot()
    def show_term_display(self):
        """
        TermEditor emits changes when it is hidden.
        """
        if self.term_editor.isVisible():
            self.term_linker.hide()
            self.term_editor.hide()
            self.term_display.show()
            self.related_terms.show()
            self._adding_enabled(True)
            self.act_view_term.setEnabled(False)
            self._editing_enabled(True)
            self._removing_enabled(True)

    def refresh_current_view(self):
        if self.term_editor.isVisible():
            self._show_term_editor()
        else:
            self.show_term_display()

    # In coming slots from outside:
    @pyqtSlot()
    def reset(self):
        self.term_str_browser.set_list([])
        self.current_term = None
        self._init_state()
        self.create_new_term()

    @pyqtSlot(tuple, Term)
    def initialize_a_project(self, terms: tuple, term: Term):
        self.term_str_browser.set_list(list(terms))
        self.show_term_display()
        self._set_current_term(term)

    @pyqtSlot()
    def unmark(self):
        self.term_str_browser.unmark()

    @pyqtSlot(Term)
    def change_term(self, term: Term):
        self._set_current_term(term)
        self.show_term_display()

    @pyqtSlot(Term)
    def term_has_been_updated(self, term: Term):
        self.term_str_browser.mark_str(term.term)
        self._set_current_term(term)

    @pyqtSlot(Term)
    def added_a_term(self, term: Term):
        self.term_str_browser.add_a_str(term.term)
        self._set_current_term(term)

    @pyqtSlot(Term)
    def term_has_been_removed(self, term: Term):
        self.term_str_browser.rem_a_str(term.term)

    @pyqtSlot(bool)
    def _redo_available_in_text_edit(self, boolean):
        self._redo_text_edit = boolean
        if boolean:
            self.act_redo.setEnabled(True)
        elif not self.current_term or not self.current_term.can_redo:
            self.act_redo.setEnabled(False)

    @pyqtSlot(bool)
    def _undo_available_in_text_edit(self, boolean):
        self._undo_text_edit = boolean
        if boolean:
            self.act_undo.setEnabled(True)
        elif not self.current_term or not self.current_term.can_undo:
            self.act_undo.setEnabled(False)

    @pyqtSlot()
    def _undo(self):
        if self._undo_text_edit:
            self.term_editor.undo()
        else:
            self._set_current_term(self.current_term.previous_term)
            self.refresh_current_view()

        if not self.current_term or not self.current_term.can_undo:
            self.act_undo.setEnabled(False)

    @pyqtSlot()
    def _redo(self):
        if self._redo_text_edit:
            self.term_editor.redo()
        else:
            self._set_current_term(self.current_term.next_term)
            self.refresh_current_view()

        if not self.current_term or not self.current_term.can_redo:
            self.act_redo.setEnabled(False)

    def save_current_term(self):
        pass

    @pyqtSlot()
    def link_terms(self):
        self._ugly_fix_to_catch_edits()
        a_list = self.term_str_browser.get_list()
        black_list = [self.current_term.term]

        if self.current_term.related_terms:
            [black_list.append(term_str) for term_str in self.current_term.related_terms]

        [a_list.remove(item) for item in black_list]

        self.term_chooser.set_list(a_list)
        #IF accepted, will return to _link_terms_accepted method
        self.term_chooser.show()

    @pyqtSlot()
    def unlink_terms(self):
        self.show_term_display()
        self.term_remover.set_list(self.current_term.related_terms)
        self.term_remover.show()

    @pyqtSlot()
    def link_files(self):
        self._ugly_fix_to_catch_edits()
        file_names = self.file_chooser.getOpenFileNames(
            self, "Select a file", '', "All Files (*)", '')
        if file_names is not None and file_names[0] is not None and self.current_term is not None:
            self.add_files_to_term.emit(self.current_term.term, file_names[0])

    @pyqtSlot()
    def unlink_files(self):
        self.show_term_display()
        all_files = list()
        [all_files.append(file.name) for file in self.current_term.linked_files]
        [all_files.append(image.name) for image in self.current_term.linked_images]
        self.file_remover.set_list(all_files)
        self.file_remover.show()

    # Slots for inner signals and triggering of events to be passed on to parent
    # module.
    @pyqtSlot()
    def create_new_term(self):
        self.show_term_display()
        self.term_editor.set_term(None)
        self.term_linker.clear()
        self.term_linker.setEnabled(False)
        self._show_term_editor()
        self.act_view_term.setEnabled(False)
        self.act_link_files.setEnabled(False)
        self.act_link_terms.setEnabled(False)
        self.act_unlink_terms.setEnabled(False)
        self.act_unlink_files.setEnabled(False)

    @pyqtSlot()
    def edit_current_term(self):
        self._set_current_term(self.current_term)
        self.term_linker.setEnabled(True)
        self._show_term_editor()

    @pyqtSlot()
    def _remove_term(self):
        if not self.current_term:
            return
        remove = QMessageBox.question(
            self, "Are you sure you want to delete this term?",
            "Are you sure, you wannt to delete this term?",
            QMessageBox.Yes | QMessageBox.No)
        print("remove response: " + str(remove))
        if remove == QMessageBox.Yes:
            self.remove_term.emit(self.current_term)

    @pyqtSlot(Term)
    def _stopped_editing(self, term: Term):
        # Tässä liitetään muokattu termi edelliseen termiin.
        self.current_term.next_term = term
        self._set_current_term(term)
        self.term_display.show()
        self.update_term.emit(term)

    @pyqtSlot(Term)
    def _stopped_editing_new_term(self, term: Term):
        if term.term is None:
            self._show_term_editor()
        else:
            self.add_new_term.emit(term)

    @pyqtSlot(str)
    def _change_term(self, term_str):
        self.term_str_selected.emit(term_str)

    @pyqtSlot(list)
    def _link_terms_accepted(self, str_list):
        if len(str_list) > 0:
            self.add_links_to_term.emit(self.current_term.term, str_list)

    @pyqtSlot(list)
    def _unlink_terms_accepted(self, str_list):
        if len(str_list) > 0:
            self.remove_links_from_term.emit(self.current_term.term, str_list)

    @pyqtSlot(list)
    def _unlink_files_accepted(self, str_list):
        if len(str_list) > 0:
            self.remove_files_from_term.emit(self.current_term.term, str_list)

    def _init_actions(self):
        #ACTIONS:
        self.act_link_terms = make_action_helper(self, "&Link terms", "Link terms to current term", "alt+l", QIcon.fromTheme('list-add'))
        self.act_link_terms.triggered.connect(self.link_terms)
        self.act_unlink_terms = make_action_helper(self, "&Unlink terms", "Remove related terms from current term", "alt+u", QIcon.fromTheme('list-remove'))
        self.act_unlink_terms.triggered.connect(self.unlink_terms)
        self.act_link_files = make_action_helper(self, "Link &files", "Link files to current term", "alt+k", QIcon.fromTheme('list-add'))
        self.act_link_files.triggered.connect(self.link_files)
        self.act_unlink_files = make_action_helper(
            self, "U&nlink files", "Unlink files from current term", "alt+y", QIcon.fromTheme('list-remove'))
        self.act_unlink_files.triggered.connect(self.unlink_files)
        self.act_rem_term = make_action_helper(
            self, "&Remove term", "Remove current term", QKeySequence.Delete, QIcon.fromTheme('edit-delete'))
        self.act_rem_term.triggered.connect(self._remove_term)
        self.act_save_term = make_action_helper(
            self, "&Save current term", "Save changes for term", None, QIcon.fromTheme('document-save'))
        self.act_save_term.triggered.connect(self.save_current_term)
        self.act_view_term = make_action_helper(
            self, "&View current term", "View current term", QKeySequence.Close, QIcon.fromTheme('document-revert'))
        self.act_view_term.triggered.connect(self.show_term_display)
        self.act_edit_term = make_action_helper(
            self, "&Edit current term", "Edit current term", "ctrl+e", QIcon.fromTheme('accessories-text-editor'))
        self.act_edit_term.triggered.connect(self.edit_current_term)
        self.act_add_term = make_action_helper(
            self, "&Add term", "Add new term to project.",
            QKeySequence.New, QIcon.fromTheme('document-new',))
        self.act_add_term.triggered.connect(self.create_new_term)

        self.act_undo = make_action_helper(
            self, "Undo", "Undo previous change", QKeySequence.Undo, QIcon.fromTheme('edit-undo'))
        self.act_undo.triggered.connect(self._undo)
        self.act_redo = make_action_helper(
            self, "Redo", "Redo undone change", QKeySequence.Redo, QIcon.fromTheme('edit-redo'))
        self.act_redo.triggered.connect(self._redo)

    def _init_layout(self):
        #Set layout
        layout_h = QHBoxLayout()

        layout_v_term_view = QVBoxLayout()
        layout_v_term_browser = QVBoxLayout()

        #Term browser area:
        layout_h.addLayout(layout_v_term_browser)
        layout_v_term_browser.addWidget(self.term_str_browser)

        layout_v_term_view.addWidget(self.term_editor)
        layout_v_term_view.addWidget(self.term_linker)
        layout_v_term_view.addWidget(self.term_display)
        layout_v_term_view.addWidget(self.related_terms)

        #Add editor area to browser layout
        layout_h.addLayout(layout_v_term_view)
        self.setLayout(layout_h)

    def _init_state(self):
        self.term_str_browser.setFocus()
        self.act_add_term.setEnabled(False)
        self.act_rem_term.setEnabled(False)
        self.act_edit_term.setEnabled(False)
        self.act_view_term.setEnabled(False)
        self.act_link_terms.setEnabled(False)
        self.act_unlink_terms.setEnabled(False)
        self.act_link_files.setEnabled(False)
        self.act_unlink_files.setEnabled(False)
        self.act_undo.setEnabled(False)
        self.act_redo.setEnabled(False)
        self.act_save_term.setEnabled(False)
        self._redo_text_edit = False
        self._undo_text_edit = False
        self.term_linker.edit_mode()
        self.term_display.hide()
        self.related_terms.hide()

    def _ugly_fix_to_catch_edits(self):
        self.show_term_display()
        self.term_editor.set_term(self.current_term)
        self._show_term_editor()
