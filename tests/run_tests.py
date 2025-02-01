###############################################################################
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#          Ján Osuský <jan.osusky@iblsoft.com>
#
# Copyright (c) 2025 Tom Kralidis
# Copyright (c) 2022 Government of Canada
# Copyright (c) 2020 IBL Software Engineering spol. s r. o.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

import json
import os
import unittest

from pywcmp.ets import WMOCoreMetadataProfileTestSuite2
from pywcmp.wcmp2.kpi import (
    calculate_grade, WMOCoreMetadataProfileKeyPerformanceIndicators)
from pywcmp.util import is_valid_created_datetime, parse_wcmp


def get_test_file_path(filename):
    """helper function to open test file safely"""

    if os.path.isfile(filename):
        return filename
    else:
        return f'tests/{filename}'


class WCMP2ETSTest(unittest.TestCase):
    """WCMP2 ETS tests of tests"""

    def setUp(self):
        """setup test fixtures, etc."""
        pass

    def tearDown(self):
        """return to pristine state"""
        pass

    def test_pass(self):
        """Simple tests for a passing record"""

        with open(get_test_file_path('data/wcmp2-passing.json')) as fh:
            data = json.load(fh)

        ts = WMOCoreMetadataProfileTestSuite2(data)
        results = ts.run_tests()

        self.assertEqual(results['report_type'], 'ets')
        self.assertEqual(results['metadata_id'], data['id'])

        codes = [r['code'] for r in results['tests']]

        self.assertEqual(codes.count('FAILED'), 0)
        self.assertEqual(codes.count('PASSED'), 12)
        self.assertEqual(codes.count('SKIPPED'), 0)

    def test_centre_id(self):
        """Simple tests for a centre-id validation"""

        with open(get_test_file_path('data/wcmp2-passing-test-centre-id.json')) as fh:  # noqa
            ts = WMOCoreMetadataProfileTestSuite2(json.load(fh))
            results = ts.run_tests()

            codes = [r['code'] for r in results['tests']]

            self.assertEqual(codes.count('FAILED'), 0)
            self.assertEqual(codes.count('PASSED'), 12)
            self.assertEqual(codes.count('SKIPPED'), 0)

        with open(get_test_file_path('data/wcmp2-failing-invalid-centre-id.json')) as fh:  # noqa
            ts = WMOCoreMetadataProfileTestSuite2(json.load(fh))
            results = ts.run_tests()

            codes = [r['code'] for r in results['tests']]

            self.assertEqual(codes.count('FAILED'), 1)
            self.assertEqual(codes.count('PASSED'), 11)
            self.assertEqual(codes.count('SKIPPED'), 0)

    def test_fail(self):
        """Simple tests for a failing record"""

        with open(get_test_file_path('data/wcmp2-failing.json')) as fh:
            record = json.load(fh)
            ts = WMOCoreMetadataProfileTestSuite2(record)
            results = ts.run_tests()

            codes = [r['code'] for r in results['tests']]

            self.assertEqual(codes.count('FAILED'), 3)
            self.assertEqual(codes.count('PASSED'), 9)
            self.assertEqual(codes.count('SKIPPED'), 0)

            with self.assertRaises(ValueError):
                ts.run_tests(fail_on_schema_validation=True)

    def test_fail_created_none(self):
        """Simple tests for a failing record with an invalid creation date"""

        with open(get_test_file_path('data/wcmp2-failing-created-none.json')) as fh:  # noqa
            record = json.load(fh)
            ts = WMOCoreMetadataProfileTestSuite2(record)
            results = ts.run_tests()

            codes = [r['code'] for r in results['tests']]

            self.assertEqual(codes.count('FAILED'), 1)
            self.assertEqual(codes.count('PASSED'), 11)
            self.assertEqual(codes.count('SKIPPED'), 0)

    def test_fail_invalid_link_channel_wis2_topic(self):
        """
        Simple tests for a failing record with an invalid
        link channel WIS2 topic
        """

        with open(get_test_file_path('data/wcmp2-failing-invalid-link-channel-wis2-topic.json')) as fh:  # noqa
            record = json.load(fh)
            ts = WMOCoreMetadataProfileTestSuite2(record)
            results = ts.run_tests()

            codes = [r['code'] for r in results['tests']]

            self.assertEqual(codes.count('FAILED'), 1)
            self.assertEqual(codes.count('PASSED'), 11)
            self.assertEqual(codes.count('SKIPPED'), 0)

    def test_fail_invalid_identifier_space(self):
        """
        Simple tests for a failing record with an invalid
        identifier (space in local identifier)
        """

        with open(get_test_file_path('data/wcmp2-failing-invalid-identifier-space.json')) as fh:  # noqa
            record = json.load(fh)
            ts = WMOCoreMetadataProfileTestSuite2(record)
            results = ts.run_tests()

            codes = [r['code'] for r in results['tests']]

            self.assertEqual(codes.count('FAILED'), 1)
            self.assertEqual(codes.count('PASSED'), 11)
            self.assertEqual(codes.count('SKIPPED'), 0)

    def test_fail_invalid_identifier_empty(self):
        """
        Simple tests for a failing record with an invalid
        identifier (empty local identifier)
        """

        with open(get_test_file_path('data/wcmp2-failing-invalid-identifier-empty.json')) as fh:  # noqa
            record = json.load(fh)
            ts = WMOCoreMetadataProfileTestSuite2(record)
            results = ts.run_tests()

            codes = [r['code'] for r in results['tests']]

            self.assertEqual(codes.count('FAILED'), 1)
            self.assertEqual(codes.count('PASSED'), 11)
            self.assertEqual(codes.count('SKIPPED'), 0)

    def test_fail_invalid_geometry_range(self):
        """
        Simple tests for a failing record with an invalid
        geometry (values out of WGS84 range)
        """

        with open(get_test_file_path('data/wcmp2-failing-invalid-geometry-range.json')) as fh:  # noqa
            record = json.load(fh)
            ts = WMOCoreMetadataProfileTestSuite2(record)
            results = ts.run_tests()

            codes = [r['code'] for r in results['tests']]

            self.assertEqual(codes.count('FAILED'), 1)
            self.assertEqual(codes.count('PASSED'), 11)
            self.assertEqual(codes.count('SKIPPED'), 0)


class WCMP2KPITest(unittest.TestCase):
    """WCMP KPI tests of tests"""

    def setUp(self):
        """setup test fixtures, etc."""
        pass

    def tearDown(self):
        """return to pristine state"""
        pass

    def test_kpi_evaluate(self):
        """Tests for KPI evaluation"""

        file_ = 'data/wcmp2-passing.json'
        with open(get_test_file_path(file_)) as fh:
            data = json.load(fh)

        kpis = WMOCoreMetadataProfileKeyPerformanceIndicators(data)

        results = kpis.evaluate()

        self.assertEqual(results['report_type'], 'kpi')
        self.assertEqual(results['metadata_id'], data['id'])

        self.assertEqual(results['summary']['total'], 32)
        self.assertEqual(results['summary']['score'], 32)
        self.assertEqual(results['summary']['percentage'], 100)
        self.assertEqual(results['summary']['grade'], 'A')

    def test_calculate_grade(self):
        self.assertEqual(calculate_grade(98), 'A')
        self.assertEqual(calculate_grade(77), 'B')
        self.assertEqual(calculate_grade(66), 'B')
        self.assertEqual(calculate_grade(52), 'C')
        self.assertEqual(calculate_grade(41), 'D')
        self.assertEqual(calculate_grade(33), 'E')
        self.assertIsNone(calculate_grade(None))

        with self.assertRaises(ValueError):
            calculate_grade(101)


class WCMPUtilTest(unittest.TestCase):
    """WCMP utility tests"""

    def setUp(self):
        """setup test fixtures, etc."""
        pass

    def tearDown(self):
        """return to pristine state"""
        pass

    def test_parse_wcmp(self):
        """test invalid input"""

        with self.assertRaises(RuntimeError):
            file_ = 'data/not-json.csv'
            with open(get_test_file_path(file_)) as fh:
                _ = parse_wcmp(fh.read())

        file_ = 'data/wcmp2-passing.json'
        with open(get_test_file_path(file_)) as fh:
            _ = parse_wcmp(fh.read())

    def test_is_valid_created_datetime(self):
        """test for valid/accepted RFC3339 datetimes"""

        self.assertTrue(is_valid_created_datetime('2024-08-09T14:29:22Z'))
        self.assertTrue(is_valid_created_datetime('2024-08-09T14:29:22.12Z'))
        self.assertTrue(is_valid_created_datetime('2024-08-09T14:29:22+0400'))
        self.assertTrue(is_valid_created_datetime('2024-08-09T14:29:22+04:00'))


if __name__ == '__main__':
    unittest.main()
