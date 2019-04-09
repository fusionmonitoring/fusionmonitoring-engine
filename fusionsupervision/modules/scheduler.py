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
    services = {}

    # dynamic properties
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

    def __init__(self, services, init_zmq=True):
        # TODO replace services with dict {"services":x, "commands":x, "users":x}
        self.services = services
        self.zmq_enable = init_zmq
        # TODO fix it
        #service = list(services.values())

        # manage time (set begin and end period of each host and service)
        self.service_check_period = list(map(lambda x: {'start': 0.0, 'end': 0.0, 'period': x['check_period'], '_id': x['_id']}, list(services.values())))
        self.service_notification_period = list(map(lambda x: {'start': 0.0, 'end': 0.0, 'period': x['notification_period'], '_id': x['_id']}, list(services.values())))
        # Get mapping service _id => list index
        self.mapping_list_services = self.mapping_dict_list_indexes(self.service_check_period)
        # Create timeperiods objects
        # TODO
        # create service check_state
        self.services_check = list(map(lambda x: {'_id': x['_id'], 'check_sent': False, 'date_sent': 0.0, 'next_check_planned': 0.0}, list(services.values())))
        # get acknowledges
        # TODO acknowledges = ...
        # get downtimes
        # TODO downtimes = ...

        # TODO manage the service _id => list index, like {'523453425':0, '408959890325': 1}

        # init zeromq
        if init_zmq:
            self.socket_scheduler = common.create_zmq_publisher(28202)
            self.socket_poller = common.create_zmq_subscriver(28203, "checks_result")

    def start(self):
        """Start running the scheduler"""
        exit = False
        while not exit:
            self.run_loop()
            # TODO manage SIGTERM (in common class), return exit or not

    def run_loop(self, freshnessed=None):
        """run these functions to manage the scheduler"""
        if freshnessed is None:
            freshnessed = []
        now = time.time()
        # TODO zeromq, get checks from poller
        checks = []
        if self.zmq_enable:
            checks = common.zmq_receive(self.socket_poller)
        # TODO zeromq, get acknowledges from arbiter
        # TODO zeromq, get downtimes from arbiter
        # TODO zeromq, get re-checks fro arbiter

        # recalculate periods if needed
        if self.timestamp_next_recalculate_periods < now:
            self.service_check_period = self.manage_service_check_period(now, self.service_check_period)
            #self.timestamp_next_recalculate_periods = reduce(lambda x, y: x if x < y else y, list(map(lambda x: x['end'], self.manage_service_check_period)))
            self.timestamp_next_recalculate_periods = now

        # schedule new checks
        zeromq_checks_to_send = self.schedule_new_checks(now, self.services, self.service_check_period, self.commands)
        print("number checks: ", len(zeromq_checks_to_send))
        # TODO send checks to poller througth zeromq
        if self.zmq_enable:
            common.zmq_send(self.socket_scheduler, "checks_to_run", zeromq_checks_to_send)

        # TODO consume check results (and recalculate next_check_planned in services_check)
        self.services = self.consume_check_results(checks, self.services, self.services_check)

        # TODO check freshness
        self.services = self.check_freshness(self.services, now, freshnessed)
        # regenerate freshnessed services
        freshnessed = list(filter(lambda x: self.generate_freshnessed_services(x, now), self.services.values()))

        # TODO manage notifications
        self.manage_service_notification_period()

        # TODO clean zombies (check, actions)

    @staticmethod
    def manage_service_check_period(now, service_check_period):
        """Set begin and end period of each host and service for check"""
        to_calculate = list(filter(lambda x: x['end'] < now, service_check_period))
        all_timeperiods = list(map(lambda x: x['period'], to_calculate))
        timeperiods = list(set(all_timeperiods))
        def replace_times(x, period, value):
            #if x['period'] == period:
            #    x['start'] = value
            x['end'] = 2054408035.6778336
            return x
        for tid in timeperiods:
            #print(tid)
            # TODO get next start and end for this period
            service_check_period = list(map(lambda x: replace_times(x, '507f1f77bcf86cd799439011', 754368957.0), service_check_period))
        return service_check_period

    @staticmethod
    def manage_service_notification_period():
        """Set begin and end period of each host and service for notification"""
        print("todo")

    def schedule_new_checks(self, now, service, service_check_period, commands):
        """Schedule new checks on hosts and services"""
        # get list from self.service_check_period who need to be scheduled and not running
        to_run = list(filter(lambda x: self.filter_to_run(x, now), service_check_period))
        # get elements in the 2 lists (to_run and service)
        services_to_check = list(map(lambda x: service[x['_id']], to_run))
        # generate checks 
        return list(map(lambda x: self.create_check(x, commands), services_to_check))

    def consume_check_results(self, checks, services, services_check):
        """Consume check results (checks = [])"""
        # TODO update self.services (ls_ simple)
        # services = list(map(lambda x: self.update_service_ls(x, services[x.service]), checks))
        # TODO update self.services (manage hard / soft)
        # services = list(map(lambda x: self.manage_hard_soft(x, services[x.service]), checks))
        # calculate next check planned
        services_check = common.convert_list_in_dict(list(map(lambda x: self.calculate_next_check_planned(x, services[x['_id']]), services_check)))
        # Update ls_next_check in service
        services = list(map(lambda x: self.update_service_ls_next_check(x, services_check[x['_id']]), services.values()))
        return common.convert_list_in_dict(services)

    @staticmethod
    def update_service_ls(x, service):
        """Update the service properties with data of the check"""
        service['ls_state'] = x.status
        #    'ls_state_id': {
        #    'ls_acknowledged': {
        #    'ls_acknowledgement_type': {
        #    'ls_downtimed': {
        #    'ls_last_check': {
        #    'ls_last_state': {
        #    'ls_last_state_type': {
        #    'ls_last_state_changed': {
        #    'ls_next_check': {
        service['ls_output'] = x.output
        service['ls_long_output'] = x.ls_long_output
        service['ls_perf_data'] = x.perf_data
        #    'ls_current_attempt': {
        #    'ls_latency': {
        service['ls_execution_time'] = x.execution_time
        #    'ls_passive_check': {
        #    'ls_state_changed': {
        #    'ls_last_hard_state_changed': {
        #    'ls_last_time_ok': {
        #    'ls_last_time_warning': {
        #    'ls_last_time_critical': {
        #    'ls_last_time_unknown': {
        #    'ls_last_time_unreachable': {
        #    'ls_last_notification': {
        return service

    @staticmethod
    def manage_hard_soft(x, service):
        """Manage the type HARD / SOFT of the service with check result"""
        # HARD OK -> SOFT CRITICAL -> SOFT CRITICAL -> HARD CRITICAL
        # HARD OK -> SOFT CRITICAL -> HARD OK
        # HARD OK -> SOFT WARNING -> SOFT CRITICAL -> HARD CRITICAL
        # HARD CRITICAL -> HARD OK
        if x.state_type == 'SOFT':
            # Manage case of multiple tries
            service['ls_current_attempt'] += 1
            if service['ls_current_attempt'] >= service['max_check_attempts']:
                service['state_type'] = 'HARD'
                service['ls_current_attempt'] = 0
                # TODO calculate next run
            # TODO calculate next run in check attempt mode
        elif service['ls_state'] == 'OK':
            if x.state != 'OK':
                service['state_type'] = 'SOFT'
                service['ls_current_attempt'] += 1
        return service

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
        if x['start'] < now and x['end'] > now:
            #  and x['check_sent'] == False and x['next_check_planned'] < now
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
    def update_service_ls_next_check(x, check):
        """Report next_check_planned of service_check to ls_next_check of the service"""
        x['ls_next_check'] = check['next_check_planned']
        return x

    @staticmethod
    def calculate_next_check_planned(x, service):
        """Calculate the next chack timestamp based on retry or check interval, depend on cases"""
        if service['ls_current_attempt'] > 0:
            # in this case (SOFT type, need use retry_interval
            x['next_check_planned'] = x['date_sent'] + float(service['retry_interval'])
        else:
            # in this case (HARD type),  use check_interval
            x['next_check_planned'] = x['date_sent'] + float(service['check_interval'])
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
