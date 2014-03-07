StarryPy_plugins
================

##A collection of plugins for the [StarryPy](https://github.com/CarrotsAreMediocre/StarryPy) starbound game server proxy
Please note:

* These plugins are free to use, free as in free and open source software.
* The developers of [StarryPy](https://github.com/CarrotsAreMediocre/StarryPy) have very little influence on these plugins, they shall not be blamed if something goes wrong. Precaution is advised before downloading an running any code from the internet.


# Plugins:

## [slitherrr's IRC plugin](https://github.com/StarryPy/StarryPy_plugins/tree/master/plugins/irc_plugin)
> This plugin will connect to the specified server and join the specified target (if it's a channel), and echo messages to that target.
>
> Note that it currently doesn't support multiple channels, but doing so is fairly trivial and it'll probably be added soon.
### Add the following block to your config file:

>```
"irc": {
            "auto_activate": false,
            "bot_nickname": "StarryPy",
            "channel": "!!REPLACE ME!!",
            "echo_from_channel": true,
            "nickserv_password": "!!REPLACE ME!!",
            "port": 6667,
            "server": "irc.freenet.org",
            "color": "^#495449;"
        },
>```


## [SloanReynolds /who on login](https://github.com/MrMarvin/StarryPy_plugins/blob/master/plugins/loginwho_plugin)
> Displays a /who upon login

## [FZFalzar's BetterWhisper plugin](https://github.com/FZFalzar/StarryPy_plugins/tree/brutus_whisper/plugins/brutus_whisper)
> Brings better functionality for the sending of Private Messages in Starbound
> Adds the following commands and abilities to the server:
>```
@permissions(UserLevels.GUEST)
/w <name> <message> 			#Sends a PM to target. Overrides default /w functionality. alias is /whisper
/r <message>      				#Replies to the last person who you received a PM from
@permissions(UserLevels.ADMIN)
/socialspy <on|true|off|false>	#Enables/Disables SocialSpy, a feature for admins to receive PMs sent by anyone, for policing purposes
>```

## [FZFalzar's /afk plugin](https://github.com/FZFalzar/StarryPy_plugins/tree/afk_plugin/plugins/afk_plugin)
> Simple plugin that allows players to set their status via /afk.
> Player will be automatically unmarked from AFK if they chat or interact with any entity (doors, chests etc).
> Currently does not allow auto-afk or un-afk upon player movement due to API deficiency.
>```
@permissions(UserLevels.GUEST)
/afk							#Enables/disables AFK status
>```

> ### Add the following block to your config file:

>```
"afk_plugin": {
    "afk_msg": "is now AFK",
    "afkreturn_msg": "has returned",
	"auto_activate": true
    }
>```

## [Maffi's uptime plugin](https://github.com/MrMarvin/StarryPy_plugins/blob/master/plugins/uptime)
> Very simple plugin that responds to /uptime with the time StarryPy is running.

## [teihoo's /me emote plugin](https://github.com/StarryPy/StarryPy_plugins/tree/master/plugins/emotes)
> Very simple plugin that adds /me <emote> command to StarryPy.

## [teihoo's /starteritems plugin](https://github.com/StarryPy/StarryPy_plugins/tree/master/plugins/starteritems)
> Adds /starteritems command which can be used once per player and will give player a set of predefined starter items
> It is ment to work along with new_player_greeter_plugin, and will give a different set, that's why:

> ### Add the following block to your config file:

>```
"starteritems_plugin": {
    "auto_activate": true,
    "items": [
    [ "coalore", 100 ],
    [ "money", 1000 ]
    ],
    "message": "You were given a set of starter items ;)"
  }
>```

## [teihoo's /players plugin](https://github.com/StarryPy/StarryPy_plugins/tree/master/plugins/players)
> Very simple plugin that adds /players command, which is an alias for the existing /who command, to StarryPy.

## [teihoo's bookmarks plugin](https://github.com/StarryPy/StarryPy_plugins/tree/master/plugins/bookmarks)
> Adds the following commands and abilities to the server:
> ```
@permissions(UserLevels.GUEST)  #everything works for all users
/bookmark <name>  #creates a personal bookmark of the planet (need to be on planet)
/goto <name>      #moves ship to the bookmarked planet (need to be on ship)
/remove <name>    #removes a bookmark (need to be on planet)
> ```

## [mdeneen's Pushover plugin](https://github.com/StarryPy/StarryPy_plugins/tree/master/plugins/pushover_plugin)
> This adds basic support for [Pushover](https://pushover.net) messages. Right now it can:

> - Send a pushover message to a mobile device whenever a player joins
> - Avoid sending notifications for ignored players.
> Pushover supports delivery groups, so one could send messages to multiple users. This can be useful when running a private server so that you know when other players are online.

> ### Add the following block to your config file:

> ```
"pushover_plugin": {
    "api_key": "MY_API_KEY",
    "ignored_players":
        "Player1",
    ],
    "user_key": "MY_USER_KEY"
}
>```

## [Maffi's planet visitor announcer](https://github.com/StarryPy/StarryPy_plugins/tree/master/plugins/planet_visitor_announcer)
> Sends a message to every player on the planet whenever another player warps down onto it.

## [Hexicube's Planet Warps for StarryPy](https://github.com/MrMarvin/StarryPy_plugins/blob/master/plugins/hexicube_planet_warps_for_starrypy.py)

> Currently it conflicts with /warp from warpy because really that should be called /tp due to what it does. If you want to use this with warpy at the same time, you'll have to change one of them to work around the other.
>
>This plugin allows admins to create and delete 'warps' to any planet. They just go on a planet and "/set_warp <name>" to make a warp. It correctly blocks doing so if that name or planet have been used in another warp.
>Similarly, admins can use "/del_warp <name>" to remove warps, and they don't have to be on a planet to do so.
>
>All users can do "/warp" to view a list of set warps, and "/warp <name>" to go to one of the planets free of charge. Currently it starts moving your ship to that planet and instantly warps you down, but I'm looking for a way to keep a player's ship where it is. The plugin has been tested and definitely works the way it should. Also, I suggest protecting a planet before making a warp to it.

## [StarryPy Server Status](https://bitbucket.org/zvorgan/starrypy-server-status/)
>Server status plugin available here. You can send query on specified port (specified in server_status.py) and plugin return status (online/offline) and number of players.
>Also include small php script for embed this in your website.

## [traxo-xx's Notify My Android plugin](https://github.com/StarryPy/StarryPy_plugins/tree/master/plugins/nma_plugin)
> If activated, this plugin will send a notification to your [Notify My Android](https://www.notifymyandroid.com/) account.

> ### Add the following block to your config file:

> ```javascript
        "nma_plugin": {
            "api_application": "StarryPy Server",
            "api_event": "Player joined",
            "api_key": "API_KEY",
            "api_priority": "0",
            "auto_activate": true,
            "ignored_players": [
                "Player"
            ]
        },
>```

> **api_application**: Name of the application the notification will come from.
>
> **api_event**: Subject of the notification.
>
> **ignored_players**: The plugin will not send a notification when a player in this list joins the server.
>
> The other parameters are pretty self-explanatory

## [traxo-xx's WebGUI plugin](https://github.com/StarryPy/StarryPy_plugins/tree/master/plugins/web_gui)
> If activated, this give you a web-GUI to administrate your StarryPy server. Still in a very alpha-ish state, which is why it is deactivated by default. For now it only has some basic functions ( I will add more soon), but those should work. Well, except for the chat... the order old messages get's f**ked up when you reload the dashboard. I'll try to fix that soon. When it's activated you can log in to the GUI with the name of the server owner and the password you set in the config file.

> ### Required Python packages:

> * tornado

> ### Add the following block to your config file:

> ```javascript
        "web_gui": {
            "auto_activate": false,
            "cookie_token": "",
            "log_path": "webgui.log",
            "log_path_access": "webgui_access.log",
            "ownerpassword": "!!PUT A PASSWORD HERE",
            "port": 8083,
            "remember_cookie_token": true,
            "restart_script": "",
            "serverurl": "localhost"
        },
>```

> **cookie_token**: A secure token for Cookies. Leave this blank. The plugin will fill it.
> **ownerpassword**: Password for the web-GUI.
> **port**: The port the web-GUI will listen on.
> **remember_cookie_token**: If set to true, you will stay logged in until you log out (even after you restart StarryPy). If set to false, a new cookie_token will be generated on every start of StarryPy.
> **restart_script**: Path to a script to restart starbound and/or StarryPy.
> **serverurl**: URL or IP of your StarryPy server.

> ### Credits:

> DevOOPS Bootstrap 3 Admin theme https://github.com/devoopsme/devoops/

> jQuery-Knob http://anthonyterrien.com/knob/ (MIT or GPL)  1.2.5
> D3 http://d3js.org/ 3.4.1 AS IS
> Select2 https://github.com/ivaynberg/select2  3.4.5 GPL2
> Bootstrap Validator https://github.com/nghuuphuoc/bootstrapvalidator 0.2.3 MIT
> TinyMCE http://www.tinymce.com 4.0.16 GPL2
> jQuery Timepicker http://trentrichardson.com/examples/timepicker/ 1.4.3 MIT
> xCharts http://tenxer.github.io/xcharts/ 0.3.0 AS IS
> Fancybox http://fancyapps.com/fancybox/ 2.1.5 ?
> Widen FineUploader https://github.com/Widen/fine-uploader  (GPL3) v 4.3.1
> Datatables  http://datatables.net 1.9.4 GPL or BSD
> jQuery-UI 1.10.4
> Twitter Bootstrap http://getbootstrap.com 3.1.0
> Flot www.flotcharts.org  0.8.2 AS IS
> Fullcalendar http://arshaw.com/fullcalendar 2.0..0beta MIT
> Moment http://momentjs.com/ 2.5.1 MIT
> Justified Gallery https://github.com/miromannino/Justified-Gallery 2.1 Creative Commons 3.0
> Morris Charts http://www.oesmith.co.uk/morris.js/ v0.4.3 MIT
