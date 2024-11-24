#!/bin/bash
echo "Initiating Kill Switch..."
echo "Terminating non-essential applications..."

# List of non-essential applications to kill
pkill -f "Google Chrome"
pkill -f "Firefox"
pkill -f "Spotify"
pkill -f "TextEdit"

echo "Kill Switch executed successfully."