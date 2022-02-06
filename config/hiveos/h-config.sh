#!/usr/bin/env bash

[[ -z $CUSTOM_TEMPLATE ]] && echo -e "${YELLOW}CUSTOM_TEMPLATE is empty${NOCOLOR}" && return 1
[[ -z $CUSTOM_URL ]] && echo -e "${YELLOW}CUSTOM_URL is empty${NOCOLOR}" && return 1

echo "$CUSTOM_URL $CUSTOM_TEMPLATE" > $CUSTOM_CONFIG_FILENAME
