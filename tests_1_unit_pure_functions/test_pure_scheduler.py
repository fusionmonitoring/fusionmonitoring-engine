#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2019: FusionSupervision team, see AUTHORS.md file for contributors
#
# This file is part of FusionSupervision engine.
#
# FusionSupervision is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FusionSupervision is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with FusionSupervision engine.  If not, see <http://www.gnu.org/licenses/>.
#

import time
import unittest2
from fusionsupervision.modules.scheduler import Scheduler

class SchedulerPureTest(unittest2.TestCase):
    """Test pure functions of the scheduler"""

    def test_filter_to_run(self):
        """Test function filter_to_run"""
        sched = Scheduler({}, {"services":{}}, False)
        now = time.time()
        # Test obsolete period
        obsolete = {
            'fs_check_period': {
                'start': 10000.0,
                'end': 100000.0
            },
            'fs_check': {
                'check_sent': False,
                'date_sent': 0.0
            },
            '_id': '507f1f77bcf86cd799439021',
            'ls_next_check': 20000.0
        }
        data = sched.filter_to_run(obsolete, now)
        self.assertFalse(data)
        # Test in period
        in_period = {
            'fs_check_period': {
                'start': (now - 10000.0),
                'end': (now + 20000.0),
            },
            'fs_check': {
                'check_sent': False,
                'date_sent': 0.0
            },
            '_id': '507f1f77bcf86cd799439022',
            'ls_next_check': (now - 10)
        }
        data_in = sched.filter_to_run(in_period, now)
        self.assertDictEqual(in_period, data_in)
        # Test period in future
        future = {
            'fs_check_period': {
                'start': (time.time() + 10000.0),
                'end': (time.time() + 20000.0),
            },
            'fs_check': {
                'check_sent': False,
                'date_sent': 0.0
            },
            '_id': '507f1f77bcf86cd799439023',
            'ls_next_check': (now - 10)
        }
        data_future = sched.filter_to_run(future, now)
        self.assertFalse(data_future)

        # TODO add test to manage next_check

    def test_create_check(self):
        """Test function create_check"""
        print("TODO")

    def test_mapping_dict_list_indexes(self):
        """Test function dict_list_indexes"""
        sched = Scheduler({}, {"services":{}}, False)
        data_list = [
            {
                "_id": "11",
                "name": "test1"
            },
            {
                "_id": "13",
                "name": "test3"
            },
            {
                "_id": "12",
                "name": "test2"
            },
        ]
        data_reference = {
            "11": 0,
            "13": 1,
            "12": 2
        }
        mapping = sched.mapping_dict_list_indexes(data_list)
        self.assertDictEqual(data_reference, mapping)

    def test_calculate_next_check_planned_SOFT(self):
        """Test funtion calculate_next_check_planned with service in SOFT"""
        sched = Scheduler({}, {"services":{}}, False)
        service_prop = {
            "_id": "13",
            "name": "test3",
            "retry_interval": 30,
            "check_interval": 90
        }
        service_state = {
            "_id": "13",
            "fs_check": {
                "check_sent": False,
                "date_sent": 1554584050.0
            },
            'ls_current_attempt': 1,
            "ls_next_check": 1554584050.0
        }
        data_reference = {
            "_id": "13",
            "fs_check": {
                "check_sent": False,
                "date_sent": 1554584050.0
            },
            'ls_current_attempt': 1,
            "ls_next_check": 1554584080.0
        }
        data = sched.calculate_next_check_planned(service_state, service_prop)
        self.assertDictEqual(data_reference, data)

    def test_calculate_next_check_planned_HARD(self):
        """Test funtion calculate_next_check_planned with service in HARD"""
        sched = Scheduler({}, {"services":{}}, False)
        service_prop = {
            "_id": "13",
            "name": "test3",
            "retry_interval": 30,
            "check_interval": 90
        }
        service_state = {
            "_id": "13",
            "fs_check": {
                "check_sent": False,
                "date_sent": 1554584050.0
            },
            'ls_current_attempt': 0,
            "ls_next_check": 1554584050.0
        }
        data_reference = {
            "_id": "13",
            "fs_check": {
                "check_sent": False,
                "date_sent": 1554584050.0
            },
            'ls_current_attempt': 0,
            "ls_next_check": 1554584140.0
        }
        data = sched.calculate_next_check_planned(service_state, service_prop)
        self.assertDictEqual(data_reference, data)

    def test_update_service_freshness_expired__nomanageexpired(self):
        """Test function update_service_freshness_expired, service not expired"""
        sched = Scheduler({}, {"services":{}}, False)
        service = {
            "_id": "13",
            "name": "test3",
            "freshness_state": "CRITICAL",
            "ls_state": "OK"
        }
        freshnessed_services = ["11", "14"]
        data = sched.update_service_freshness_expired(service, freshnessed_services)
        self.assertDictEqual(service, data)

    def test_update_service_freshness_expired__manageexpired(self):
        """Test function update_service_freshness_expired, service expired"""
        sched = Scheduler({}, {"services":{}}, False)
        service = {
            "_id": "13",
            "name": "test3",
            "freshness_state": "CRITICAL",
            "ls_state": "OK"
        }
        freshnessed_services = ["11", "14", "13"]
        data_reference = {
            "_id": "13",
            "name": "test3",
            "freshness_state": "CRITICAL",
            "ls_state": "CRITICAL"
        }
        data = sched.update_service_freshness_expired(service, freshnessed_services)
        self.assertDictEqual(data_reference, data)

    def test_generate_freshnessed_services__notolder(self):
        """Test function generate_freshnessed_services, last_check not older"""
        sched = Scheduler({}, {"services":{}}, False)
        service = {
            "_id": "13",
            "name": "test3",
            "ls_last_check": 1554584050.0,
            "freshness_threshold": 3600
        }
        data = sched.generate_freshnessed_services(service, 1554584150.0)
        self.assertFalse(data)

    def test_generate_freshnessed_services__older(self):
        """Test function generate_freshnessed_services, last_check older"""
        sched = Scheduler({}, {"services":{}}, False)
        service = {
            "_id": "13",
            "name": "test3",
            "ls_last_check": 1554584050.0,
            "freshness_threshold": 3600
        }
        data = sched.generate_freshnessed_services(service, 1554588050.0)
        self.assertEqual("13", data)

    def test_update_field_with_another(self):
        print("TODO")