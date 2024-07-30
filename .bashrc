#
# ~/.bashrc

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Use bash-completion, if available
[[ $PS1 && -f /usr/share/bash-completion/bash_completion ]] && \
    . /usr/share/bash-completion/bash_completion

source <(kitty + complete setup bash)

# Use fzf completion too
source /usr/share/bash-completion/completions/fzf

# If there are multiple matches for completion, Tab should cycle through them
bind 'TAB':menu-complete

# Display a list of the matching files
bind "set show-all-if-ambiguous on"

# Perform partial completion on the first Tab press,
# only start cycling full results on the second Tab press
bind "set menu-complete-display-prefix on"

# Colour autocomplete suggestions
bind "set colored-stats on"

# If bpytop is installed then alias top to bpytop 
[ -e /usr/bin/bpytop ] && alias top="/usr/bin/bpytop"
alias ls='ls --color=auto -hv --group-directories-first'
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'

# Only use aliases according to the TERM we are in
case $TERM in
  xterm*|konsole*)
     alias vim='nvim';
     alias ssh='kitty +kitten ssh';;
  linux)
    alias vim="nvim";;
  *)
esac

command -v bat > /dev/null && alias cat='bat --paging=never' 
alias wanip='dig +short myip.opendns.com @resolver1.opendns.com'

export PS1="\[$(tput bold)\]\[$(tput setaf 2)\][\u@\h \w]\\$ \[$(tput sgr0)\]"
export EDITOR="nvim"
export VISUAL="nvim"
export PATH=$PATH:~/.local/bin
export STARSHIP_CONFIG=~/.config/starship/config.toml
export BROWSER="qutebrowser"
export XDG_CONFIG_HOME="$HOME/.config"
export WEECHAT_HOME="$XDG_CONFIG_HOME/weechat"

# FZF default options
export FZF_DEFAULT_OPTS="--color='bg:#000000,bg+:#000000,info:#00EE00,border:#6B6B6B,spinner:#98BC99' \
        --color='hl:#719872,fg:#D9D9D9,header:#719872,fg+:#D9D9D9' \
        --color='pointer:#0000ff,marker:#E17899,prompt:#98BEDE,hl+:#98BC99'"

# startx if on matching VT
if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi

# If not in xterm don't start starship
case $TERM in
  xterm*|konsole*)
    eval "$(starship init bash)";;
  *)
esac

