# Quick Start Guide

Get your first AI-optimized resume in 3 minutes!

## Step 1: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install LaTeX (choose your OS)
# macOS:
brew install --cask mactex-no-gui

# Ubuntu/Debian:
sudo apt-get install texlive-latex-base texlive-latex-extra

# Windows:
# Download from https://miktex.org/
```

## Step 2: Set Up API Key

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Anthropic API key
# Get your key from: https://console.anthropic.com/
nano .env  # or use any text editor
```

Your `.env` should look like:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx
```

## Step 3: Verify Your Config

Your personalized `config.json` is already set up with your resume data!

To update it:
```bash
# Edit your config
nano config.json  # or use any text editor
```

## Step 4: Generate Your First Resume

### Test with sample job description:
```bash
python resume_builder.py sample_job.txt -o fintech_role
```

### Or use a real job posting:
```bash
# Copy the job description to a file
nano job_posting.txt
# Paste the job description, save and exit

# Generate resume
python resume_builder.py job_posting.txt -o company_role_name
```

### Or paste directly:
```bash
python resume_builder.py "Senior Full-Stack Engineer with React, Node.js, AWS experience..."
```

## Step 5: Get Your Resume

Check the `output/` directory:
```bash
ls -lh output/
```

Your resume will be:
- `output/fintech_role.pdf` - Your final resume
- `output/fintech_role.tex` - LaTeX source (for manual edits)

## What to Expect

The multi-agent system will:

1. **[Agent 1/4]** Analyze the job description (15-20s)
   - Shows: Must-have requirements, ATS keywords, role focus

2. **[Agent 2/4]** Generate initial draft (30-40s)
   - Shows: Number of experiences, keywords incorporated

3. **[Agent 3/4]** Refine for perfect alignment (30-40s)
   - Shows: Enhanced keywords list

4. **[Agent 4/4]** Validate ATS compatibility (10-15s)
   - Shows: **ATS Score**, compatibility level, recommendations

**Total time: 90-120 seconds**

## Example Output

```
======================================================================
                  AI-Powered Resume Builder
======================================================================

======================================================================
              AI MULTI-AGENT RESUME OPTIMIZATION
======================================================================

[Agent 1/4] Analyzing job description...
  ✓ Identified 12 must-have requirements
  ✓ Found 24 critical ATS keywords
  ✓ Role focus: Backend scalability and payment systems

[Agent 2/4] Generating initial resume draft...
  ✓ Generated resume with 4 experiences
  ✓ Incorporated 28 keywords

[Agent 3/4] Refining resume for perfect JD harmony...
  ✓ Refinement complete
  ✓ Enhanced keywords: React, Node.js, PostgreSQL, AWS, Docker...

[Agent 4/4] Performing ATS validation...
  ✓ ATS Score: 92/100
  ✓ Compatibility: Excellent
  ✓ Keywords matched: 26

  Recommendations:
    - Strong alignment with job requirements
    - All critical keywords present
    - Resume well-optimized for ATS

======================================================================
            MULTI-AGENT OPTIMIZATION COMPLETE
======================================================================

Generating LaTeX document...
LaTeX file created: output/fintech_role.tex

Compiling PDF...
SUCCESS! Resume generated: output/fintech_role.pdf
File size: 42.3 KB

======================================================================
Resume ready: output/fintech_role.pdf
======================================================================
```

## Tips for Best Results

1. **Include the entire job description** - More context = better optimization
2. **Use descriptive output names** - `python resume_builder.py job.txt -o google_swe_l5`
3. **Review the ATS score** - Aim for 85+ for best results
4. **Check recommendations** - Agent 4 provides improvement suggestions
5. **Update config.json** - Keep your experiences and skills current

## Troubleshooting

### API Key Error
```
Error: ANTHROPIC_API_KEY not found in environment
```
**Fix**: Make sure `.env` file exists with your API key

### LaTeX Not Found
```
Error: pdflatex not found!
```
**Fix**: Install LaTeX using the commands in Step 1

### ATS Score Low (<70)
**Fix**:
- Check if job description is complete
- Update `config.json` with more relevant experiences
- Regenerate the resume

## Cost

Each resume costs approximately **$0.10-0.15** (using Claude Sonnet 4)
- Very affordable for job searching!
- 4 AI agent calls per resume

## Next Steps

- Try with different job descriptions
- Experiment with output names for organization
- Keep your `config.json` updated
- Review and customize generated resumes before sending

## Need Help?

Check the main [README.md](README.md) for:
- Detailed documentation
- More examples
- Customization options
- Template modifications

---

**Happy job hunting!** 🚀
