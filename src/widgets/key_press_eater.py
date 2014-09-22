# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
import logging
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QKeySequence


class KeyPressEater(QObject):
    """
    This class can be attached to a QWidget.installEventFiltter method. It
    intercepts key sequence (QKeySequence) that was given to it on
    intialization.

    This is heavily taken from `qt documentation`_ and `codeprogress.com`_ was
    also looked into.

    .. _qt documentation: http://qt-project.org/doc/qt-4.8/qobject.html#installEventFilter
    .. _codeprogress.com: http://codeprogress.com/python/libraries/pyqt/showPyQTExample.php?key=QApplicationInstallEventFiler&index=379


    :param: sequence, a QKeySequence object containing the key combination(s)
        to filter.
    :param: sender is a reference to the class containing _trigger_event
        method
    """
    def __init__(self, sequence: QKeySequence, sender):
        super().__init__()
        self.sender = sender
        self.sequence = sequence

    def eventFilter(self, object, event):
        """
        Event capturing method.

        When QSKeySequence is matched the super class
        **_triggered_event** method is called with the key sequence, **it is
        assumed that parent class implements this method**, and the further
        handling of the compliting keypress  event is prevented when sequence
        is matched.
        """
        if event.type() == QEvent.KeyPress and not event.isAutoRepeat():
            if event.matches(self.sequence):
                logging.info("nom nom nom eating a key sequence: "
                             + str(self.sequence))
                self.sender._trigger_event(self.sequence)
                return True
        return super().eventFilter(object, event)
