#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2015: Alignak team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak.
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#  Copyright (C) 2009-2014:
#     Hartmut Goebel, h.goebel@goebel-consult.de
#     aviau, alexandre.viau@savoirfairelinux.com
#     Nicolas Dupeux, nicolas@dupeux.net
#     Zoran Zaric, zz@zoranzaric.de
#     Grégory Starck, g.starck@gmail.com
#     Sebastien Coavoux, s.coavoux@free.fr
#     Thibault Cohen, titilambert@gmail.com
#     Jean Gabes, naparuba@gmail.com
#     Olivier Hanesse, olivier.hanesse@gmail.com
#     Gerhard Lausser, gerhard.lausser@consol.de

#  This file is part of Shinken.
#
#  Shinken is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Shinken is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Shinken.  If not, see <http://www.gnu.org/licenses/>.
"""This module provides Check classe which is a simple abstraction for monitoring checks

"""
from alignak.action import Action
from alignak.property import BoolProp, IntegerProp, FloatProp
from alignak.property import StringProp


class Check(Action):
    """Check class implements monitoring concepts of checks :(status, state, output)
    Check instance are used to store monitoring plugins data (exit status, output)
    and used by schedule to raise alert, reschedule check etc.

    """
    # AutoSlots create the __slots__ with properties and
    # running_properties names

    # FIXME : reenable AutoSlots if possible
    # __metaclass__ = AutoSlots

    my_type = 'check'

    properties = {
        'is_a':             StringProp(default='check'),
        'type':             StringProp(default=''),
        '_in_timeout':      BoolProp(default=False),
        'status':           StringProp(default=''),
        'exit_status':      IntegerProp(default=3),
        'state':            IntegerProp(default=0),
        'output':           StringProp(default=''),
        'long_output':      StringProp(default=''),
        'ref':              IntegerProp(default=-1),
        't_to_go':          IntegerProp(default=0),
        'depend_on':        StringProp(default=[]),
        'dep_check':        StringProp(default=[]),
        'check_time':       IntegerProp(default=0),
        'execution_time':   FloatProp(default=0.0),
        'u_time':           FloatProp(default=0.0),
        's_time':           FloatProp(default=0.0),
        'perf_data':        StringProp(default=''),
        'check_type':       IntegerProp(default=0),
        'poller_tag':       StringProp(default='None'),
        'reactionner_tag':   StringProp(default='None'),
        'env':              StringProp(default={}),
        'internal':         BoolProp(default=False),
        'module_type':      StringProp(default='fork'),
        'worker':           StringProp(default='none'),
        'from_trigger':     BoolProp(default=False),
    }

    def __init__(self, status, command, ref, t_to_go, dep_check=None, id=None,
                 timeout=10, poller_tag='None', reactionner_tag='None',
                 env={}, module_type='fork', from_trigger=False, dependency_check=False):

        self.is_a = 'check'
        self.type = ''
        if id is None:  # id != None is for copy call only
            self.id = Action.id
            Action.id += 1
        self._in_timeout = False
        self.timeout = timeout
        self.status = status
        self.exit_status = 3
        self.command = command
        self.output = ''
        self.long_output = ''
        self.ref = ref
        # self.ref_type = ref_type
        self.t_to_go = t_to_go
        self.depend_on = []
        if dep_check is None:
            self.depend_on_me = []
        else:
            self.depend_on_me = [dep_check]
        self.check_time = 0
        self.execution_time = 0
        self.u_time = 0  # user executon time
        self.s_time = 0  # system execution time
        self.perf_data = ''
        self.check_type = 0  # which kind of check result? 0=active 1=passive
        self.poller_tag = poller_tag
        self.reactionner_tag = reactionner_tag
        self.module_type = module_type
        self.env = env
        # we keep the reference of the poller that will take us
        self.worker = 'none'
        # If it's a business rule, manage it as a special check
        if ref and ref.got_business_rule or command.startswith('_internal'):
            self.internal = True
        else:
            self.internal = False
        self.from_trigger = from_trigger
        self.dependency_check = dependency_check


    def copy_shell(self):
        """return a copy of the check but just what is important for execution
        So we remove the ref and all

        :return: a copy of check
        :rtype: object
        """
        # We create a dummy check with nothing in it, just defaults values
        return self.copy_shell__(Check('', '', '', '', '', id=self.id))

    def get_return_from(self, c):
        """Update check data from action (notification for instance)

        :param c: action to get data from
        :type c: alignak.action.Action
        :return: None
        """
        self.exit_status = c.exit_status
        self.output = c.output
        self.long_output = c.long_output
        self.check_time = c.check_time
        self.execution_time = c.execution_time
        self.perf_data = c.perf_data
        self.u_time = c.u_time
        self.s_time = c.s_time


    def is_launchable(self, t):
        """Check if the check can be launched

        :param t: time to compare with t_to_go attribute
        :type t: int
        :return: True if t > self.t_to_go, False otherwise
        :rtype: bool
        """
        return t > self.t_to_go

    def __str__(self):
        return "Check %d status:%s command:%s ref:%s" % \
               (self.id, self.status, self.command, self.ref)

    def get_id(self):
        """Getter for id attribute

        :return: id
        :rtype: int
        """
        return self.id

    def set_type_active(self):
        """Set check_type attribute to 0

        :return: None
        """
        self.check_type = 0

    def set_type_passive(self):
        """Set check_type attribute to 1

        :return: None
        """
        self.check_type = 1

    def is_dependent(self):
        """Getter for dependency_check attribute

        :return: True if this check was created for dependent one, False otherwise
        :rtype: bool
        """
        return self.dependency_check