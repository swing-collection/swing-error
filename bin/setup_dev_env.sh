#!/usr/bin/env bash

# =============================================================================
# Script: setup_dev_env.sh
# =============================================================================
# This script sets up the development environment by installing required Python
# packages, setting up virtual environments, and ensuring all necessary tools
# are available.
# =============================================================================

# Function to display a message and exit on error
function exit_on_error {
    echo "Error: $1"
    exit 1
}

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || exit_on_error "Failed to create virtual environment."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || exit_on_error "Failed to activate virtual environment."

# Install required packages
echo "Installing required packages..."
pip install --upgrade pip || exit_on_error "Failed to upgrade pip."
pip install -r requirements.txt || exit_on_error "Failed to install required packages."

echo "Development environment setup completed successfully."
