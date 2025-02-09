#!/usr/bin/env bash

# =============================================================================
# Script: generate_docs.sh
# =============================================================================
# This script generates HTML documentation using Sphinx.
# =============================================================================

# Function to display a message and exit on error
function exit_on_error {
    echo "Error: $1"
    exit 1
}

# Check if Sphinx is installed
if ! command -v sphinx-build &> /dev/null; then
    exit_on_error "Sphinx is not installed. Please install it and try again."
fi

# Generate documentation
echo "Generating HTML documentation..."
sphinx-build -b html docs/source docs/build/html || exit_on_error "Failed to generate documentation."

echo "Documentation generated successfully."
