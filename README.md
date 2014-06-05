
# Definator

## Plan and description

With **Definator** you will be able to quickly save terms and write up
definition for them. It should support cross-referencing the terms and also
enable attachment of media to the definition texts (mainly images is needed). It
is also a plan to save the data in such a form, that a definition project can be
browsed in a web browser. It is supposed to use
[PyQt 5](http://www.riverbankcomputing.co.uk/software/pyqt/intro)
and
[Qt 5](http://qt-project.org/qt5).
The definition area is planned to be implemented using
[Qt WebKit](http://qt-project.org/doc/qt-5/qtwebkit-index.html)
module and at least one custom built qt-module is to be done for listing of
terms and cross references between them.  App is mainly developed on linux and
as such it should be simplest to run on linux. Binaries for different operation
systems could be achieved by using
[pyqtdeploy](http://www.riverbankcomputing.com/software/pyqtdeploy/),
which will be looked into at some point.

* Resources:
    * [QML intro](http://qt-project.org/doc/qt-5/qmlapplications.html)
    * [PyQT and QML](http://pyqt.sourceforge.net/Docs/PyQt5/qml.html)
    * [Making a QML component](http://doc-snapshot.qt-project.org/qtcreator-2.8/quick-components.html)

##Planning

[Pencil](http://pencil.evolus.vn/) mocups for "main" -window, "add term" -window and "term reference map" -window [here](https://github.com/aparaatti/definator/tree/master/mockups). For PlantUml models click [here](https://github.com/aparaatti/definator/tree/master/models).

## Licensing

**Definator** is licensed **[GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt)**, which
is in line with the [Qt 5](http://qt-project.org/doc/qt-5/licensing.html) and [PyQt 5](http://www.riverbankcomputing.co.uk/software/pyqt/license) licensing options.

## Context

The app is developed as a part of
[graphical UI programming course TIEA212](http://appro.mit.jyu.fi/gko/) (2014)
at the University of Jyväskylä. It is also developed to scratch an itch and for
fun.

Creator Niko Humalamäki (nikohuma at gmail.com).
