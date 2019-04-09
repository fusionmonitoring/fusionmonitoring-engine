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

import unittest2
from fusionsupervision.modules.poller import Poller

class PollerPureTest(unittest2.TestCase):
    """Test pure functions of the poller"""

    def test_manage_timeout_checks__notimeout(self):
        """Test function manage_timeout_checks, no in timeout period"""
        poller = Poller(False)
        now = 1554645956.5512931
        check = {
            "time_poller_finish": 0.0,
            "time_poller_run": 1554645946.5512931,
            "timeout": 30,
            "output": "",
            "running_process": "something"
        }
        data = poller.manage_timeout_checks(check, now)
        self.assertDictEqual(check, data)

    def test_manage_timeout_checks__intimeout(self):
        """Test function manage_timeout_checks, in timeout period"""
        poller = Poller(False)
        now = 1554645992.5512931
        check = {
            "time_poller_finish": 0.0,
            "time_poller_run": 1554645946.5512931,
            "timeout": 30,
            "output": "",
            "running_process": "something"
        }
        data_reference = {
            "time_poller_finish": 1554645992.5512931,
            "time_poller_run": 1554645946.5512931,
            "timeout": 30,
            "output": "timeout",
            "running_process": None
        }
        data = poller.manage_timeout_checks(check, now)
        self.assertDictEqual(data_reference, data)

    def test_set_time_poller_received(self):
        """Test function set_time_poller_received"""
        poller = Poller(False)
        now = 1554645992.5512931
        check = {
            "time_poller_received": 0.0,
            "time_poller_finish": 0.0
        }
        data_reference = {
            "time_poller_received": 1554645992.5512931,
            "time_poller_finish": 0.0
        }
        data = poller.set_time_poller_received(check, now)
        self.assertDictEqual(data_reference, data)
