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

class Control():
    """Manage the control (host and services)"""

    name = ''
    'business_impact': {
    'alias': {
    'notes': {
    'notes_url': {
    'action_url': {
    'tags': {
    'customs': {
    'location': {
    'parents': {
    'ipv4': {
    'ipv6': {
    'maintenance_period': {
    'initial_state': {
    'check_period': {
    'time_to_orphanage': {
    'active_checks_enabled': {
    'check_command': {
    'check_command_args': {
    'max_check_attempts': {
    'check_interval': {
    'retry_interval': {
    'passive_checks_enabled': {
    'check_freshness': {
    'freshness_threshold': {
    'freshness_state': {
    'event_handler_enabled': {
    'event_handler': {
    'event_handler_args': {
    'flap_detection_enabled': {
    'flap_detection_options': {
    'low_flap_threshold': {
    'high_flap_threshold': {
    'process_perf_data': {
    'notifications_enabled': {
    'notification_period': {
    'notification_options': {
    'users': {
    'usergroups': {
    'notification_interval': {
    'first_notification_delay': {
    'stalking_options': {
    'poller_tag': {
    'reactionner_tag': {
    'trigger_name': {
    'trigger_broker_raise_enabled': {
    'snapshot_enabled': {
    'snapshot_command': {
    'snapshot_period': {
    'snapshot_criteria': {
    'snapshot_interval': {
    'ls_state': {
    'ls_state_type': {
    'ls_state_id': {
    'ls_acknowledged': {
    'ls_acknowledgement_type': {
    'ls_downtimed': {
    'ls_last_check': {
    'ls_last_state': {
    'ls_last_state_type': {
    'ls_next_check': {
    'ls_output': {
    'ls_long_output': {
    'ls_perf_data': {
    'ls_current_attempt': {
    'ls_latency': {
    'ls_execution_time': {
    'ls_passive_check': {
    'ls_state_changed': {
    'ls_last_state_changed': {
    'ls_last_hard_state_changed': {
    'ls_last_time_up': {
    'ls_last_time_down': {
    'ls_last_time_unknown': {
    'ls_last_time_unreachable': {
    'ls_grafana': {
    'ls_grafana_panelid': {
    'ls_last_notification': {
    '_realm': {
    '_sub_realm': {


    def __init__(self, prop):
