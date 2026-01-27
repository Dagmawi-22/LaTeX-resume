# Quick Start Guide

Get your first AI-optimized resume using Claude Code (no API key needed!)

## Step 1: Verify Dependencies

```bash
# Check if LaTeX is installed
which pdflatex

# If not installed (macOS only):
brew install --cask mactex-no-gui
```

## Step 2: Set Up Your Config

```bash
# Copy the example config
cp config.example.json config.json

# Edit with your details
nano config.json  # or use any text editor
```

## Step 3: Generate Your First Resume

### Method 1: Using the Slash Command (Easiest)

In Claude Code:
```
/generate-resume job_file=sample_job.txt output_name=Dagmawi-Teka-Software-Engineer-20260127_143022
```

### Method 2: Manual with Helper Script

```bash
# Prepare the environment (automatically generates name: Dagmawi-Teka-{title}-{timestamp})
./build.sh sample_job.txt Software-Engineer

# Then ask Claude Code:
# "Generate an ATS-optimized resume from sample_job.txt,
#  save LaTeX to output/Dagmawi-Teka-Software-Engineer-{timestamp}.tex"

# Compile to PDF
node compile-resume.js output/Dagmawi-Teka-Software-Engineer-*.tex
```

## Step 4: Get Your Resume

Check the `output/` directory:
```bash
ls -lh output/
```

Your resume will be:
- `output/my_resume.pdf` - Your final resume
- `output/my_resume.tex` - LaTeX source (for manual edits)

## What to Expect

Claude Code will:

1. **Analyze** the job description
   - Extract must-have requirements & ATS keywords
   - Identify role focus and key technologies

2. **Generate** optimized resume content
   - Tailor professional summary
   - Select most relevant experiences
   - Incorporate keywords naturally

3. **Create** LaTeX file
   - Format using the optimized template
   - Ensure proper page fitting (1-2 pages)

4. **Compile** to PDF
   - Run pdflatex twice for proper formatting
   - Clean up auxiliary files

5. **Validate** ATS compatibility
   - Provide ATS score estimate
   - List matched keywords
   - Give recommendations

## Tips for Best Results

1. **Include the entire job description** - More context = better optimization
2. **Use descriptive output names** - e.g., `google_swe_l5`, `acme_backend_2026`
3. **Keep config.json updated** - Add recent experiences and skills
4. **Review before sending** - Always check the generated PDF
5. **Save job descriptions** - Keep them as .txt files for reuse

## Troubleshooting

### LaTeX Not Found
```
✗ Error: pdflatex not found!
```
**Fix**: Install LaTeX (macOS: `brew install --cask mactex-no-gui`)

### Config Not Found
```
Error: config.json not found
```
**Fix**: Copy config.example.json to config.json and fill in your details

### Resume Too Long
**Fix**:
- Edit config.json to remove less relevant experience
- Ask Claude Code to be more concise
- Select only 3-4 most relevant positions

### Compilation Errors
**Fix**: Check the .log file in output/ for LaTeX errors

## Key Features

- **No API costs** - Uses Claude Code directly (free!)
- **Fast compilation** - Node.js tools for quick PDF generation
- **Smart page fitting** - Optimized LaTeX template
- **ATS optimized** - Keyword extraction and proper formatting
- **Lightweight** - Minimal dependencies

## Example Workflow

```bash
# 1. Save job description
cat > meta_engineer.txt << 'EOF'
Software Engineer, Infrastructure
Requirements: Go, Kubernetes, distributed systems...
EOF

# 2. Generate resume (in Claude Code)
/generate-resume job_file=meta_engineer.txt output_name=Dagmawi-Teka-Meta-Infrastructure-20260127_143022

# 3. Your PDF is ready!
open output/Dagmawi-Teka-Meta-Infrastructure-*.pdf
```

## Next Steps

- Try with different job descriptions
- Keep config.json updated with latest experience
- Experiment with output names for organization
- Review each resume before sending

---

**Happy job hunting!**
