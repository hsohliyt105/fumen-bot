# -*- coding: utf-8 -*-

command_list = [ 'help', 'four' ]

command_help = { 
    'help': 'Sends the list of commands and descriptions. `!help [command name, optional]`',
    'four': 'Sends an four formatted image containing the fumen. `!four <fumen string / fumen url / tinyurl> [options]`' 
    }

command_option = { 
    'help': '`command name` Example: `!help four`',
    'four': '`option=<option>` \nOption list (first option is the default): \n`transparent(t)=yes(y)/no(n)` (not supported in gif), \n`theme=dark/light`, \n`duration(d)=0.5/<delay per frame in seconds>` \n`background(b)=#36393f/<hex colour code>` \nExample: `!four v115@HhwhglQpAtwwg0Q4C8JewhglQpAtwwg0Q4A8LeAgH duration=1 t=n b=#FFFFFF`' 
    }

version = "0.0.6"

presence_time = 60
