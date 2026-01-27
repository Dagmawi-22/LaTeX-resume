# AI-Powered Resume Builder

Automatically generate ATS-optimized, professional resumes tailored to specific job descriptions using Claude AI.

## Features

- **Multi-Agent AI System**: 4 specialized AI agents work together for perfect JD-resume harmony
  - **Agent 1**: Deep job description analysis
  - **Agent 2**: Initial resume generation
  - **Agent 3**: Iterative refinement
  - **Agent 4**: ATS validation & scoring
- **ATS Optimization**: Automatically extracts and incorporates keywords from job descriptions
- **AI-Powered Tailoring**: Uses Claude Sonnet 4 to customize your resume for each application
- **Professional PDF Output**: Generates clean, professional LaTeX-based PDFs
- **Space Efficient**: Automatically fits content in 1-2 pages with optimal space usage
- **Keyword Density**: Ensures proper keyword placement without stuffing
- **Quantifiable Results**: Emphasizes metrics and achievements
- **One-Command Generation**: Simple CLI interface
- **ATS Score**: Get a compatibility score (0-100) for each generated resume

## Prerequisites

### Required

1. **Python 3.8+**
   ```bash
   python3 --version
   ```

2. **Anthropic API Key**
   - Get your key from: https://console.anthropic.com/
   - Set up billing if not already done

3. **LaTeX Distribution** (for PDF generation)
   - **macOS**:
     ```bash
     brew install --cask mactex-no-gui
     ```
   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get install texlive-latex-base texlive-latex-extra
     ```
   - **Windows**: Download MiKTeX from https://miktex.org/

## Installation

1. **Clone or navigate to the repository**
   ```bash
   cd /path/to/my-resume
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
   ```

4. **Configure your resume data**

   Your personalized `config.json` is already set up! You can edit it anytime to:
   - Update your contact information
   - Add new experiences or projects
   - Update skills
   - Add certifications

## Usage

### Basic Usage

```bash
python resume_builder.py "job description text here"
```

### Using a Job Description File

```bash
python resume_builder.py job_description.txt
```

### Custom Output Name

```bash
python resume_builder.py job_description.txt -o senior_developer_role
```

### Full Example

1. **Create a job description file** (e.g., `job_posting.txt`):
   ```
   Senior Full-Stack Developer

   We're looking for an experienced full-stack developer with expertise in React,
   Node.js, and cloud infrastructure. The ideal candidate will have...
   ```

2. **Generate your resume**:
   ```bash
   python resume_builder.py job_posting.txt -o google_senior_dev
   ```

3. **Find your resume**:
   ```
   output/google_senior_dev.pdf
   ```

## How It Works

### Multi-Agent Pipeline

**Agent 1: Job Description Analysis** (15-20 seconds)
   - Extracts must-have vs nice-to-have requirements
   - Identifies critical ATS keywords
   - Analyzes technologies, soft skills, action verbs
   - Determines seniority level and role focus
   - Maps success metrics and responsibilities

**Agent 2: Initial Resume Generation** (30-40 seconds)
   - Creates tailored professional summary
   - Selects and reorders relevant experiences
   - Rewrites achievement bullets with impact focus
   - Incorporates all critical keywords naturally
   - Matches tone and seniority level
   - Quantifies achievements with metrics

**Agent 3: Resume Refinement** (30-40 seconds)
   - Strengthens keyword alignment
   - Enhances bullet points for maximum impact
   - Improves readability and flow
   - Ensures all must-have requirements are highlighted
   - Verifies 1-2 page constraint
   - Replaces em dashes with hyphens

**Agent 4: ATS Validation** (10-15 seconds)
   - Validates all critical keywords are present
   - Checks formatting compatibility
   - Calculates ATS score (0-100)
   - Identifies missing keywords
   - Provides improvement recommendations
   - Rates compatibility level

**Final Output**:
   - Professional LaTeX file (.tex)
   - ATS-optimized PDF resume
   - Detailed ATS validation report

## Output Files

After running the tool, you'll find in the `output/` directory:

- `resume_YYYYMMDD_HHMMSS.pdf` - Your final resume
- `resume_YYYYMMDD_HHMMSS.tex` - LaTeX source (for manual editing if needed)
- Auxiliary LaTeX files (.aux, .log, etc.)

## ATS Optimization Tips

The tool automatically handles:
- ✅ Standard section headings
- ✅ Simple, clean formatting
- ✅ Keyword optimization
- ✅ No special characters or graphics
- ✅ Proper use of hyphens (no em dashes)
- ✅ Industry-standard terminology

## Customization

### Modify the Template

Edit `templates/resume_template.tex` to:
- Change fonts or sizing
- Adjust margins
- Modify section order
- Customize styling

### Adjust AI Behavior

Edit the `_build_claude_prompt()` method in `resume_builder.py` to:
- Change the tone or style
- Add specific instructions
- Modify optimization criteria

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Make sure `.env` file exists in the project root
- Verify your API key is correctly set in `.env`

### "pdflatex not found"
- Install LaTeX using the instructions in Prerequisites
- On macOS, you may need to restart your terminal after installing

### PDF not generating
- Check `output/*.log` files for LaTeX errors
- The `.tex` file is still created and can be manually compiled
- Try compiling manually: `pdflatex output/resume_*.tex`

### Resume is too long
- The AI tries to fit content in 1-2 pages
- Edit `config.json` to remove less relevant experiences
- Modify the prompt to be more aggressive about space conservation

## Examples

### Example 1: Fintech Role
```bash
python resume_builder.py "Senior Backend Engineer for payment processing system" -o fintech_backend
```

### Example 2: Frontend Specialist
```bash
python resume_builder.py frontend_job.txt -o react_specialist
```

### Example 3: Full-Stack Position
```bash
python resume_builder.py <<EOF
Full-Stack Engineer position requiring React, Node.js, PostgreSQL,
AWS experience, and 3+ years building scalable web applications.
EOF
```

## Best Practices

1. **Paste the entire job description** - More context = better optimization
2. **Keep config.json updated** - Regular updates ensure accurate resumes
3. **Review before sending** - Always review the generated PDF
4. **Use specific output names** - Name files by company/role for organization
5. **Save job descriptions** - Keep a folder of job postings for future reference

## Project Structure

```
my-resume/
├── resume_builder.py       # Main script
├── config.json            # Your resume data (gitignored)
├── config.example.json    # Template for resume data
├── .env                   # API keys (gitignored)
├── .env.example           # Template for environment variables
├── requirements.txt       # Python dependencies
├── templates/
│   └── resume_template.tex  # LaTeX template
└── output/               # Generated resumes (PDFs gitignored)
    └── .gitkeep
```

## Cost Estimate

- Each resume generation uses ~10,000-15,000 tokens
- With Claude Sonnet 4: ~$0.03-0.05 per resume
- Very affordable for job searching!

## Tips for Best Results

1. **Include all job requirements** in your input
2. **Keep your config.json comprehensive** - more data = better tailoring
3. **Use different output names** for different applications
4. **Review keyword matches** in the console output
5. **Iterate if needed** - regenerate if the first attempt needs adjustment

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the example commands
3. Verify your prerequisites are installed correctly

## License

This is a personal automation tool. Use responsibly and always review generated content before submitting to employers.

---

**Happy job hunting!** 🚀
