#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Running Subway Model ===${NC}"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run setup_env.sh first${NC}"
    exit 1
fi

# Check if main module exists
if [ ! -f "src/main.py" ]; then
    echo -e "${RED}src/main.py not found!${NC}"
    echo -e "${YELLOW}Please ensure your main module is located at src/main.py${NC}"
    exit 1
fi

# Activate environment and run
echo -e "${YELLOW}Activating environment...${NC}"
source .venv/bin/activate

echo -e "${YELLOW}Running subway model...${NC}"
python -m src.main

echo -e "${GREEN}Execution complete${NC}"