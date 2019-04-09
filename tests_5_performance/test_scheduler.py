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
import resource
import zmq
import unittest2
from fusionsupervision.modules.scheduler import Scheduler

class PerfTest(unittest2.TestCase):


    def test_loop(self):
        services = {}
        id = 5017786799000000
        for i in range(100000):
            id += 1
            services[str(id)] = {
                "ls_grafana": True,
                "business_impact_modulations": [],
                "labels": [],
                "action_url": "",
                "low_flap_threshold": 25,
                "process_perf_data": True,
                "business_rule_downtime_as_ack": False,
                "_realm": "59a926c494db6e01fa7a0551",
                "display_name": "",
                "notification_interval": 60,
                "ls_execution_time": 13.3346421719,
                "failure_prediction_enabled": False,
                "ls_last_time_warning": 0,
                "retry_interval": 1,
                "snapshot_enabled": False,
                "event_handler_enabled": False,
                "ls_acknowledged": False,
                "_template_fields": [],
                "high_flap_threshold": 50,
                "notifications_enabled": True,
                "aggregation": "",
                "freshness_threshold": 0,
                "time_to_orphanage": 300,
                "name": "".join(["test", str(i)]),
                "notes": "",
                "ls_last_notification": 0,
                "parallelize_check": True,
                "merge_host_users": False,
                "custom_views": [],
                "active_checks_enabled": True,
                "ls_max_attempts": 0,
                "hostgroups": [],
                "reactionner_tag": "",
                "is_volatile": False,
                "ls_last_state": "OK",
                "ls_last_time_unknown": 1537648779,
                "default_value": "",
                "ls_attempt": 1,
                "resultmodulations": [],
                "icon_image": "",
                "stalking_options": [],
                "_sub_realm": True,
                "ls_long_output": "",
                "macromodulations": [],
                "ls_state_id": 0,
                "business_rule_host_notification_options": ["d", "u", "r", "f", "s"],
                "ls_impact": False,
                "_is_template": False,
                "definition_order": 100,
                "tags": [],
                "snapshot_criteria": ["w", "c", "x"],
                "ls_latency": 0.4351449013,
                "_created": "Sat, 07 Apr 2018 03:08:15 GMT",
                "ls_current_attempt": 0,
                "ls_grafana_panelid": 2,
                "icon_set": "",
                "business_impact": 2,
                "max_check_attempts": 3,
                "business_rule_service_notification_options": ["w", "u", "c", "r", "f", "s"],
                "ls_downtimed": False,
                "escalations": [],
                "ls_last_time_ok": 1554304045,
                "ls_next_check": 1554304091,
                "flap_detection_options": ["o", "w", "c", "u", "x"],
                "ls_last_check": 1554304031,
                "_overall_state_id": 0,
                "host_dependency_enabled": True,
                "_links": {
                    "self": {
                        "href": "service/5ac8361f94db6e091a7f1af8",
                        "title": "Service"
                    }
                },
                "ls_last_time_critical": 1554300192,
                "first_notification_delay": 0,
                "_templates": [],
                "notification_options": ["w", "u", "c", "r", "f", "s", "x"],
                "event_handler_args": "",
                "trigger_broker_raise_enabled": False,
                "event_handler": None,
                "check_command_args": "support.dcsit-group.com",
                "ls_last_state_changed": 1554300282,
                "imported_from": "unknown",
                "initial_state": "x",
                "ls_state": "OK",
                "check_command": "59a94f8d94db6e01fb7a0583",
                "passive_checks_enabled": True,
                "check_interval": 1,
                "notes_url": "",
                "_etag": "aa81bb700adf92e842c2fe1a753af57ffb3db530",
                "check_freshness": False,
                "snapshot_interval": 5,
                "icon_image_alt": "",
                "_templates_from_host_template": False,
                "duplicate_foreach": "",
                "ls_output": "CUCUMBER OK - Critical: 0, Warning: 0, 12 okay",
                "ls_passive_check": False,
                "ls_last_state_type": "HARD",
                "ls_perf_data": "passed=12; failed=0; nosteps=0; total=12; time=11",
                "alias": "",
                "freshness_state": "x",
                "trending_policies": [],
                "ls_last_hard_state_changed": 1554300282,
                "flap_detection_enabled": True,
                "users": [],
                "business_rule_smart_notifications": False,
                "ls_acknowledgement_type": 1,
                "customs": {},
                "usergroups": [],
                "trigger_name": "",
                "service_dependencies": [],
                "_updated": "Sat, 07 Apr 2018 03:16:55 GMT",
                "checkmodulations": [],
                "poller_tag": "",
                "ls_last_time_unreachable": 0,
                "ls_state_type": "HARD",
                "_id": str(id),
                "business_rule_output_template": "",
                "check_period": "59a94f8d94dbfe563801fb7a0583",
                "notification_period": "59a94f8d94dbfe563801fb7a0583",
            }
        sched = Scheduler(services)

        # connect zmq
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:5666")
        socket.setsockopt_string(zmq.SUBSCRIBE, "poller-run-checks")

        print("=================== loop ===================")
        start = time.time() * 1000
        sched.run_loop()
        print("time: ", (time.time()*1000) - start)
        print("memory (in Mo): ", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000)

        print("=================== loop ===================")
        start = time.time() * 1000
        sched.run_loop()
        print("time: ", (time.time()*1000) - start)
        print("memory (in Mo): ", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000)
        print("=================== loop ===================")
        start = time.time() * 1000
        sched.run_loop()
        print("time: ", (time.time()*1000) - start)
        print("memory (in Mo): ", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000)
        print("=================== loop ===================")
        start = time.time() * 1000
        sched.run_loop()
        print("time: ", (time.time()*1000) - start)
        print("memory (in Mo): ", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000)
        print("=================== loop ===================")
        start = time.time() * 1000
        sched.run_loop()
        print("time: ", (time.time()*1000) - start)
        print("memory (in Mo): ", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000)
        print("=================== loop ===================")
        start = time.time() * 1000
        sched.run_loop()
        print("time: ", (time.time()*1000) - start)
        print("memory (in Mo): ", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000)
        print("=================== loop ===================")
        start = time.time() * 1000
        sched.run_loop()
        print("time: ", (time.time()*1000) - start)
        print("memory (in Mo): ", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000)
        print("=================== loop ===================")
        start = time.time() * 1000
        sched.run_loop()
        print("time: ", (time.time()*1000) - start)
        print("memory (in Mo): ", (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/1000)
        assert 1 == 1000
