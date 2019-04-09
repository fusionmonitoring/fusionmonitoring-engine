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
import signal
from subprocess import Popen, PIPE
from fusionsupervision import common

class Poller():
    """Run the checks sent by the scheduler and return the result to it"""

    checks = []
    loop_time_ms = 500

    def __init__(self, init_zmq=True):
        self.zmq_enable = init_zmq
        if init_zmq:
            self.socket_poller = common.create_zmq_publisher(28203)
            self.socket_scheduler = common.create_zmq_subscriver(28202, "checks_result")

    def start(self):
        """Start running the scheduler"""
        run = True
        while run:
            start = time.time() * 1000
            self.run_loop()
            # TODO manage SIGTERM
            # wait if too fast running
            diff = (time.time() * 1000) - start
            print(diff)
            if diff < self.loop_time_ms:
                time.sleep((self.loop_time_ms - diff) / 1000)

    def run_loop(self):
        """Run loop to manage checks"""
        now = time.time()
        # zeromq, get checks from scheduler
        new_checks = self.zeromq_get_checks()
        # manage time_poller_received
        new_checks = list(map(lambda x: self.set_time_poller_received(x, now), new_checks))
        # Merge received checks with current checks
        self.checks = self.checks + new_checks
        # run new checks
        self.checks = list(map(lambda x: self.run_new_checks(x, now), self.checks))
        # check running checks for checks finished
        now = time.time()
        self.checks = list(map(lambda x: self.manage_running_checks(x, now), self.checks))
        # manage timeout checks
        self.checks = list(map(lambda x: self.manage_timeout_checks(x, now), self.checks))
        # TODO zeromq, return check results for checks finished to scheduler
        if self.zmq_enable:
            common.zmq_send(self.socket_poller, "checks_result", list(filter(lambda x: x['time_poller_finish'] > 0.0, self.checks)))
        # delete checks finished
        self.checks = list(filter(lambda x: x['time_poller_finish'] == 0.0, self.checks))

    def zeromq_get_checks(self):
        """Get list of checks from scheduler through zeromq"""
        if not self.zmq_enable:
            return []
        return common.zmq_receive(self.socket_scheduler)

    @staticmethod
    def run_new_checks(check, now):
        """Run command for commands not yet running"""
        if check['running_process'] is None:
            cmd = [check['command']]
            args = check['command_args'].split()
            check['running_process'] = Popen(cmd + args, stdout=PIPE, stderr=PIPE)
            check['time_poller_run'] = now
        return check

    @staticmethod
    def manage_running_checks(check, now):
        """Manage the checks finished to run and get information"""
        retcode = check['running_process'].poll()
        if retcode is not None:
            check['time_poller_finish'] = now
            check['return_code'] = retcode
            stdout, stderr = check['running_process'].communicate()
            spl_out = stdout.decode().split("|")
            check['output'] = spl_out[0].strip()
            if len(spl_out) == 2:
                check['perf_data'] = spl_out[1].strip()
            check['running_process'] = None
        return check

    ############################################################
    ###################### PURE FUNCTIONS ######################
    ############################################################

    @staticmethod
    def manage_timeout_checks(check, now):
        """If the check is too long, stop it"""
        if check['time_poller_finish'] > 0.0:
            return check
        if (check['time_poller_run'] + check['timeout']) < now:
            check['time_poller_finish'] = now
            #check['return_code'] = retcode
            check['output'] = 'timeout'
            check['running_process'] = None
        return check

    @staticmethod
    def set_time_poller_received(x, now):
        """Set date of received check"""
        x['time_poller_received'] = now
        return x
