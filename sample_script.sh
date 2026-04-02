#!/bin/bash

echo "Listing all files in the current directory:"
ls -la

echo "Showing current user:"
whoami

# A vulnerable command using user input unsafely
echo "Enter filename to view:"
read filename
cat "$filename"
