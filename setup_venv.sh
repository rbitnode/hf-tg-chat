#!/bin/bash

# Check if the .venv directory exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Activating virtual environment..."
fi

# Activate the virtual environment
source .venv/bin/activate

# Check if requirements.txt exists and install dependencies
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip3 install -r requirements.txt
else
  echo "requirements.txt not found. Skipping installation of dependencies."
fi
