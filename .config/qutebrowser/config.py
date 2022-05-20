# config.py
#
# NOTE: config.py is intended for advanced users who are comfortable
# with manually migrating the config file on qutebrowser upgrades. If
# you prefer, you can also configure qutebrowser using the
# :set/:bind/:config-* commands without having to write a config.py
# file.
#
# Documentation:
#   qute://help/configuring.html
#   qute://help/settings.html

# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103

config.load_autoconfig(False)

c.auto_save.session = True

# Format of timestamps (e.g. for the history completion).
c.completion.timestamp_format = '%d-%m-%Y %H:%M'

# Confirm quit if downloading
c.confirm_quit = ["downloads"]

# Download locations
c.downloads.location.directory = "~/Downloads"

c.url.searchengines = {'DEFAULT': 'https://start.duckduckgo.com/?q={}',
                       'aw': 'https://wiki.archlinux.org/?search={}',
                       'goog': 'https://www.google.com/search?q={}',
                       're': 'https://www.reddit.com/search?q={}',
                       # Go to a given subreddit
                       'sr': 'https://www.reddit.com/r/{unquoted}',
                       'gh': 'https://github.com/search?q={}',
                       # Jumpt to github repo or user
                       'ghr': 'https://github.com/{unquoted}',
                       'wiki': 'https://en.wikipedia.org/wiki/{}',
                       'yt': 'https://www.youtube.com/results?search_query={}'}

c.url.default_page = 'https://start.duckduckgo.com'

config.set('content.cookies.accept', 'all', 'chrome-devtools://*')

config.set('content.cookies.accept', 'all', 'devtools://*')

config.set('content.headers.accept_language', '', 'https://matchmaker.krunker.io/*')

config.set('content.headers.user_agent', 'Mozilla/5.0 ({os_info}) AppleWebKit/{webkit_version} (KHTML, like Gecko) {upstream_browser_key}/{upstream_browser_version} Safari/{webkit_version}', 'https://web.whatsapp.com/')

config.set('content.headers.user_agent', 'Mozilla/5.0 ({os_info}) AppleWebKit/{webkit_version} (KHTML, like Gecko) {upstream_browser_key}/{upstream_browser_version} Safari/{webkit_version} Edg/{upstream_browser_version}', 'https://accounts.google.com/*')

config.set('content.headers.user_agent', 'Mozilla/5.0 ({os_info}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99 Safari/537.36', 'https://*.slack.com/*')

config.set('content.images', True, 'chrome-devtools://*')

config.set('content.images', True, 'devtools://*')

config.set('content.javascript.enabled', True, 'chrome-devtools://*')

config.set('content.javascript.enabled', True, 'devtools://*')

config.set('content.javascript.enabled', True, 'chrome://*/*')

config.set('content.javascript.enabled', True, 'qute://*/*')

config.set('content.notifications.enabled', True, 'https://www.netflix.com')

config.set('content.register_protocol_handler', True, 'https://mail.google.com?extsrc=mailto&url=%25s')

c.editor.command = ['kitty', '-e', 'nvim', '{file}', '-c', 'normal {line}G{column0}l']

c.fileselect.multiple_files.command = ['kitty', '-e', 'ranger', '--choosefiles={}']

c.fileselect.folder.command = ['kitty', '-e', 'ranger', '--choosedir={}']

c.spellcheck.languages = ['en-GB']

c.tabs.padding = {'bottom': 4, 'left': 5, 'right': 5, 'top': 2}

c.tabs.select_on_remove = 'prev'

c.fonts.default_family = 'FiraCode Nerd Font'
c.fonts.default_size = '10pt'
c.fonts.web.family.standard = 'FiraCode Nerd Font'
c.fonts.web.size.default = 14

# Font used for the context menu. If set to null, the Qt default is
# used.
# Type: Font
c.fonts.contextmenu = 'default_size default_family'

config.bind(',M', 'hint links spawn mpv {hint-url}')
config.bind('xb', 'config-cycle statusbar.show never always')
config.bind('xt', 'config-cycle tabs.show never always ')
config.bind('xx', 'config-cycle statusbar.show never always;; config-cycle tabs.show never always ')
# config.source("gruvbox.py")

# Custom stylesheet for qt to set tab mouse hover info window font size
c.qt.args += ['stylesheet=/home/justine/.config/qutebrowser/stylesheet.qss']

c.content.autoplay = False
