#!/bin/bash

# Resume Build Helper Script
# Usage: ./build.sh <job_file> [output_name]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get arguments
JOB_FILE="$1"

# Check if job file is provided
if [ -z "$JOB_FILE" ]; then
    echo -e "${RED}Error: Please provide a job description file${NC}"
    echo ""
    echo "Usage: ./build.sh <job_file>"
    echo "Example: ./build.sh sample_job.txt"
    echo ""
    echo "Note: Output filename is automatically generated from the job title"
    echo "Format: Dagmawi-Teka-{Role-Title}-{timestamp}"
    exit 1
fi

# Check if job file exists
if [ ! -f "$JOB_FILE" ]; then
    echo -e "${RED}Error: Job file not found: $JOB_FILE${NC}"
    exit 1
fi

# Check if config.json exists
if [ ! -f "config.json" ]; then
    echo -e "${RED}Error: config.json not found${NC}"
    echo "Please copy config.example.json to config.json and fill in your details"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p output

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}           Resume Generation Helper${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Job file:${NC} $JOB_FILE"
echo ""
echo -e "${GREEN}✓ Configuration files found${NC}"
echo -e "${GREEN}✓ Output directory ready${NC}"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────${NC}"
echo -e "${YELLOW}Ready to generate resume!${NC}"
echo ""
echo "Next steps:"
echo "1. Use the slash command in Claude Code:"
echo "   /generate-resume j=$JOB_FILE"
echo ""
echo "2. Claude Code will:"
echo "   - Analyze the job description"
echo "   - Extract the role title automatically"
echo "   - Generate optimized resume content"
echo "   - Create LaTeX file at: output/Dagmawi-Teka-{Role}-{timestamp}.tex"
echo "   - Compile to PDF"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────${NC}"

# Export variables for use by other scripts
export JOB_FILE

echo ""
echo -e "${GREEN}Environment ready. Run the slash command above in Claude Code.${NC}"
