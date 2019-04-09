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

import ujson
import zmq

def create_zmq_publisher(port):
    """Create socket to pubkish on zmq"""
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    return socket

def create_zmq_subscriver(port, topic):
    """Create socket to subscribe to a zmq publisher"""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:%s" % str(port))
    socket.setsockopt_string(zmq.SUBSCRIBE, topic)
    return socket

def zmq_send(socket, topic, data):
    """Publish data on specific topic"""
    socket.send_string("%s|||||%s" % (topic, ujson.dumps(data)))

def zmq_receive(socket):
    """Get data publisheds"""
    try:
        string = socket.recv(flags=zmq.NOBLOCK)
        _, jsonchecks = string.decode().split("|||||")
        return ujson.loads(jsonchecks)
    except zmq.Again:
        pass
    return []

def manage_signal():
    """Intercept signal like SIGTERM"""
    print("TODO")

############################################################
###################### PURE FUNCTIONS ######################
############################################################

def convert_list_in_dict(source):
    """Convert list in dict with _id value in key of the dict"""
    data = {}
    for x in source:
        data[x['_id']] = x
    return data
