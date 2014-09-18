# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
# Based on:
# http://qt-project.org/doc/qt-4.8/qobject.html#installEventFilter
# and
# http://codeprogress.com/python/libraries/pyqt/showPyQTExample.php?key=QApplicationInstallEventFiler&index=379
import logging
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QKeySequence


class KeyPressEater(QObject):
    def __init__(self, sequence: QKeySequence, sender):
        super().__init__()
        self.sender = sender
        self.sequence = sequence

    def eventFilter(self, object, event):
        if event.type() == QEvent.KeyPress and not event.isAutoRepeat():
            if event.matches(self.sequence):
                logging.info("nom nom nom eating a key sequence: " + str(self.sequence))
                self.sender._trigger_event(self.sequence)
                return True
        return super().eventFilter(object, event)
