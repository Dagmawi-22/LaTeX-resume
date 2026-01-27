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
/generate-resume j=sample_job.txt
```

That's it! The role title is **automatically extracted** from the job description.
Output will be: `Dagmawi-Teka-{Role-Title}-{timestamp}.pdf`

### Method 2: Manual with Helper Script

```bash
# Prepare the environment
./build.sh sample_job.txt

# Then use the slash command shown in the output:
/generate-resume j=sample_job.txt
```

## Step 4: Get Your Resume

Check the `output/` directory:
```bash
ls -lh output/
```

Your resume will be named automatically:
- `output/Dagmawi-Teka-{Role}-{timestamp}.pdf` - Your final resume
- `output/Dagmawi-Teka-{Role}-{timestamp}.tex` - LaTeX source (for manual edits)

Example: `Dagmawi-Teka-Backend-Developer-20260127_153045.pdf`

## What to Expect

Claude Code will:

1. **Extract role title** automatically
   - Analyzes job description for role name
   - Generates filename: Dagmawi-Teka-{Role}-{timestamp}

2. **Analyze** the job description
   - Extract must-have requirements & ATS keywords
   - Identify role focus and key technologies

3. **Generate** optimized resume content
   - Tailor professional summary
   - Select most relevant experiences (reverse chronological)
   - Incorporate keywords naturally

4. **Create** LaTeX file
   - Format using the optimized template (Charter font)
   - Ensure proper spacing and page fitting (1-2 pages)

5. **Compile** to PDF
   - Run pdflatex twice for proper formatting
   - Clean up auxiliary files

6. **Validate** ATS compatibility
   - Provide ATS score estimate
   - List matched keywords
   - Give recommendations

## Tips for Best Results

1. **Include the entire job description** - More context = better optimization
2. **Keep config.json updated** - Add recent experiences and skills
3. **Review before sending** - Always check the generated PDF
4. **Save job descriptions** - Keep them as .txt files for reuse
5. **Use descriptive filenames** - Name job files clearly (e.g., `google-swe.txt`, `meta-backend.txt`)

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
/generate-resume j=meta_engineer.txt

# Role title automatically extracted as "Software-Engineer"
# Output: Dagmawi-Teka-Software-Engineer-{timestamp}.pdf

# 3. Your PDF is ready!
open output/Dagmawi-Teka-Software-Engineer-*.pdf
```

## Next Steps

- Try with different job descriptions
- Keep config.json updated with latest experience
- Save job files with clear names for easy organization
- Review each resume before sending

---

**Happy job hunting!**
