#!/bin/bash

WIN_CLASS="WebApp-ChatGPT4319"

# pega ID HEX da janela alvo
WIN_HEX=$(wmctrl -lx | awk -v wc="$WIN_CLASS" '$3~wc {print $1; exit}')

# se não existe → abrir webapp
if [ -z "$WIN_HEX" ]; then
    google-chrome-stable --app="https://chatgpt.com/" \
    --class=WebApp-ChatGPT4319 \
    --name=WebApp-ChatGPT4319 \
    --user-data-dir=/home/diego/.local/share/ice/profiles/ChatGPT4319 &
    exit
fi

# pega janela ativa (decimal)
ACTIVE_DEC=$(xdotool getactivewindow 2>/dev/null)

# converte décimal → hex no padrão wmctrl (0xXXXXXXXX)
ACTIVE_HEX=$(printf "0x%08x" "$ACTIVE_DEC")

# se a janela ativa é a do chatgpt → minimizar
if [ "$ACTIVE_HEX" == "$WIN_HEX" ]; then
    xdotool windowminimize "$ACTIVE_DEC"
else
    wmctrl -ia "$WIN_HEX"
fi

