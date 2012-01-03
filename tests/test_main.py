# -*- encoding: utf-8 -*-
from tests import prepare_fakeparser_for_tests
prepare_fakeparser_for_tests()

import os
import time
import b3
from b3.fake import fakeConsole
from vehiclecontrolbf3 import Vehiclecontrolbf3Plugin
from b3.config import XmlConfigParser

conf = XmlConfigParser()
conf.loadFromString("""
<configuration plugin="vehiclecontrolbf3">
    <disable_vehicle_respawn>
        <map>MP_001</map>
        <map>MP_003  </map>
    </disable_vehicle_respawn>
</configuration>
""")
# make B3 think it has a config file on the filesystem
conf.fileName = os.path.join(os.path.dirname(__file__), '../extplugins/conf/vehiclecontrolbf3.xml')


p = Vehiclecontrolbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

def my_getNextMap():
    return nextmap

def my_getHardName(mapname):
    return "MP_007"

fakeConsole.getNextMap = my_getNextMap
fakeConsole.getHardName = my_getHardName

nextmap = "Caspian Border (Squad Deathmatch)"
p._delay = 1

print "----------------------------Should disable vehicles"
fakeConsole.game.mapName = "MP_003"
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_START, None))

time.sleep(1)

print "----------------------------Should enable vehicles"
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_END, None))
