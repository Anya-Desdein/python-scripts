#!/bin/bash

CONF_FILE="/etc/modprobe.d/uvcvideo.conf"

if [ ! -f "$CONF_FILE" ]; then
	echo "options uvcvideo quirks=128" > "$CONF_FILE"
	exit 0
fi

sed -E '/^options[[:space:]]+uvcvideo/ {

	/quirks=/! {
		s/$/ quirks=128/
		b
	}

	/quirks=[0-9,]*128[,[:space:]]+/ b
	/quirks=[0-9,]*128$/ b

	s/(quirks=[0-9,]+)/\1,128/

} ' "$CONF_FILE"
