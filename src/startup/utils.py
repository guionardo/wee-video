"""Startup utilities"""

import os
import tempfile
from typing import Tuple


def folder_exists_and_is_writeable(folder_name) -> Tuple[bool, str]:
    """Returns success and message"""
    if not os.path.isdir(folder_name):
        return False, f'folder not found "{folder_name}"'
    try:
        with tempfile.NamedTemporaryFile(
                mode='w',
                dir=folder_name,
                delete=True) as tmp:
            tmp.write('testing')
        return True, ''

    except PermissionError:
        return False, f'folder "{folder_name}" is not writeble'
