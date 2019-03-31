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
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#  Copyright (C) 2015-2018: Alignak team, see AUTHORS.alignak.txt file for contributors
#
#  This file is part of Alignak.
#
#  Alignak is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Alignak is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Alignak.  If not, see <http://www.gnu.org/licenses/>.
#
#
#  This file incorporates work covered by the following copyright and
#  permission notice:
#
#   Copyright (C) 2009-2014:
#      Thibault Cohen, titilambert@gmail.com
#      Jean Gabes, naparuba@gmail.com
#
#   This file is part of Shinken.
#
#   Shinken is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Shinken is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

"""
This file is to be imported by every FusionSupervision Engine service component:
Arbiter, Scheduler, etc. It just checks for the main requirement of
FusionSupervision Engine.
"""

import sys
from fusionsupervision.notification import Notification
from fusionsupervision.eventhandler import EventHandler
from fusionsupervision.check import Check
from fusionsupervision.downtime import Downtime
from fusionsupervision.contactdowntime import ContactDowntime
from fusionsupervision.comment import Comment
from fusionsupervision.objects.module import Module


# Make sure people are using Python 2.7 or higher
# This is the canonical python version check
if sys.version_info < (2, 7):
    sys.exit("FusionSupervision engine requires as a minimum Python 2.7.x, sorry")
