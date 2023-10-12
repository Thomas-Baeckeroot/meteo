#!/usr/bin/env bash
# Helper functions:

function fail {
    # Usage:
    # fail "Failed because xyz" 42
    printf -- '%s\n' "$1" >&2 ## Send message to stderr.
    exit "${2-1}" ## Return a code specified by $2, or 1 by default.
}

function apt_install_or_skip {
    # Usage:
	# apt_install_or_skip "modules pack1 and pack2" mod_pack1 mod_pack2
	if [ "$package_tool_ok" = true ]
	then
		sudo apt install -y ${@:2}
		printf -- "Installing $1...\n"
	else
		printf -- "Skipping $1...\n"
		# PROCEED FROM HERE # PROCEED FROM HERE# PROCEED FROM HERE# PROCEED FROM HERE# PROCEED FROM HERE #
	fi
}

