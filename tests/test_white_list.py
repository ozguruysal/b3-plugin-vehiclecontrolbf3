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
    <settings name="messages">
        <set name="no_vehicle_respawn">Combat vehicles will NOT respawn on this map! Use them wisely.</set>
    </settings>
    <disable_vehicle_respawn>
        <map>MP_001</map>
        <map>MP_003</map>
    </disable_vehicle_respawn>
    <whitelist_gametypes>
        <gametype>ConquestLarge0</gametype>
        <gametype>ConquestSmall0</gametype>
        <gametype>ConquestAssaultLarge0</gametype>
        <gametype>ConquestAssaultSmall0</gametype>
        <gametype>ConquestAssaultSmall1</gametype>
    </whitelist_gametypes>
</configuration>
""")
# make B3 think it has a config file on the filesystem
conf.fileName = os.path.join(os.path.dirname(__file__), '../extplugins/conf/vehiclecontrolbf3.xml')

p = Vehiclecontrolbf3Plugin(fakeConsole, conf)
p.onLoadConfig()
p.onStartup()

fakeConsole.game.gameType = 'ConquestLarge0'

print "----------------------------Should skip disabling vehicles"
fakeConsole.game.mapName = "MP_003"
fakeConsole.queueEvent(b3.events.Event(b3.events.EVT_GAME_ROUND_START, None))
