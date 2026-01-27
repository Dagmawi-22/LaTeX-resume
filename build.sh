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
TITLE="${2:-Resume}"
OUTPUT_NAME="Dagmawi-Teka-${TITLE}-$(date +%Y%m%d_%H%M%S)"

# Check if job file is provided
if [ -z "$JOB_FILE" ]; then
    echo -e "${RED}Error: Please provide a job description file${NC}"
    echo "Usage: ./build.sh <job_file> [title]"
    echo "Example: ./build.sh sample_job.txt Software-Engineer"
    echo "Output format: Dagmawi-Teka-{title}-{timestamp}"
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
echo -e "${YELLOW}Output name:${NC} $OUTPUT_NAME"
echo ""
echo -e "${GREEN}✓ Configuration files found${NC}"
echo -e "${GREEN}✓ Output directory ready${NC}"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────${NC}"
echo -e "${YELLOW}Ready to generate resume!${NC}"
echo ""
echo "Next steps:"
echo "1. Claude Code will analyze the job description"
echo "2. Generate optimized resume content"
echo "3. Create LaTeX file at: output/${OUTPUT_NAME}.tex"
echo "4. Compile to PDF using: node compile-resume.js output/${OUTPUT_NAME}.tex"
echo ""
echo -e "${BLUE}────────────────────────────────────────────────────────${NC}"

# Export variables for use by other scripts
export JOB_FILE
export OUTPUT_NAME

echo ""
echo -e "${GREEN}Environment ready. You can now use Claude Code to generate the resume.${NC}"
