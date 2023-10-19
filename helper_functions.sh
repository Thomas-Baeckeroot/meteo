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
	if [ "${package_tool_ok}" = true ]
	then
		printf -- "Installing %s...\n" "$1"
		sudo apt install -y ${@:2}
	else
		printf -- "Skipping %s.\n" "$1"
	fi
}

# Function to ask for a value with a default
ask_with_default() {
    local prompt="$1"
    local default_value="$2"
    local user_input

    # Display the prompt with the default value in square brackets
    read -r -p "${prompt} [${default_value}]: " user_input

    # Use the default value if no input is provided
    if [ -z "${user_input}" ]; then
        user_input="${default_value}"
    fi

    echo "${user_input}"
}

# Function to ask for a confirmation with a default choice
ask_confirmation() {
    local user_input
    user_input=$(ask_with_default "$1 (Y/n)" "$2")

    # Convert the user input to lowercase
    user_input=$(echo "${user_input}" | tr '[:upper:]' '[:lower:]')

    # Check if the user confirmed (yes or y)
    [ "${user_input}" = "y" ] || [ "${user_input}" = "yes" ]
}

# Create symbolic link ${link_file} pointing to ${target_file}
create_link() {
  local target_file="$1"  # file targeted by link
  local link_file  # link to be created
  link_file="$2"

  # sudo runuser --login --command "ln -f -s ${HOME}/meteo/src/main/py/home_web/index.html.py ${HOME}/../${WEB_USER}/index.html"
  # Used to be the upper. Why complicated?
  # no command "runuser" on Synology NAS,
  sudo ln -f -s "${target_file}" "${link_file}"
  sudo chmod 755 "${link_file}"
}
