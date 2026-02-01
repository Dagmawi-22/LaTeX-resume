# AI-Powered Resume Builder

**Claude Code slash command that generates ATS-optimized resumes in ~2 minutes.**

- **Input:** Job description text file
- **Output:** LaTeX file (`.tex`) + optional PDF
- **Process:** 4 AI agents analyze job → generate tailored resume → validate ATS compatibility
- **Cost:** ~$0.06 per resume

## Prerequisites

1. **Claude Code CLI** - https://docs.claude.com/en/docs/claude-code
2. **Python 3.8+** - `python3 --version`
3. **Anthropic API Key** - Get from https://console.anthropic.com/

**Optional:** LaTeX (for local PDF compilation) - Otherwise use Overleaf online

## Setup

```bash
# 1. Clone and install dependencies
git clone <repo-url> && cd my-resume
pip install -r requirements.txt

# 2. Authenticate Claude Code (if not done)
claude auth login

# 3. Edit config.json with your resume data
# - Contact info, work experience, projects, skills, education
```

## Usage

```bash
# Create job description file
cat > job.txt << 'EOF'
Senior Full-Stack Developer - Google
Requirements: 5+ years React/Node.js, TypeScript, AWS, microservices...
EOF

# Generate resume
/generate-resume job.txt

# Output: output/resume_YYYYMMDD_HHMMSS.tex (+ .pdf if LaTeX installed)
```

**What happens:**
1. Agent 1: Analyzes job, extracts keywords (15-20s)
2. Agent 2: Generates tailored resume (30-40s)
3. Agent 3: Refines content and keywords (30-40s)
4. Agent 4: Validates ATS compatibility, scores 0-100 (10-15s)

## Compiling to PDF

### Option 1: Local (Automatic)

Install LaTeX, PDF auto-generates:
```bash
# macOS
brew install --cask mactex-no-gui

# Ubuntu/Debian
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended

# Windows
# Download from https://miktex.org/
```

### Option 2: Online (No Installation)

1. Upload `.tex` to https://www.overleaf.com
2. Click **New Project** → **Upload Project**
3. Click **Recompile** → **Download PDF**

**Alternatives:** https://papeeria.com or https://latexbase.com

## Troubleshooting

**"ANTHROPIC_API_KEY not found"**
- Run `claude auth login` or set `export ANTHROPIC_API_KEY=sk-ant-xxx`

**"pdflatex not found"**
- Install LaTeX (see above) OR upload `.tex` to Overleaf

**Low ATS score (<80)**
- Include full job description (not summary)
- Update `config.json` with more detailed experiences
- Add missing keywords shown in console output

**Resume too long**
- Remove older/less relevant experiences from `config.json`

## Best Practices

- **Include complete job postings** - more context = better optimization
- **Keep config.json updated** - add new projects/achievements regularly
- **Organize job files** - create `jobs/` folder with descriptive names
- **Review before submitting** - always verify accuracy and formatting
- **Check ATS score** - aim for 80+, regenerate if needed

## License

Personal automation tool. Review all generated content before submitting to employers.
