#TODO and ideas
## All menu items:

- settings
    - language
    - remember opened projects
    - load last opened project on startup
    - colors of files in linked things

## Later:

- Generic tag class, that can be used to define a tag and html
  representation for it.
- Term browser in side pane (QDockWidget).
- File copy doesn't work on windows (?)
- Maybe open terms in tabs, with editor/term --> proper undo/redo
- Writing of unit tests
- Add list of synonymous terms to a term.
- Show tags bold on term editor, show references to images bold on term
  display
- Maybe different types of links for terms (sub term, parent term)
- Use python built in serialization/de-serialization for saving stuff
- Warn user when removing a term, that also the linked files in term folder
  will be deleted.
- Exception handler, that shows certain exception as a warning dialog
  (currently exceptions are not handled).

## RE FACTOR:

- TermDisplay to HtmlDisplay

