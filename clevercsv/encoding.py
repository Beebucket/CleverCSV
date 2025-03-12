# -*- coding: utf-8 -*-

"""Functionality to detect file encodings

Author: G.J.J. van den Burg
License: See the LICENSE file

This file is part of CleverCSV.

"""

from typing import Optional

import charset_normalizer
from ._types import _OpenFile


def get_encoding(filename: _OpenFile) -> Optional[str]:
    """Get the encoding of the file

    This function uses the chardet package for detecting the encoding of a
    file.

    Parameters
    ----------
    filename: str
        Path to a file

    Returns
    -------
    encoding: str
        Encoding of the file.
    """
    with open(filename, "rb") as fid:
        best = charset_normalizer.from_fp(fid).best()
    return best.encoding if best else None
