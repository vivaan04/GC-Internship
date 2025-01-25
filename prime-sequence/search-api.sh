#!/bin/bash

# Function to open links in Chrome using the Python script
open_links() {
  awk -F ': ' '{print $NF}' | python3 ./prime-sequence/open_select.py
}

# Prompt the user for the search query
read -p "Enter your search query: " search_query

# Build the curl command with the user's input - CORRECTED
# 1. Added proper quoting around the entire URL.
# 2. Correctly encoded spaces in the search query using command substitution.
links_output=$(curl -s "https://www.googleapis.com/customsearch/v1?key=$(cat ./prime-sequence/search-api-key.txt)&cx=$(cat ./prime-sequence/cx-id.txt)&q=$(echo "$search_query" | sed 's/\ /\+/g')" | jq -r '.items | .[] | .link' | sed 's/.*/link: &/')

# Print the extracted links
echo "Extracted Links:"
echo "$links_output"

# Ask the user if they want to open the links in Chrome
read -p "Open links in Chrome? (y/n): " open_choice

# If the user chooses 'y', open the links
if [[ "$open_choice" == "y" ]]; then
  echo "$links_output" | open_links
fi
