# -*- coding: utf-8 -*-
#Based on:
#http://qt-project.org/doc/qt-4.8/qobject.html#installEventFilter
#and
#http://codeprogress.com/python/libraries/pyqt/showPyQTExample.php?key=QApplicationInstallEventFiler&index=379
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
                print("nom nom nom")
                self.sender._trigger_event(self.sequence)
                return True
        return super().eventFilter(object, event)
