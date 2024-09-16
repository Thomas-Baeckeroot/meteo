#!/bin/bash

# Configuration
config_file="$HOME/.config/susanoo_WeatherStation.conf"
base_captures_folder="captures"

# Step 1: Read the MeteoFolder from the config file
METEO_FOLDER=$(grep "MeteoFolder" "$config_file" | cut -d'=' -f2 | tr -d ' ')

# Combine the METEO_FOLDER with the base captures folder
captures_dir="${METEO_FOLDER}${base_captures_folder}"
printf -- "Will remove oldest sub-folder from path %s" "${captures_dir}"

# Step 2: Function to check disk usage
check_disk_usage() {
    df / | awk 'NR==2 {print $5}' | tr -d '%'
}

# Step 3: Remove oldest folder function
remove_oldest_folder() {
    # Find the oldest folder (3 levels deep), sorted by modification time (ctime)
    oldest_folder=$(find "$captures_dir" -mindepth 3 -maxdepth 3 -type d -printf '%T+ %p\n' | sort | head -n 1 | awk '{print $2}')

    if [ -n "${oldest_folder}" ]; then
        printf -- "Removing oldest folder: %s\n" "${oldest_folder}"
        rm -rf "${oldest_folder}"
    else
        printf -- "No more folders to delete.\n"
        exit 1
    fi
}

# Step 4: Main loop - Check if disk usage exceeds 80%

# In order to adda limit:
# max_iterations=10
# current_iteration=0
while [ "$(check_disk_usage)" -gt 80 ]; do
    # && [ "$current_iteration" -lt "$max_iterations" ]
    printf -- "Disk usage is over 80%%. Proceeding to remove the oldest folder.\n"

    # Step 5: Call the function to remove the oldest folder
    remove_oldest_folder

    # Increment the iteration counter
    # current_iteration=$((current_iteration + 1))

    # Pause for a moment before checking again
    sleep 2
done

printf -- "Disk usage is now under control.\n"
