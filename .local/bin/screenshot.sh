#!/bin/bash


home=$(eval echo ~"$USER")

case $1 in
    selected-region)
        # Take a screenshot of the selected region
        grim -t jpeg -g "$(slurp)" "$home"/Pictures/Screenshots/"$(date +%Y-%m-%d_%H-%m-%s)".jpg
        ;;
    save-to-clipboard)
        # Take a screenshot and save it to the clipboard
        grim -g "$(slurp -d)" - | wl-copy
        ;;
    *)
        # Take a screenshot of the currently focused output and save it into screenshots
        output="$(qtile cmd-obj -o core -f eval -a "self._current_output.wlr_output.name" | awk -F"['']" '/,/{print $2}')"
        grim -o $output -t jpeg ~/Pictures/Screenshots/$(date +%Y-%m-%d_%H-%m-%s).jpg
        ;;
esac
