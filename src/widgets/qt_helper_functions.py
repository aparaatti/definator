__author__ = 'aparaatti'
import logging
from PyQt5.QtWidgets import QAction, QShortcut, QMessageBox
from PyQt5.QtGui import QIcon


def make_action_helper(self, text, help_text, shortcut: QShortcut=None,
                       icon_path=None):
    """ Idea from "Rapid GUI Programming with Python and Qt" by Mark Summerfield
        Published:  Jun 2008
        Publisher:  Prentice Hall """
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
    warning_message = QMessageBox(
            QMessageBox.Warning, title, message, QMessageBox.NoButton, self)
    warning_message.addButton("&Ok", QMessageBox.RejectRole)
    warning_message.exec_()