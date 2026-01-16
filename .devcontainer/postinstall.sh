#!/bin/bash
# Post-installation script for Spotify Token Setup devcontainer
# Installs required Python packages

set -e

echo "=========================================="
echo "Spotify Token Generator Setup"
echo "=========================================="

# Install Python packages
echo "Installing spotifywebapipython..."
pip install spotifywebapipython -U

echo ""
echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""
echo "To generate your Spotify token, run:"
echo "  python setup_spotify_token.py"
echo ""
echo "This will:"
echo "  1. Download the official script"
echo "  2. Run the token generator"
echo "  3. Start a download server for easy file transfer"
echo ""
