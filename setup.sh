#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_NAME="subway-model"
VENV_NAME=".venv"
PYTHON_VERSION="3.12"

echo -e "${BLUE}=== Subway Model Environment Setup ===${NC}"
echo -e "${BLUE}Setting up environment for: $PROJECT_NAME${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if uv is installed
echo -e "${YELLOW}Checking for uv installation...${NC}"
if ! command_exists uv; then
    echo -e "${RED}Error: uv is not installed or not in PATH${NC}"
    echo -e "${YELLOW}Please install uv first:${NC}"
    echo -e "${YELLOW}  curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
    echo -e "${YELLOW}  Or visit: https://github.com/astral-sh/uv${NC}"
    exit 1
fi

echo -e "${GREEN} uv is installed${NC}"

# Check if Python 3.12+ is available
echo -e "${YELLOW}Checking Python version...${NC}"
if ! uv python list | grep -q "3.1[2-9]"; then
    echo -e "${YELLOW}Installing Python $PYTHON_VERSION...${NC}"
    uv python install $PYTHON_VERSION
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install Python $PYTHON_VERSION${NC}"
        exit 1
    fi
fi

echo -e "${GREEN} Python $PYTHON_VERSION is available${NC}"

# Check if virtual environment already exists
if [ -d "$VENV_NAME" ]; then
    echo -e "${YELLOW}Virtual environment already exists at $VENV_NAME${NC}"
    echo -e "${YELLOW}Do you want to recreate it? (y/N)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${YELLOW}Removing existing virtual environment...${NC}"
        rm -rf "$VENV_NAME"
    else
        echo -e "${BLUE}Using existing virtual environment${NC}"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_NAME" ]; then
    echo -e "${YELLOW}Creating virtual environment with Python $PYTHON_VERSION...${NC}"
    uv venv --python $PYTHON_VERSION
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment${NC}"
        exit 1
    fi
    echo -e "${GREEN} Virtual environment created${NC}"
fi

# Install dependencies from pyproject.toml
echo -e "${YELLOW}Installing dependencies from pyproject.toml...${NC}"
uv sync
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install dependencies${NC}"
    exit 1
fi

echo -e "${GREEN} Dependencies installed successfully${NC}"

# Verify installation
echo -e "${YELLOW}Verifying installation...${NC}"
source "$VENV_NAME/bin/activate"
python --version
echo -e "${GREEN} Environment verification complete${NC}"

# Create activation script
cat > activate_env.sh << 'EOF'
#!/bin/bash
source .venv/bin/activate
echo "Subway Model environment activated!"
echo "Python version: $(python --version)"
echo "To deactivate, run: deactivate"
EOF

chmod +x activate_env.sh

echo ""
echo -e "${GREEN}=== Setup Complete! ===${NC}"
echo -e "${GREEN}Your subway-model environment is ready to use.${NC}"
echo ""
echo -e "${BLUE}To activate the environment:${NC}"
echo -e "${BLUE}  source .venv/bin/activate${NC}"
echo -e "${BLUE}  Or run: ./activate_env.sh${NC}"
echo ""
echo -e "${BLUE}To run your project:${NC}"
echo -e "${BLUE}  python -m src.main${NC}"
echo ""
echo -e "${BLUE}To deactivate:${NC}"
echo -e "${BLUE}  deactivate${NC}"
echo ""
echo -e "${YELLOW}Note: Make sure your src/main.py file exists before running!${NC}"
