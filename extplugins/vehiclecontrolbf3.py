# -*- coding: utf-8 -*-
#
# Vehicle Control BF3 Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2011-2012 Freelander (freelander@fps-gamer.net)
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# CHANGELOG
#
# 1.0   - Initial release
# 1.0.1 - Bug fix for enabling vehicles again if not in disable list
# 1.0.2 - Ability to skip disabling vehicles on selected gametypes

__version__ = '1.0.2'
__author__  = 'Freelander'

import b3
import b3.events
from b3.plugin import Plugin
import threading

class Vehiclecontrolbf3Plugin(Plugin):

    def __init__(self, console, config=None):
        self._delay = 30
        self._disable_vehicle_respawn_maps = []
        self._whitelist_gametypes = []
        Plugin.__init__(self, console, config)

################################################################################################################
#
#    Plugin interface implementation
#
################################################################################################################

    def onLoadConfig(self):
        '''
        This is called after loadConfig(). Any plugin private variables loaded
        from the config need to be reset here.
        '''
        self._load_messages()
        self._load_disable_vehicle_respawn_maps()
        self._load_whitelist_gametypes()

    def startup(self):
        '''Initialize plugin settings'''
        # Register our events
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        self.registerEvent(b3.events.EVT_GAME_ROUND_END)

    def onEvent(self, event):
        '''Handle intercepted events'''
        if event.type == b3.events.EVT_GAME_ROUND_START:
            self._check_vehicles()
        elif event.type == b3.events.EVT_GAME_ROUND_END:
            self._check_vehicles_next_map()

################################################################################################################
#
#    Other methods
#
################################################################################################################

    def _load_disable_vehicle_respawn_maps(self):
        '''Loads maplist from plugin config file'''
        try:
            for m in self.config.get('disable_vehicle_respawn/map'):
                map = m.text.lower()
                self._disable_vehicle_respawn_maps.append(map.strip())
            self.debug('Vehicle respawn disabled on maps %s' % self._disable_vehicle_respawn_maps)
        except:
            self.debug('Cannot load vehicles respawn disabled map list')

    def _load_whitelist_gametypes(self):
        '''Loads white listed game types from plugin config file'''
        try:
            for m in self.config.get('whitelist_gametypes/gametype'):
                gametype = m.text
                self._whitelist_gametypes.append(gametype.strip())
            self.debug('Vehicle Control Plugin is disabled for gametypes; %s' % self._whitelist_gametypes)
        except:
            self.debug('Cannot load white listed gametypes')

    def _load_messages(self):
        '''Loads messages section from plugin config file'''
        try:
            self.info_message = self.getMessage('messages', 'no_vehicle_respawn')
        except:
            self.info_message = "Combat vehicles will NOT respawn on this map! Use them wisely."

    def _check_vehicles(self):
        '''checks and disables vehicles in current map if included in maplist (if gametype is not whitelisted)'''
        _current_map = self.console.game.mapName.lower()
        self.debug('Checking current map name %s for vehicle disabling' % _current_map)

        _current_gametype = self.console.game.gameType
        self.debug('Current gametype is %s' % _current_gametype)

        if _current_map in self._disable_vehicle_respawn_maps and _current_gametype not in self._whitelist_gametypes:
            self.debug('Map %s found in disable_vehicle_respawn_maps, disabling vehicles in %s seconds' % (_current_map, self._delay))
            t = threading.Timer(self._delay, self.toggle_vehicle_status, ['false'])
            t.start()
            m = threading.Timer(self._delay, self.console.say, [self.info_message])
            m.start()
        elif _current_map in self._disable_vehicle_respawn_maps and _current_gametype in self._whitelist_gametypes:
            self.debug('Map %s found in disable_vehicle_respawn_maps but current gametype %s is whitelisted. Vehicles will respawn on this map' % (_current_map, _current_gametype))

    def _check_vehicles_next_map(self):
        '''checks and enables vehicles for next map if not in maplist'''
        next_map = self.console.getNextMap()
        p = next_map.split('(')
        next_mapName = p[0].strip()
        next_mapName = self.console.getHardName(next_mapName)

        if next_mapName not in self._disable_vehicle_respawn_maps:
            self.debug('Next map (%s) is not in disable_vehicle_respawn_maps, enabling vehicles' % next_mapName)
            self.toggle_vehicle_status('true')
            self.debug('Vehicle respawn enabled')

    def toggle_vehicle_status(self, status):
        '''Enables or disables vehicles'''
        try:
            self.console.setCvar('vehicleSpawnAllowed', status)
            self.debug('Setting vehicle status to %s' % status)
        except CommandFailedError, err:
            self.debug("Cannot change vehicle status : %s" % err.message)
