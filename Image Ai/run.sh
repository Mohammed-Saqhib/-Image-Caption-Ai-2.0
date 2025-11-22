#!/bin/bash
# Script to run the Image AI Platform

# Ensure we are in the project directory
cd "$(dirname "$0")"

# Run the Streamlit app using python module to avoid PATH issues
python3 -m streamlit run src/app_enhanced.py
