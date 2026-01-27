#!/usr/bin/env python3
"""
Simple Resume Generator using Claude Code
This script prepares the prompt for Claude Code to generate your resume.
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


def read_file(filepath):
    """Read file content."""
    with open(filepath, 'r') as f:
        return f.read()


def generate_prompt(job_desc_file, output_name):
    """Generate the prompt for Claude Code."""

    # Read job description
    if not os.path.exists(job_desc_file):
        print(f"Error: Job description file '{job_desc_file}' not found")
        sys.exit(1)

    if not os.path.exists('config.json'):
        print("Error: config.json not found")
        sys.exit(1)

    job_desc = read_file(job_desc_file)

    prompt = f"""Generate an ATS-optimized resume for this job description.

**JOB DESCRIPTION:**
{job_desc}

**INSTRUCTIONS:**

## Stage 1: Analyze Job Description
Read config.json for my resume data, then deeply analyze this job description:
- Extract must-have vs nice-to-have requirements
- Identify ALL critical ATS keywords (aim for 25+ keywords)
- List technologies, tools, and frameworks mentioned
- Note soft skills and competencies
- Identify action verbs used
- Determine seniority level
- Map core responsibilities

Print a summary of your analysis.

## Stage 2: Generate Optimized Resume Content

Create resume content that:
1. Tailors professional summary to match role focus
2. Selects 3-4 most relevant experiences from config.json
3. Rewrites achievement bullets with:
   - Strong action verbs from the JD
   - Quantifiable metrics and impact
   - Natural keyword integration
   - 2-4 bullets per experience
4. Organizes skills by category (matching JD keywords)
5. Uses hyphens (-) never em dashes
6. Fits in 1-2 pages
7. Maintains professional, concise language

## Stage 3: Create LaTeX File

Using templates/resume_template.tex:
1. Replace all placeholders with content from config.json and generated resume
2. Format experience section with \\resumeSubheading
3. Format skills with \\textbf{{Category:}} items
4. Write to: output/{output_name}.tex

## Stage 4: Compile PDF

1. Compile with: pdflatex -output-directory output output/{output_name}.tex
2. Run twice for proper formatting

## Stage 5: ATS Validation Report

Provide:
- **ATS Score**: (0-100)
- **Keywords Matched**: (list top 20)
- **Keywords Missing**: (if any)
- **Compatibility**: Excellent/Good/Fair/Poor
- **Recommendations**: Top 3 suggestions

Create the complete resume PDF at: output/{output_name}.pdf"""

    return prompt


def main():
    parser = argparse.ArgumentParser(
        description="Generate prompt for Claude Code resume builder"
    )
    parser.add_argument("job_description", help="Path to job description file")
    parser.add_argument(
        "-o", "--output",
        help="Output filename (without extension)",
        default=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )

    args = parser.parse_args()

    # Ensure output directory exists
    Path("output").mkdir(exist_ok=True)

    prompt = generate_prompt(args.job_description, args.output)

    print("="*70)
    print("CLAUDE CODE RESUME BUILDER")
    print("="*70)
    print()
    print("Copy the prompt below and paste it into Claude Code:")
    print()
    print("-"*70)
    print(prompt)
    print("-"*70)
    print()
    print(f"Output will be saved to: output/{args.output}.pdf")
    print()


if __name__ == "__main__":
    main()
