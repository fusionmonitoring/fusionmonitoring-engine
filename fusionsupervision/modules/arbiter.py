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

from multiprocessing import Process
from fusionsupervision.modules.poller import Poller
from fusionsupervision.modules.scheduler import Scheduler

class Arbiter():
    """Get configuration from FusionSupervision backend and manage modules"""

    def start_modules(self):
        """Start the modules in separate processes"""
        # TODO check https://docs.python.org/3/library/multiprocessing.html
        poller = Poller()
        self.poller = Process(poller.start)
        self.poller.start()

        scheduler = Scheduler({})
        self.scheduler = Process(scheduler.start)
        self.scheduler.start()

    def stop_modules(self):
        """Stop the modules properly"""
        self.poller.terminate()
        self.scheduler.terminate()
