# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401
from libqtile import qtile
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.layout.floating import Floating
from libqtile.lazy import lazy
# from libqtile.utils import guess_terminal
from libqtile import hook
# from libqtile.command import lazy
from datetime import datetime as dt
import os
import subprocess
import time
# from libqtile.utils import send_notification
from libqtile.log_utils import logger

# Get the number of connected screens


def get_monitors():
    xr = subprocess.check_output('xrandr --query | grep " connected"', shell=True).decode().split('\n')
    monitors = len(xr) - 1 if len(xr) > 2 else len(xr)
    return monitors


monitors = get_monitors()

# Run autorandr --change and restart Qtile on screen change


@hook.subscribe.screen_change
def set_screens(event):
    subprocess.run(["autorandr", "--change"])
    # lazy.spawn("mydock")
    qtile.restart()

# When application launched automatically focus it's group


@hook.subscribe.client_new
def modify_window(client):
    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[group.name]  # there can be multiple instances of a group
            targetgroup.cmd_toscreen(toggle=False)
            break

# Hook to fallback to the first group with windows when last window of group is killed


@hook.subscribe.client_killed
def fallback(window):
    if window.group.windows != [window]:
        return
    idx = qtile.groups.index(window.group)
    for group in qtile.groups[idx - 1::-1]:
        if group.windows:
            qtile.current_screen.toggle_group(group)
            return
    qtile.current_screen.toggle_group(qtile.groups[0])

# Work around for matching Spotify


@hook.subscribe.client_new
def slight_delay(window):
    time.sleep(0.04)


@hook.subscribe.startup_once
def autostart():
    # home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])

# Add th, nd or st to the date - use custom_date in text box


def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def custom_date():
    return custom_strftime('%A {S} %B %Y - %H:%M', dt.now())


mod = "mod4"

terminal = 'kitty'
home = os.path.expanduser('~')

MYCOLORS = [
    '#073642',
    '#dc322f',
    '#00ff2a',
    '#b58900',
    '#268bd2',
    '#d33682',
    '#2aa198',
    '#eee8d5'
]

BLACK = MYCOLORS[0]
RED = MYCOLORS[1]
GREEN = MYCOLORS[2]
YELLOW = MYCOLORS[3]
BLUE = MYCOLORS[4]
MAGENTA = MYCOLORS[5]
CYAN = MYCOLORS[6]
WHITE = MYCOLORS[7]

keys = [

    Key([mod], "g",
        lazy.screen.next_group(skip_empty=True),
        desc="Move to next active group"
        ),
    Key([mod, "shift"], "g",
        lazy.screen.prev_group(skip_empty=True),
        desc="Move to previous active group"
        ),
    # Switch between windows in current stack pane
    Key([mod], "k",
        lazy.layout.down(),
        desc="Move focus down in stack pane"
        ),
    Key([mod], "j",
        lazy.layout.up(),
        desc="Move focus up in stack pane"
        ),

    Key([mod, "shift"], "k",
        lazy.layout.shuffle_down(),
        desc='Shuffle down'
        ),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_up(),
        desc='Shuffle up'
        ),
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        desc='Shuffle left'
        ),
    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        desc='Shuffle right'
        ),
    Key([mod, "mod1"], "j",
        lazy.layout.flip_down(),
        desc='Flip down'
        ),
    Key([mod, "mod1"], "k",
        lazy.layout.flip_up(),
        desc='Flip up'
        ),
    Key([mod, "mod1"], "h",
        lazy.layout.flip_left(),
        desc='Flip left'
        ),
    Key([mod, "mod1"], "l",
        lazy.layout.flip_right(),
        desc='Flip right'
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        desc='Grow down'
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        desc='Grow up'
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        desc='Grow left'
        ),
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        desc='Grow right'
        ),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc='normalize window size ratios'
        ),
    Key([mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'
        ),
    Key([mod], "h",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
        ),
    Key([mod], "l",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
        ),

    # Toggle floating
    Key([mod, "shift"], "f", lazy.window.toggle_floating(),
        desc="Toggle floating"
        ),

    # Toggle Fullscreen
    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        lazy.hide_show_bar(position='all'),
        desc='Toggle fullscreen and the bars'
        ),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"
        ),

    # Swap panes of split stack
    Key([mod, "shift"], "space",
        lazy.layout.rotate(),
        desc="Swap panes of split stack"
        ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"
        ),
    Key([mod], "Return",
        lazy.spawn(terminal),
        desc="Launch terminal"
        ),

    # Toggle between different layouts as defined below
    Key([mod], "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"
        ),
    Key([mod], "w",
        lazy.window.kill(),
        desc="Kill focused window"
        ),

    # Toggle bars
    Key([mod], "b",
        lazy.hide_show_bar(position='all'),
        desc="Toggle bars"
        ),

    # Qtile system keys
    Key([mod, "shift", "control"], "l",
        lazy.spawn("betterlockscreen -l"),
        desc="Lock screen"
        ),
    Key([mod, "control"], "r",
        lazy.restart(),
        desc="Restart qtile"
        ),
    Key([mod, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown qtile"
        ),
    Key([mod], "r",
        lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"
        ),
    Key([mod, "control"], "p",
        lazy.spawn("" + home + "/.local/bin/powermenu"),
        desc="Launch Power menu"
        ),

    # Rofi
    Key(["control"], "space",
        lazy.spawn("rofi -show drun"),
        desc="Launch Rofi menu"
        ),

    # Cycle through windows in the floating layout
    Key([mod, "shift"], "i",
        lazy.window.toggle_minimize(),
        lazy.group.next_window(),
        lazy.window.bring_to_front()
        ),

    # ------------ Hardware Configs ------------
    # Volume
    Key([], "XF86AudioMute",
        lazy.spawn(home + "/.local/bin/statusbar/volumecontrol mute"),
        desc='Mute audio'
        ),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn(home + "/.local/bin/statusbar/volumecontrol down"),
        desc='Volume down'
        ),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn(home + "/.local/bin/statusbar/volumecontrol up"),
        desc='Volume up'
        ),

    # Media keys
    Key([], "XF86AudioPlay",
        lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.PlayPause"),
        desc='Audio play'
        ),
    Key([], "XF86AudioNext",
        lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.Next"),
        desc='Audio next'
        ),
    Key([], "XF86AudioPrev",
        lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.Previous"),
        desc='Audio previous'
        ),

    # Brightness
    Key([], "XF86MonBrightnessDown",
        lazy.spawn(home + "/.local/bin/statusbar/brightnesscontrol down"),
        desc='Brightness down'
        ),
    Key([], "XF86MonBrightnessUp",
        lazy.spawn(home + "/.local/bin/statusbar/brightnesscontrol up"),
        desc='Brightness up'
        ),

    # Screenshots
    # Save screen to clipboard
    Key([], "Print",
        lazy.spawn("/usr/bin/escrotum -C"),
        desc='Save screen to clipboard'
        ),
    # Save screen to screenshots folder
    Key([mod], "Print",
        lazy.spawn("/usr/bin/escrotum " + home + "/Pictures/Screenshots/screenshot_%d_%m_%Y_%H_%M_%S.png"),
        desc='Save screen to screenshots folder'
        ),
    # Capture region of screen to clipboard
    Key([mod, "shift"], "s",
        lazy.spawn("/usr/bin/escrotum -Cs"),
        desc='Capture region of screen to clipboard'
        ),
]

# Groups with matches

workspaces = [
    {"name": " ₁", "key": "1", "matches": [Match(wm_class='firefox')], "layout": "monadtall"},
    {"name": " ₂", "key": "2", "matches": [Match(wm_class='kitty'), Match(wm_class='ranger')], "layout": "monadtall"},
    {"name": " ₃", "key": "3", "matches": [Match(wm_class='vim')], "layout": "monadtall"},
    {"name": " ₄", "key": "4", "matches": [Match(wm_class='telegram-desktop'), Match(wm_class='weechat')], "layout": "monadtall"},
    {"name": " ₅", "key": "5", "matches": [Match(wm_class='gimp-2.10')], "layout": "monadtall"},
    {"name": "阮 ₆", "key": "6", "matches": [Match(wm_class='spotify')], "layout": "monadtall"},
    {"name": " ₇", "key": "7", "matches": [Match(wm_class='libreoffice')], "layout": "monadtall"},
    {"name": " ₈", "key": "8", "matches": [Match(wm_class='newsboat')], "layout": "monadtall"},
    {"name": " ₉", "key": "9", "matches": [Match(wm_class='neomutt')], "layout": "monadtall"},
]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    layouts = workspace["layout"] if "layout" in workspace else None
    groups.append(Group(workspace["name"], matches=matches, layout=layouts))
    keys.append(Key([mod], workspace["key"], lazy.group[workspace["name"]].toscreen()))
    keys.append(Key([mod, "shift"], workspace["key"], lazy.window.togroup(workspace["name"])))

# Move window to screen with Mod, Alt and number


for i in range(monitors):
    keys.extend([Key([mod, "mod1"], str(i), lazy.window.toscreen(i))])

# DEFAULT THEME SETTINGS FOR LAYOUTS #
layout_theme = {"border_width": 3,
                "margin": 16,
                "border_focus": BLUE,
                "border_normal": BLACK
                }

layouts = [
    layout.MonadTall(**layout_theme, single_border_width=0),
    layout.Stack(num_stacks=2, **layout_theme),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    layout.Bsp(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Floating(**layout_theme),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='FiraCode Nerd Font Regular',
    fontsize='12',
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = []

for monitor in range(monitors):
    if monitor == 0:
        screens.append(
            Screen(
                top=bar.Bar(
                    [
                        widget.Spacer(length=10),
                        widget.GroupBox(borderwidth=2, inactive='969696', this_current_screen_border='eee8d5', this_screen_border='eee8d5', font='FiraCode Nerd Font', fontsize=18, highlight_method='line', highlight_color=['00000000', '00000000']),
                        widget.CurrentLayoutIcon(scale=0.7),
                        widget.CurrentLayout(**widget_defaults),
                        widget.Prompt(**widget_defaults),
                        widget.Spacer(),
                        widget.GenPollText(func=custom_date, update_interval=1, **widget_defaults, mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/calendar.sh show"), shell=True), 'Button3': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/calendar.sh edit"), shell=True)}),
                        widget.Spacer(),
                        widget.CheckUpdates(
                            **widget_defaults,
                            update_interval=1800,
                            distro='Arch_yay',
                            custom_command='checkupdates;paru -Qum',
                            display_format=' {updates}',
                            colour_have_updates=GREEN,
                            execute='kitty -e paru',
                        ),
                        widget.Mpris2(
                            name='spotify',
                            objname="org.mpris.MediaPlayer2.spotify",
                            display_metadata=['xesam:title', 'xesam:artist'],
                            scroll_chars=None,
                            stop_pause_text='',
                            **widget_defaults
                        ),
                        widget.Systray(),
                        widget.GenPollText(update_interval=1, **widget_defaults, func=lambda: subprocess.check_output(os.path.expanduser("~/.local/bin/statusbar/brightnesscontrol")).decode(), mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/brightnesscontrol down"), shell=True), 'Button3': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/brightnesscontrol up"), shell=True)}),
                        widget.Spacer(length=5),
                        widget.GenPollText(update_interval=1, **widget_defaults, func=lambda: subprocess.check_output(os.path.expanduser("~/.local/bin/statusbar/volumecontrol")).decode(), mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/volumecontrol down"), shell=True), 'Button2': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/volumecontrol mute"), shell=True), 'Button3': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/volumecontrol up"), shell=True)}),
                        widget.Spacer(length=5),
                        widget.GenPollText(update_interval=1, **widget_defaults, func=lambda: subprocess.check_output(os.path.expanduser("~/.local/bin/statusbar/battery.py")).decode(), mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/battery.py --c left-click"), shell=True)}),
                        widget.Spacer(length=5),
                        widget.GenPollText(update_interval=1, **widget_defaults, func=lambda: subprocess.check_output(os.path.expanduser("~/.local/bin/statusbar/network.sh")).decode(), mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/network.sh ShowInfo"), shell=True), 'Button3': lambda: qtile.cmd_spawn(terminal + ' -e nmtui', shell=True)}),
                        widget.Spacer(length=10),
                    ],
                    28, background="#000000AA", margin=[10, 16, 0, 16]  # N E S W
                ),
            )
        )
else:
    screens.append(
        Screen(
            top=bar.Bar(
                [
                    widget.Spacer(),
                    widget.GenPollText(func=custom_date, update_interval=1, **widget_defaults, mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/calendar.sh show"), shell=True), 'Bu      tton3': lambda: qtile.cmd_spawn(os.path.expanduser("~/.local/bin/statusbar/calendar.sh edit"), shell=True)}),
                    widget.Spacer(),
                ],
                28, background="000000AA", margin=[10, 16, 0, 16]  # N E S W
            ),
        )
    )


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # *layout.Floating.default_float_rules,
    Match(title='Quit and close tabs?'),
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='Conky'),
    Match(wm_class='Firefox'),
    Match(wm_class='file_progress'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
