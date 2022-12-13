# fumen-bot
Discord bot that produces gif or png based on the fumen string given.

Please invite the bot by [this link](https://discord.com/api/oauth2/authorize?client_id=1014015919351152640&permissions=517543938112&scope=bot).

# Uses
## Fumen Strings
Given any fumen strings given no matter it is in raw fumen string or in url such as https://fumen.zui.jp/, Outputs an image with default Four command. 

## !help
Sends the list of commands and descriptions.

### Format
`!help [command name, optional]`

### Example
`!help four`

## !four
Sends an [four](https://four.lol/) formatted image containing the fumen.

### Format
`!four <fumen string / fumen url / tinyurl> [options]`

### Options
Use with `option=<option>` format.

Option list: 

`transparent(t)=yes(y)/no(n)` Sets the transparency of the background. Only supported in png. Default is `yes` for png, and `no` for gif.

`theme=dark/light` Sets the theme of the image. Default is `dark`.

`duration(d)=<delay per frame in seconds>` Sets the duration of each frame in gif, in seconds. Default is `0.5`.

`background(b)=<hex colour code>` Sets the colour of the background. Default is determined by the theme.

### Example
`!four v115@HhwhglQpAtwwg0Q4C8JewhglQpAtwwg0Q4A8LeAgH duration=1.5 t=n theme=light b=#FFFFFF`

# Update

## 0.0.4
[Tinyurls](https://tinyurl.com/app) can now be processed.
