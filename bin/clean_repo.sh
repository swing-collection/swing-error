#!/usr/bin/env bash

# =============================================================================
# Script: clean_repo.sh
# =============================================================================
# This script cleans up the repository by removing Python cache files, build
# artifacts, and other unnecessary files.
# =============================================================================

# Function to display a message and exit on error
function exit_on_error {
    echo "Error: $1"
    exit 1
}

# Remove Python cache files
echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -r {} + || exit_on_error "Failed to remove Python cache files."

# Remove build artifacts
echo "Removing build artifacts..."
rm -rf build dist *.egg-info || exit_on_error "Failed to remove build artifacts."

# Remove Sphinx build directory
echo "Removing Sphinx documentation build directory..."
rm -rf docs/build || exit_on_error "Failed to remove Sphinx build directory."

echo "Repository cleaned successfully."
