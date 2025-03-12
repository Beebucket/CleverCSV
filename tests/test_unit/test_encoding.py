# -*- coding: utf-8 -*-

"""Unit tests for encoding detection

Note that we're not necessarily testing how accurate the charset_normalizer
library is. We're testing that our encoding detection function works.

Author: G.J.J. van den Burg
License: See the LICENSE file.

This file is part of CleverCSV.

"""

import os
import tempfile
import unittest

from dataclasses import dataclass

from typing import Any
from typing import List

from clevercsv._types import AnyPath
from clevercsv.encoding import get_encoding
from clevercsv.write import writer


class EncodingTestCase(unittest.TestCase):
    @dataclass(frozen=True)
    class Instance:
        # Data to write to a file
        table: List[List[Any]]

        # Source encoding to use when writing
        source_encoding: str

        # Acceptable encodings charset_normalizer may report
        expected_encodings: set[str]

    cases: List[Instance] = [
        Instance(
            table=[["Å", "B", "C"], [1, 2, 3], [4, 5, 6]],
            source_encoding="ISO-8859-1",
            expected_encodings={"ISO-8859-1", "KOI8-R"},
        ),
        Instance(
            table=[["A", "B", "C"], [1, 2, 3], [4, 5, 6]],
            source_encoding="ascii",
            expected_encodings={"ascii"},
        ),
        Instance(
            table=[["亜唖", "娃阿", "哀愛"], [1, 2, 3], ["挨", "姶", "葵"]],
            source_encoding="ISO-2022-JP",
            expected_encodings={"ISO-2022-JP"},
        ),
    ]

    def setUp(self) -> None:
        self._tmpfiles: List[AnyPath] = []

    def tearDown(self) -> None:
        for f in self._tmpfiles:
            os.unlink(f)

    def _build_file(self, table: List[List[str]], encoding: str) -> str:
        tmpfd, tmpfname = tempfile.mkstemp(
            prefix="ccsv_",
            suffix=".csv",
        )
        tmpfp = os.fdopen(tmpfd, "w", newline=None, encoding=encoding)
        w = writer(tmpfp, dialect="excel")
        w.writerows(table)
        tmpfp.close()
        self._tmpfiles.append(tmpfname)
        return tmpfname

    def test_encoding(self) -> None:
        for case in self.cases:
            with self.subTest(encoding=case.source_encoding):
                tmpfname = self._build_file(case.table, case.source_encoding)
                detected = get_encoding(tmpfname)
                self.assertIn(detected, case.expected_encodings)


if __name__ == "__main__":
    unittest.main()
