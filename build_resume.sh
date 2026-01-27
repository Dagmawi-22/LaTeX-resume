#!/bin/bash

# Resume Builder with Claude Code
# Usage: ./build_resume.sh job_description.txt [output_name]

if [ -z "$1" ]; then
    echo "Usage: ./build_resume.sh <job_description_file> [output_name]"
    echo "Example: ./build_resume.sh job.txt senior_dev"
    exit 1
fi

JOB_DESC_FILE="$1"
OUTPUT_NAME="${2:-resume_$(date +%Y%m%d_%H%M%S)}"

if [ ! -f "$JOB_DESC_FILE" ]; then
    echo "Error: Job description file '$JOB_DESC_FILE' not found"
    exit 1
fi

if [ ! -f "config.json" ]; then
    echo "Error: config.json not found. Please create it from config.example.json"
    exit 1
fi

echo "======================================================================"
echo "                 AI Resume Builder with Claude Code"
echo "======================================================================"
echo ""
echo "Job Description: $JOB_DESC_FILE"
echo "Output Name: $OUTPUT_NAME"
echo ""
echo "Starting resume generation with Claude Code..."
echo ""

# Create a prompt file for Claude Code
PROMPT_FILE=".resume_prompt_tmp.txt"

cat > "$PROMPT_FILE" << 'EOF'
I need you to generate an ATS-optimized resume. Please follow these steps:

1. Read config.json for my resume data
2. Read the job description from: JOB_DESC_PLACEHOLDER
3. Analyze the job description deeply:
   - Extract must-have vs nice-to-have requirements
   - Identify ALL critical ATS keywords
   - Determine seniority level and role focus
   - List technologies, soft skills, action verbs

4. Generate an optimized resume that:
   - Tailors professional summary to the role
   - Selects and reorders relevant experiences
   - Rewrites achievements with strong action verbs and metrics
   - Incorporates ALL critical keywords naturally
   - Matches the tone and seniority level
   - Fits in 1-2 pages maximum
   - Uses hyphens (-) not em dashes
   - Is highly ATS-compatible

5. Create a LaTeX file at: output/OUTPUT_NAME_PLACEHOLDER.tex using the template at templates/resume_template.tex

6. Compile to PDF using pdflatex

7. Provide an ATS compatibility assessment:
   - ATS score estimate (0-100)
   - Keywords matched
   - Recommendations for improvement

Please be thorough and create the best possible resume for this job!
EOF

# Replace placeholders
sed -i.bak "s|JOB_DESC_PLACEHOLDER|$JOB_DESC_FILE|g" "$PROMPT_FILE"
sed -i.bak "s|OUTPUT_NAME_PLACEHOLDER|$OUTPUT_NAME|g" "$PROMPT_FILE"
rm -f "${PROMPT_FILE}.bak"

# Get the prompt content
PROMPT=$(cat "$PROMPT_FILE")

# Run Claude Code with the prompt
echo "$PROMPT" | claude

# Cleanup
rm -f "$PROMPT_FILE"

echo ""
echo "======================================================================"
echo "Resume generation complete!"
echo "Check: output/$OUTPUT_NAME.pdf"
echo "======================================================================"
