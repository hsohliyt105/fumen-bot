# -*- coding: utf-8 -*-

command_list = [ 'help', 'four' ]

command_help = { 
    'help': 'Sends the list of commands and descriptions. `!help [command name, optional]`',
    'four': 'Sends an four formatted image containing the fumen. `!image <fumen string> [options]`' 
    }

command_option = { 
    'help': '`command name` Example: `!help four`',
    'four': '`option=<option>` Option list (first option is the default): `transparent(t)=yes(y)/no(n)` (not supported in gif), `theme=dark/light`, `duration(d)=0.5/<delay per frame in seconds>` `background(b)=#36393f/<hex colour code>` Example: `!fumen v115@HhwhglQpAtwwg0Q4C8JewhglQpAtwwg0Q4A8LeAgH duration=1 t=n b=#FFFFFF' 
    }

version = "1.0.0"

presence_time = 60