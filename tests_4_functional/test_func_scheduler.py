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
from fusionsupervision import common

class SchedulerFunctionalTest(unittest2.TestCase):
    """Functional tests of the scheduler"""

    def test_active_check_run_and_runagain(self):
        """Test run check at right time and works nicely"""
        self.run_fake_poller()
        # create a service
        services = self.get_services()
        # init the scheduler
        sched = Scheduler(services)
        # runloop scheduler
        sched.run_loop()
        # return_check_executed (must return 1)
        checks_cnt = self.return_check_executed()
        self.assertEqual(1, checks_cnt)
        # runloop scheduler (manage result)
        sched.run_loop()
        # return_check_executed (must return 0)
        checks_cnt = self.return_check_executed()
        self.assertEqual(0, checks_cnt)
        # sleep 3 seconds to next check_internal
        time.sleep(3)
        # runloop scheduler
        sched.run_loop()
        # return_check_executed (must return 1)
        checks_cnt = self.return_check_executed()
        self.assertEqual(1, checks_cnt)
        # runloop scheduler (manage result)
        sched.run_loop()

    ############################################################
    #################### INTERNAL FUNCTIONS ####################
    ############################################################

    def run_fake_poller(self):
        """Run fake poller"""
        self.psocket_poller = common.create_zmq_publisher(28203)
        self.psocket_scheduler = common.create_zmq_subscriver(28202, "checks_to_run")

    def return_check_executed(self):
        """Get check on zmq and return the check completed"""
        checks = common.zmq_receive(self.psocket_scheduler)
        # modify check data
        if len(checks) == 1:
            checks[0]['time_poller_received'] = time.time()
            checks[0]['time_poller_run'] = time.time()
            checks[0]['time_poller_finish'] = time.time()
            checks[0]['return_code'] = 0
            checks[0]['output'] = "HTTP OK: HTTP/1.1 200 OK - 11916 bytes in 0.420 second response time"
            checks[0]['perf_data'] = "time=0.420222s;;;0.000000;10.000000 size=11916B;;;0"
        common.zmq_send(self.psocket_poller, "checks_result", checks)
        return len(checks)

    @staticmethod
    def get_services():
        return {
            "5cac312d192a8a3fd6dfe5f4": {
                "_id": "5cac312d192a8a3fd6dfe5f4",
                "name": "_dummy",
                "check_command": "59a94f8d94db6e01fb7a0583",
                "_realm": "5cac312d192a8a3fd6dfe5ec",
                "_sub_realm": True,
                "business_impact": 2,
                "check_period": "507f1f77bcf86cd799439011",
                "notification_period": "507f1f77bcf86cd799439011",
                "notes": "",
                "notes_url": "",
                "action_url": "",
                "tags": [],
                "customs": {},
                "location": {
                    "type": "Point",
                    "coordinates": [48.858293, 2.294601]
                },
                "parents": [],
                "ipv4": "",
                "ipv6": "",
                "initial_state": "x",
                "time_to_orphanage": 300,
                "active_checks_enabled": True,
                "check_command_args": "",
                "max_check_attempts": 1,
                "check_interval": 2,
                "retry_interval": 0,
                "passive_checks_enabled": True,
                "check_freshness": False,
                "freshness_threshold": 3600,
                "freshness_state": "x",
                "event_handler_enabled": False,
                "event_handler": None,
                "event_handler_args": "",
                "flap_detection_enabled": True,
                "flap_detection_options": ["o", "d", "x"],
                "low_flap_threshold": 25,
                "high_flap_threshold": 50,
                "process_perf_data": True,
                "notifications_enabled": True,
                "notification_options": ["d", "x", "r", "f", "s"],
                "users": [],
                "usergroups": [],
                "notification_interval": 3600,
                "first_notification_delay": 0,
                "stalking_options": [],
                "poller_tag": "",
                "reactionner_tag": "",
                "labels": [],
                "snapshot_enabled": False,
                "snapshot_criteria": ["d", "x"],
                "snapshot_interval": 300,
                "ls_state": "OK",
                "ls_state_type": "HARD",
                "ls_state_id": 3,
                "ls_acknowledged": False,
                "ls_acknowledgement_type": 1,
                "ls_downtimed": False,
                "ls_last_check": 0,
                "ls_last_state": "OK",
                "ls_last_state_type": "HARD",
                "ls_next_check": 0,
                "ls_output": "",
                "ls_long_output": "",
                "ls_perf_data": "",
                "ls_current_attempt": 0,
                "ls_latency": 0.0,
                "ls_execution_time": 0.0,
                "ls_passive_check": False,
                "ls_state_changed": 0,
                "ls_last_state_changed": 0,
                "ls_last_hard_state_changed": 0,
                "ls_last_time_up": 0,
                "ls_last_time_down": 0,
                "ls_last_time_unknown": 0,
                "ls_last_time_unreachable": 0,
                "ls_grafana": False,
                "ls_grafana_panelid": 0,
                "ls_last_notification": 0,
                "_etag": "5ec976ccbadf6634c229e7180b9583c54149dfd0",
            }
        }