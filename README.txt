Vehicle Control BF3 Plugin for BigBrotherBot (www.bigbrotherbot.net)
===================================================================

Author: Freelander - freelander@bigbrotherbot.net
Author URI: http://www.bigbrotherbot.net
Author URI: http://www.fps-gamer.net

Description
-----------

This plugin disables vehicle respawn on selected maps. i.e. all combat vehicles will
spawn once at the beginning of round and will not spawn again after they are destroyed.
Use this plugin if you want to add some realism to your BF3 server.

This plugin works only for Battlefield 3

Changelog
---------

 * 17.12.2011 - v1.0
    - Initial release

 * 03.01.2012 - v1.0.1
    - Bug fix: enable vehicles again if map is not in the list

Installation
------------

 * copy vehiclecontrolbf3.py into b3/extplugins
 * copy vehiclecontrolbf3.xml into your b3/extplugins/conf folder
 * edit vehiclecontrolbf3.xml with your preferred settings
 * update your main b3 config file with :
   <plugin name="vehiclecontrolbf3" config="@b3/extplugins/conf/vehiclecontrolbf3.xml"/>
 
Support
-------

see the B3 forums http://forum.bigbrotherbot.net/releases/vehicle-control-plugin-for-bf3/