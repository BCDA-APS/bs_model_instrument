#!/usr/bin/env bash

full_name=$1

echo $full_name

repo=$(echo $full_name | awk -F '/' '{print $2}')

original_repo="BITS"


echo $repo
echo $original_repo

sed -i "s/$original_repo/$repo/g" README.md


rm -rf .github/workflows/init_repo.sh
rm -rf .github/workflows/init_repo.yml
