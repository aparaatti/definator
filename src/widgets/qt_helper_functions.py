# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
__author__ = 'aparaatti'
import logging
from PyQt5.QtWidgets import QAction, QShortcut, QMessageBox
from PyQt5.QtGui import QIcon


def make_action_helper(self, text, help_text, shortcut: QShortcut=None,
                       icon_path=None):
    """
    Builds an action.

    Idea from "Rapid GUI Programming with Python and Qt" by Mark Summerfield
        Published:  Jun 2008
        Publisher:  Prentice Hall

    :param text: Short text for description of action.
    :param help_text: Longer description for action.
    :param shortcut: Shortcut key combination for action.
    :param icon_path: Path of icon for action
    :return: built action as QAction
    """
    if icon_path is not None:
        action = QAction(QIcon(icon_path), text, self)
    else:
        action = QAction(text, self)
    if shortcut:
        action.setShortcut(shortcut)

    action.setToolTip(help_text)
    action.setStatusTip(help_text)
    logging.debug("Action set for " + str(type(self)) + ": " + text + " " + str(shortcut))

    return action


def warning_dialog(self, title: str, message: str):
    """
    Shows a warning dialog with an ok -button.

    :param title: Dialog window title
    :param message: Message on dialog
    """
    warning_message = QMessageBox(
        QMessageBox.Warning, title, message, QMessageBox.NoButton, self)
    warning_message.addButton("&Ok", QMessageBox.RejectRole)
    warning_message.exec_()


def info_dialog(self, title: str, message: str):
    """
    Shows a information dialog with an ok -button.

    :param title: Dialog window title
    :param message: Message on dialog
    """
    info_message = QMessageBox(
        QMessageBox.Information, title, message, QMessageBox.NoButton, self)
    info_message.addButton("&Ok", QMessageBox.RejectRole)
    info_message.exec_()
