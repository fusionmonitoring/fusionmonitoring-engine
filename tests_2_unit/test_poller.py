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
from subprocess import Popen, PIPE
import unittest2
from fusionsupervision.modules.poller import Poller

class PollerTest(unittest2.TestCase):
    """Test single functions of the poller"""

    def test_zeromq_get_checks(self):
        print("TODO")

    def test_run_new_checks__newcheck(self):
        """Test function run_new_checks where the check not yet running"""
        poller = Poller(False)
        now = 1554646001.3
        check = {
            'command': "/usr/local/libexec/nagios/check_http",
            'command_args': "-H www.google.com",
            'timeout': 30,
            'time_creation': 1554645956.5512931,
            'time_poller_received': 1554645958.3439,
            'time_poller_run': 0.0,
            'time_poller_finish': 0.0,
            'time_scheduler_received': 0.0,
            'service': "b5748e89457834",
            'running_process': None,
            'return_code': None,
            'output': "",
            'perf_data': ""
        }
        data_reference = {
            'command': "/usr/local/libexec/nagios/check_http",
            'command_args': "-H www.google.com",
            'timeout': 30,
            'time_creation': 1554645956.5512931,
            'time_poller_received': 1554645958.3439,
            'time_poller_run': 1554646001.3,
            'time_poller_finish': 0.0,
            'time_scheduler_received': 0.0,
            'service': "b5748e89457834",
            'running_process': None,
            'return_code': None,
            'output': "",
            'perf_data': ""
        }
        data = poller.run_new_checks(check, now)
        self.assertIsNotNone(data['running_process'])
        data_reference['running_process'] = data['running_process']
        self.assertListEqual(["/usr/local/libexec/nagios/check_http", "-H", "www.google.com"], data_reference['running_process'].args)
        self.assertDictEqual(data_reference, data)

    def test_run_new_checks__runningcheck(self):
        """Test function run_new_checks where the check is running"""
        poller = Poller(False)
        now = 1554646001.3
        check = {
            'command': "/usr/local/libexec/nagios/check_http",
            'command_args': "-H www.google.com",
            'timeout': 30,
            'time_creation': 1554645956.5512931,
            'time_poller_received': 1554645958.3439,
            'time_poller_run': 1554646001.3,
            'time_poller_finish': 0.0,
            'time_scheduler_received': 0.0,
            'service': "b5748e89457834",
            'running_process': object,
            'return_code': None,
            'output': "",
            'perf_data': ""
        }
        data = poller.run_new_checks(check, now)
        self.assertDictEqual(check, data)

    def test_manage_running_checks__running(self):
        """Test function manage_running_checks, check is running"""
        poller = Poller(False)
        now = 1554646002.5
        check = {
            'command': "/usr/local/libexec/nagios/check_http",
            'command_args': "-H www.google.com",
            'timeout': 30,
            'time_creation': 1554645956.5512931,
            'time_poller_received': 1554645958.3439,
            'time_poller_run': 1554646001.3,
            'time_poller_finish': 0.0,
            'time_scheduler_received': 0.0,
            'service': "b5748e89457834",
            'running_process': Popen(["sleep", "5"], stdout=PIPE, stderr=PIPE),
            'return_code': None,
            'output': "",
            'perf_data': ""
        }
        data = poller.manage_running_checks(check, now)
        self.assertDictEqual(check, data)

    def test_manage_running_checks__finish_running(self):
        """Test function manage_running_checks, check has finished to run"""
        poller = Poller(False)
        now = 1554646002.5
        check = {
            'command': "/usr/local/libexec/nagios/check_http",
            'command_args': "-H www.google.com",
            'timeout': 30,
            'time_creation': 1554645956.5512931,
            'time_poller_received': 1554645958.3439,
            'time_poller_run': 1554646001.3,
            'time_poller_finish': 0.0,
            'time_scheduler_received': 0.0,
            'service': "b5748e89457834",
            'running_process': Popen(["echo", "549876456"], stdout=PIPE, stderr=PIPE),
            'return_code': None,
            'output': "",
            'perf_data': ""
        }
        data_reference = {
            'command': "/usr/local/libexec/nagios/check_http",
            'command_args': "-H www.google.com",
            'timeout': 30,
            'time_creation': 1554645956.5512931,
            'time_poller_received': 1554645958.3439,
            'time_poller_run': 1554646001.3,
            'time_poller_finish': 1554646002.5,
            'time_scheduler_received': 0.0,
            'service': "b5748e89457834",
            'running_process': None,
            'return_code': 0,
            'output': "549876456",
            'perf_data': ""
        }
        time.sleep(0.2)
        data = poller.manage_running_checks(check, now)
        self.assertDictEqual(data_reference, data)

    def test_manage_running_checks__finish_running__perfdata(self):
        """Test function manage_running_checks, check has finished to run + perfdata"""
        poller = Poller(False)
        now = 1554646002.5
        check = {
            'command': "/usr/local/libexec/nagios/check_http",
            'command_args': "-H www.google.com",
            'timeout': 30,
            'time_creation': 1554645956.5512931,
            'time_poller_received': 1554645958.3439,
            'time_poller_run': 1554646001.3,
            'time_poller_finish': 0.0,
            'time_scheduler_received': 0.0,
            'service': "b5748e89457834",
            'running_process': Popen(["echo", "549876456|perftest"], stdout=PIPE, stderr=PIPE),
            'return_code': None,
            'output': "",
            'perf_data': ""
        }
        data_reference = {
            'command': "/usr/local/libexec/nagios/check_http",
            'command_args': "-H www.google.com",
            'timeout': 30,
            'time_creation': 1554645956.5512931,
            'time_poller_received': 1554645958.3439,
            'time_poller_run': 1554646001.3,
            'time_poller_finish': 1554646002.5,
            'time_scheduler_received': 0.0,
            'service': "b5748e89457834",
            'running_process': None,
            'return_code': 0,
            'output': "549876456",
            'perf_data': "perftest"
        }
        time.sleep(0.2)
        data = poller.manage_running_checks(check, now)
        self.assertDictEqual(data_reference, data)
