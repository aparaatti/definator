# -*- coding: utf-8 -*-
#
# This file is a part of Definator (https://github.com/aparaatti/definator)
# and it is licensed under the GPLv3 (http://www.gnu.org/licenses/gpl-3.0.txt).
#
__author__ = 'aparaatti'

import os
import logging
import shutil
from pathlib import Path

def remove_file(file_path: Path):
    logging.debug('-------------------------( Removing file: ' + str(
        file_path) + '! )')
    os.remove(str(file_path))


def copy_file_to(src: Path, target: Path):
    logging.debug('-------------------------( Copying file "' + str(src) +
                  '" to "' + str(target / src.name))
    shutil.copy2(str(src), str(target / src.name))

def make_dir(dir: Path):
    logging.debug('-------------------------( Creating dir: "' + str(dir) +
                  "'.")
    os.mkdir(str(dir))