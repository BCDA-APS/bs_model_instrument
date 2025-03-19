#!/usr/bin/env bash

full_name=$1

echo $full_name

repo=$(echo $full_name | awk -F '/' '{print $2}')

# Sanitize the repo name to be a valid Python package name
sanitized_repo=$(echo "$repo" | sed 's/[^a-zA-Z0-9_-]/_/g')

original_repo="APSBITS"

echo $sanitized_repo
echo $original_repo

sed -i "s/$original_repo/$sanitized_repo/g" README.md

# Call the create_new_instrument function
python3 -m apsbits.utils.create_new_instrument "${sanitized_repo}_instrument" "src/."

rm -rf .github/workflows/init_repo.sh
rm -rf .github/workflows/init_repo.yml
