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
from functools import reduce
from fusionsupervision import common

class Scheduler():
    """Manage the items monitored

    Attributes:
        services                            The services to control / manage
        services_check                      Manage the check of each service
        service_check_period                Manage the current (or next) period where we can check the service
        service_notification_period         Manage the current (or next) period where we can send notifications
        acknowledges                        Manage the list of acknowledges
        downtimes                           Manage the list of downtimes
        zeromq_checks_to_send               Manage the list of checks to add to zeromq
        timestamp_next_recalculate_periods  store the timestamp of the next periods recalculation
        zmq_enable                          boolean to say enable or not (not enable is used when run unit tests)
    """

    # static properties
    services_prop = {}

    # dynamic properties
    services_state = {}



    services_check = {}
    service_check_period = []
    service_notification_period = []
    acknowledges = {}
    downtimes = {}
    zeromq_checks_to_send = []
    mapping_list_services = {}
    commands = {
        '59a94f8d94db6e01fb7a0583': {
            'command_line': 'check_ping',
            'timeout': 30
        }
    }
    timestamp_next_recalculate_periods = 0.0
    zmq_enable = True

    def __init__(self, config, config_data, init_zmq=True):
        """Initialize the scheduler

        config: it's the config
        config_data: it's the data config (services, commands, timeperiods...)
        """
        self.zmq_enable = init_zmq
        # Split services in static and dynamic dict
        self.services_prop = common.convert_list_in_dict(list(map(lambda x: self.map_services_prop(x), config_data['services'].values())))
        self.services_state = common.convert_list_in_dict(list(map(lambda x: self.map_services_state(x), config_data['services'].values())))
        # Get mapping service _id => list index
        self.mapping_list_services = self.mapping_dict_list_indexes(self.services_prop.values())
        # TODO Create timeperiods objects

        # get acknowledges
        # TODO acknowledges = ...
        # get downtimes
        # TODO downtimes = ...

        # init zeromq
        if init_zmq:
            self.socket_scheduler = common.create_zmq_publisher(28202)
            self.socket_poller = common.create_zmq_subscriver(28203, "checks_result")

    def start(self):
        """Start running the scheduler"""
        to_exit = False
        while not to_exit:
            self.run_loop()
            # TODO manage SIGTERM (in common class), return exit or not

    def run_loop(self, freshnessed=None):
        """run these functions to manage the scheduler"""
        if freshnessed is None:
            freshnessed = []
        now = time.time()
        # zeromq, get checks from poller
        checks = []
        if self.zmq_enable:
            checks = common.zmq_receive(self.socket_poller)
        # TODO zeromq, get acknowledges from arbiter
        # TODO zeromq, get downtimes from arbiter
        # TODO zeromq, get re-checks fro arbiter

        # recalculate periods if needed
        if self.timestamp_next_recalculate_periods < now:
            self.services_state = self.manage_service_check_period(now, self.services_state, self.services_prop)
            #self.timestamp_next_recalculate_periods = reduce(lambda x, y: x if x < y else y, list(map(lambda x: x['end'], self.manage_service_check_period)))
            self.timestamp_next_recalculate_periods = now
        # schedule new checks
        zeromq_checks_to_send, self.services_state = self.schedule_new_checks(now, self.services_prop, self.services_state, self.commands)
        # send checks to poller througth zeromq
        if self.zmq_enable:
            common.zmq_send(self.socket_scheduler, "checks_to_run", zeromq_checks_to_send)
        # TODO consume check results (and recalculate next_check_planned in services_check)
        self.services_state = self.consume_check_results(checks, self.services_state, self.services_prop)

        # calculate next check planned
        self.services_state = common.convert_list_in_dict(list(map(lambda x: self.calculate_next_check_planned(x, self.services_prop[x['_id']]), self.services_state.values())))


        # TO BE CONTINUE...

        # TODO check freshness
        #self.services = self.check_freshness(self.services, now, freshnessed)
        # regenerate freshnessed services
        #freshnessed = list(filter(lambda x: self.generate_freshnessed_services(x, now), self.services.values()))

        # TODO manage notifications
        self.manage_service_notification_period()

        # TODO clean zombies (check, actions)

    @staticmethod
    def manage_service_check_period(now, services_state, services_prop):
        """Set begin and end period of each host and service for check"""
        to_calculate = list(filter(lambda x: x['fs_check_period']['end'] < now, services_state.values()))
        all_timeperiods = list(map(lambda x: x['check_period'], services_prop.values()))
        timeperiods = list(set(all_timeperiods))
        def replace_times(x, period, value):
            #if x['period'] == period:
            #    x['start'] = value
            x['fs_check_period']['end'] = 2054408035.6778336
            return x
        for tid in timeperiods:
            #print(tid)
            # TODO get next start and end for this period
            services_state = list(map(lambda x: replace_times(x, '507f1f77bcf86cd799439011', 754368957.0), services_state.values()))
        return common.convert_list_in_dict(services_state)

    @staticmethod
    def manage_service_notification_period():
        """Set begin and end period of each host and service for notification"""
        print("todo")

    def schedule_new_checks(self, now, services_prop, services_state, commands):
        """Schedule new checks on hosts and services"""
        # get list from self.services_state who need to be scheduled and not running
        to_run = list(filter(lambda x: self.filter_to_run(x, now), services_state.values()))
        # get elements in the 2 lists (to_run and service)
        services_to_check = common.convert_list_in_dict(list(map(lambda x: services_prop[x['_id']], to_run)))
        # update fs_check values
        services_state = list(map(lambda x: self.set_fs_check(x, services_to_check, now), services_state.values()))
        # generate checks
        return list(map(lambda x: self.create_check(x, commands), services_to_check.values())), common.convert_list_in_dict(services_state)

    def consume_check_results(self, checks, services_state, services_prop):
        """Consume check results (checks = [])"""
        # TODO NEED UPDATE THE SERVICE, NOT THE CHECK
        checks = common.convert_list_in_dict(checks)
        # update self.services (ls_ simple)
        services_state = list(map(lambda x: self.update_service_ls(x, checks), services_state.values()))
        # update self.services (manage hard / soft)
        return common.convert_list_in_dict(list(map(lambda x: self.manage_hard_soft(x, services_prop[x['_id']], checks), services_state)))

    @staticmethod
    def update_service_ls(x, checks):
        """Update the service properties with data of the check"""
        if not x['_id'] in checks.keys():
            return x
        check = checks[x['_id']]
        x['ls_state'] = check['return_code']
        #    'ls_state_id': {
        #    'ls_acknowledged': {
        #    'ls_acknowledgement_type': {
        #    'ls_downtimed': {
        #    'ls_last_check': {
        #    'ls_last_state': {
        #    'ls_last_state_type': {
        #    'ls_last_state_changed': {
        #    'ls_next_check': {
        x['ls_output'] = check['output']
        x['ls_long_output'] = check['output']
        x['ls_perf_data'] = check['perf_data']
        #    'ls_current_attempt': {
        #    'ls_latency': {
        x['ls_execution_time'] = check['time_poller_finish'] - check['time_poller_run']
        #    'ls_passive_check': {
        #    'ls_state_changed': {
        #    'ls_last_hard_state_changed': {
        #    'ls_last_time_ok': {
        #    'ls_last_time_warning': {
        #    'ls_last_time_critical': {
        #    'ls_last_time_unknown': {
        #    'ls_last_time_unreachable': {
        #    'ls_last_notification': {
        x['fs_check']['check_sent'] = False
        return x

    @staticmethod
    def manage_hard_soft(x, service_prop, checks):
        """Manage the type HARD / SOFT of the service with check result"""
        # HARD OK -> SOFT CRITICAL -> SOFT CRITICAL -> HARD CRITICAL
        # HARD OK -> SOFT CRITICAL -> HARD OK
        # HARD OK -> SOFT WARNING -> SOFT CRITICAL -> HARD CRITICAL
        # HARD CRITICAL -> HARD OK
        # TODO must rewrite, not working
        # if x.state_type. == 'SOFT':
        #     # Manage case of multiple tries
        #     service['ls_current_attempt'] += 1
        #     if service['ls_current_attempt'] >= service['max_check_attempts']:
        #         service['ls_state_type'] = 'HARD'
        #         service['ls_current_attempt'] = 0
        #         # TODO calculate next run
        #     # TODO calculate next run in check attempt mode
        # elif service['ls_state'] == 'OK':
        #     if x.state != 'OK':
        #         service['ls_state_type'] = 'SOFT'
        #         service['ls_current_attempt'] += 1
        return x

    def check_freshness(self, services, now, freshnessed):
        """Check the freshness and do actions when freshness is expired"""
        passives = list(filter(lambda x: x['passive_checks_enabled'], services.values()))
        passives_expired = list(filter(lambda x: x['ls_last_check'] < (now - float(x['freshness_threshold'])) and x['_id'] not in freshnessed, passives))
        passives_expired_notyet_managed = list(filter(lambda x: x['_id'] not in freshnessed, passives_expired))
        passives_expired_notyet_managed_ids = common.convert_list_in_dict(passives_expired_notyet_managed)
        # update state
        if passives_expired_notyet_managed_ids.keys():
            services = list(map(lambda x: self.update_service_freshness_expired(x, passives_expired_notyet_managed_ids.keys()), services.values()))
            return common.convert_list_in_dict(services)
        return services

    ############################################################
    ###################### PURE FUNCTIONS ######################
    ############################################################

    @staticmethod
    def filter_to_run(x, now):
        """Get services not have check running and need to be run"""
        if x['fs_check_period']['start'] < now and x['fs_check_period']['end'] > now and not x['fs_check']['check_sent'] and x['ls_next_check'] <= now:
            return x
        return False

    @staticmethod
    def create_check(x, commands):
        """Create check with properties for the element"""
        return {
            'command': commands[x['check_command']]['command_line'],
            'command_args': x['check_command_args'].split(),
            'timeout': commands[x['check_command']]['timeout'],
            'time_creation': time.time(),
            'time_poller_received': 0.0,
            'time_poller_run': 0.0,
            'time_poller_finish': 0.0,
            'time_scheduler_received': 0.0,
            'service': x['_id'],
            'running_process': None,
            'return_code': None,
            'output': '',
            'perf_data': ''
        }

    @staticmethod
    def mapping_dict_list_indexes(x):
        """Get mapping service _id => list index"""
        data = {}
        i = 0
        for y in x:
            data[y['_id']] = i
            i += 1
        return data

    @staticmethod
    def calculate_next_check_planned(x, service_prop):
        """Calculate the next check timestamp based on retry or check interval, depend on cases"""
        if x['ls_current_attempt'] > 0:
            # in this case (SOFT type, need use retry_interval
            x['ls_next_check'] = x['fs_check']['date_sent'] + float(service_prop['retry_interval'])
        else:
            # in this case (HARD type),  use check_interval
            x['ls_next_check'] = x['fs_check']['date_sent'] + float(service_prop['check_interval'])
        return x

    @staticmethod
    def update_service_freshness_expired(x, freshness_services):
        """Update ls_state with freshness_state value in services when needed to do"""
        if x['_id'] in freshness_services:
            x['ls_state'] = x['freshness_state']
        return x

    @staticmethod
    def generate_freshnessed_services(x, now):
        """Return only services have last_check too older"""
        if x['ls_last_check'] < (now - float(x['freshness_threshold'])):
            return x['_id']
        return False

    @staticmethod
    def update_field_with_another(x, field_name, field_value):
        """Update value of dict with another value"""
        x[field_name] = field_value
        return x

    @staticmethod
    def map_services_prop(service):
        """Get static / config properties"""
        new = {}
        for key, val in service.items():
            if key[:3] != "ls_":
                new[key] = val
        return new

    @staticmethod
    def map_services_state(service):
        """Get state properties (dynamic)"""
        print("TODO")
        new = {
            "_id": service["_id"]
        }
        for key, val in service.items():
            if key[:3] == "ls_":
                new[key] = val
        new["fs_check_period"] = {
            "start": 0.0,
            "end": 0.0
        }
        new["fs_notification_period"] = {
            "start": 0.0,
            "end": 0.0
        }
        new["fs_check"] = {
            "check_sent": False,
            "date_sent": 0.0
        }
        return new

    @staticmethod
    def set_fs_check(service_state, services_to_check, now):
        if service_state["_id"] in services_to_check.keys():
            service_state["fs_check"]["check_sent"] = True
            service_state["fs_check"]["date_sent"] = now
        return service_state
