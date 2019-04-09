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

from FusionSupervision.object.configbackend import configbackend

class Fusionsupervision(object):
    """GLobal Fusionsupervision"""

    def start():
        """Start the program"""

        # * load general config from file

        # * load config from backend
        obj_config = configbackend.get_objects()

        # * run each modules (scheduler, poller, broker, reactionner, receiver) in seperate process
        # * send config through zeromq
        # * begin loop
        #   * [zeromq] check acknowledge send by backend
        #   * [zeromq] check downtime send by backend
        #   * [zeromq] check new hosts  / services added in the backend
        #   * [zeromq] send acknowloedge to scheduler
        #   * [zeromq] send downtimes to scheduler
        #   * [zeromq] dispatch new config?
