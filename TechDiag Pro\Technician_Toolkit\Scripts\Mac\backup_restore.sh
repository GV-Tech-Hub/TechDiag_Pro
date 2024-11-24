#!/bin/bash
echo "Backup and Restore Script"

# Backup Example
echo "Backing up Documents..."
cp -R ~/Documents /Volumes/Backup/Documents

# Restore Example
echo "Restoring Documents..."
cp -R /Volumes/Backup/Documents ~/Documents

echo "Backup and Restore operations completed."