#!/usr/bin/env bash

# =============================================================================
# Script: build_and_upload.sh
# =============================================================================
# This script automates the process of building a Python package and uploading
# it to PyPI. It removes the old `dist` directory, installs/updates necessary
# tools, creates a new build, and uploads it using Twine.
# =============================================================================

# Function to display a message and exit on error
function exit_on_error {
    echo "Error: $1"
    exit 1
}

# Remove dist folder if it exists
if [ -d "dist" ]; then
    echo "Deleting existing 'dist' directory..."
    rm -r dist || exit_on_error "Failed to delete 'dist' directory."
fi

# Install/update necessary tools
echo "Installing/updating tools (twine, setuptools, wheel)..."
python3 -m pip install --upgrade twine setuptools wheel || exit_on_error "Failed to install/update tools."

# Create new build
echo "Creating a new source distribution..."
python3 setup.py sdist || exit_on_error "Failed to create a new build."

# Upload new build to PyPI using Twine
echo "Uploading the new build to PyPI..."
python3 -m twine upload dist/* || exit_on_error "Failed to upload the build to PyPI."

echo "Build and upload completed successfully."
