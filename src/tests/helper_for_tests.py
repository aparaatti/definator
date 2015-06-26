#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tempfile

__author__ = 'Niko Humalamäki'

from pathlib import Path
import shutil
import tempfile

TMP = Path('/tmp/test-generated-project/')

def make_tmp_project():
    if Path(TMP).exists():
        shutil.rmtree(str(TMP))
    Path(TMP).mkdir()
    if not Path(TMP).exists():
        raise FileNotFoundError("Path doesn't exist: %s." % TMP)

def make_tmp_file(prefix):
    file = tempfile.NamedTemporaryFile(suffix="txt", prefix=prefix,
                                       delete=False)
    file.close()
    return file.name