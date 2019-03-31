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
#      Hartmut Goebel, h.goebel@goebel-consult.de
#      aviau, alexandre.viau@savoirfairelinux.com
#      Grégory Starck, g.starck@gmail.com
#      Gerhard Lausser, gerhard.lausser@consol.de
#      Sebastien Coavoux, s.coavoux@free.fr
#      Jean Gabes, naparuba@gmail.com
#      Romain Forlot, rforlot@yahoo.com
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
The objects package contains the definition of the classes for the different objects
 that can be declared in configuration files.
"""

from fusionsupervision.objects.item import Item, Items
from fusionsupervision.objects.timeperiod import Timeperiod, Timeperiods
from fusionsupervision.objects.schedulingitem import SchedulingItem
from fusionsupervision.objects.service import Service, Services
from fusionsupervision.objects.command import Command, Commands
from fusionsupervision.objects.config import Config
from fusionsupervision.objects.resultmodulation import Resultmodulation, Resultmodulations
from fusionsupervision.objects.escalation import Escalation, Escalations
from fusionsupervision.objects.serviceescalation import Serviceescalation, Serviceescalations
from fusionsupervision.objects.hostescalation import Hostescalation, Hostescalations
from fusionsupervision.objects.host import Host, Hosts
from fusionsupervision.objects.hostgroup import Hostgroup, Hostgroups
from fusionsupervision.objects.realm import Realm, Realms
from fusionsupervision.objects.contact import Contact, Contacts
from fusionsupervision.objects.contactgroup import Contactgroup, Contactgroups
from fusionsupervision.objects.notificationway import NotificationWay, NotificationWays
from fusionsupervision.objects.servicegroup import Servicegroup, Servicegroups
from fusionsupervision.objects.servicedependency import Servicedependency, Servicedependencies
from fusionsupervision.objects.hostdependency import Hostdependency, Hostdependencies
from fusionsupervision.objects.module import Module, Modules
from fusionsupervision.objects.businessimpactmodulation import Businessimpactmodulation, \
    Businessimpactmodulations
from fusionsupervision.objects.macromodulation import MacroModulation, MacroModulations
