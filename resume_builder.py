#!/usr/bin/env python3
"""
AI-Powered Resume Builder
Automatically generates ATS-optimized resumes tailored to job descriptions using Claude AI.
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()


class ResumeBuilder:
    """Main class for building ATS-optimized resumes."""

    def __init__(self, config_path: str = "config.json"):
        """Initialize the resume builder."""
        self.config_path = config_path
        self.config = self._load_config()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.template_dir = Path("templates")
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        """Load user configuration from JSON file."""
        if not os.path.exists(self.config_path):
            print(f"Error: Configuration file '{self.config_path}' not found.")
            print("Please copy 'config.example.json' to 'config.json' and fill in your information.")
            sys.exit(1)

        with open(self.config_path, 'r') as f:
            return json.load(f)

    def _read_job_description(self, job_desc_input: str) -> str:
        """Read job description from file or string."""
        if os.path.isfile(job_desc_input):
            with open(job_desc_input, 'r') as f:
                return f.read()
        return job_desc_input

    def _build_claude_prompt(self, job_description: str) -> str:
        """Build the prompt for Claude to generate optimized resume content."""
        config_json = json.dumps(self.config, indent=2)

        prompt = f"""You are an expert resume writer and ATS (Applicant Tracking System) optimization specialist. Your task is to create a highly optimized, professional resume that will achieve the highest possible ATS score while being compelling to human readers.

**Job Description:**
{job_description}

**Candidate's Information:**
{config_json}

**Requirements:**
1. **ATS Optimization:**
   - Extract ALL relevant keywords from the job description
   - Use exact keyword matches where appropriate
   - Include industry-standard terms and acronyms
   - Ensure proper keyword density without stuffing
   - Use standard section headings (Experience, Education, Skills, etc.)

2. **Content Quality:**
   - Tailor the professional summary to this specific role
   - Rewrite/reorder experience bullet points to emphasize relevant skills
   - Quantify achievements with metrics wherever possible
   - Use strong action verbs (Led, Developed, Implemented, Achieved, etc.)
   - Focus on impact and results, not just responsibilities
   - Keep language professional and concise

3. **Formatting Requirements:**
   - Content must fit in 1-2 pages maximum (prefer 1 page if possible)
   - Use hyphens (-) instead of em dashes or en dashes
   - No special characters that might confuse ATS systems
   - Efficient use of space while maintaining readability
   - Prioritize most relevant experience and skills

4. **Selection Criteria:**
   - If candidate has extensive experience, select the 3-4 most relevant positions
   - Choose projects that align with the job requirements
   - Highlight skills that match the job description
   - Include only relevant certifications

**Output Format:**
Provide your response as a JSON object with the following structure:

{{
  "professional_summary": "Tailored 2-3 sentence professional summary",
  "experience": [
    {{
      "company": "Company Name",
      "position": "Job Title",
      "location": "City, State",
      "start_date": "Mon YYYY",
      "end_date": "Mon YYYY or Present",
      "achievements": [
        "Tailored achievement bullet point 1",
        "Tailored achievement bullet point 2",
        "Tailored achievement bullet point 3"
      ]
    }}
  ],
  "education": [
    {{
      "institution": "University Name",
      "degree": "Degree Name",
      "location": "City, State",
      "graduation_date": "Mon YYYY",
      "gpa": "X.X/4.0 (optional)",
      "honors": "Honor if applicable"
    }}
  ],
  "skills": {{
    "category1": ["skill1", "skill2"],
    "category2": ["skill1", "skill2"]
  }},
  "projects": [
    {{
      "name": "Project Name",
      "description": "Brief relevant description",
      "technologies": ["Tech1", "Tech2"]
    }}
  ],
  "certifications": [
    {{
      "name": "Certification Name",
      "issuer": "Issuing Organization",
      "date": "YYYY"
    }}
  ],
  "ats_keywords_used": ["keyword1", "keyword2", "keyword3"],
  "optimization_notes": "Brief explanation of key optimizations made"
}}

**Important:** Only include sections with relevant content. If projects or certifications aren't relevant, use empty arrays. Ensure all text uses hyphens (-) instead of em dashes or en dashes."""

        return prompt

    def _analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """Agent 1: Deep analysis of job description."""
        print("\n[Agent 1/4] Analyzing job description...")

        prompt = f"""You are a job description analysis expert. Analyze this job posting in extreme detail.

**Job Description:**
{job_description}

Extract and categorize:
1. **Must-have requirements** (hard requirements)
2. **Nice-to-have requirements** (preferred qualifications)
3. **Key technologies and tools** mentioned
4. **Soft skills** and competencies
5. **Action verbs and industry terms** used
6. **Seniority level indicators**
7. **Core responsibilities**
8. **Success metrics or KPIs** mentioned
9. **Company culture indicators**
10. **ATS keywords** (terms that should appear in resume)

Output as JSON:
{{
  "must_have": ["requirement1", "requirement2"],
  "nice_to_have": ["skill1", "skill2"],
  "technologies": ["tech1", "tech2"],
  "soft_skills": ["skill1", "skill2"],
  "action_verbs": ["verb1", "verb2"],
  "seniority_level": "Junior|Mid|Senior|Lead|Principal",
  "core_responsibilities": ["resp1", "resp2"],
  "success_metrics": ["metric1", "metric2"],
  "culture_keywords": ["keyword1", "keyword2"],
  "ats_critical_keywords": ["keyword1", "keyword2"],
  "role_focus": "Brief summary of what role prioritizes"
}}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            analysis = json.loads(content)
            print(f"  ✓ Identified {len(analysis.get('must_have', []))} must-have requirements")
            print(f"  ✓ Found {len(analysis.get('ats_critical_keywords', []))} critical ATS keywords")
            print(f"  ✓ Role focus: {analysis.get('role_focus', 'N/A')}")

            return analysis

        except Exception as e:
            print(f"Error in job analysis: {e}")
            return {}

    def _generate_initial_resume(self, job_description: str, jd_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Agent 2: Generate initial resume draft."""
        print("\n[Agent 2/4] Generating initial resume draft...")

        config_json = json.dumps(self.config, indent=2)
        analysis_json = json.dumps(jd_analysis, indent=2)

        prompt = f"""You are an expert resume writer. Create an ATS-optimized resume draft.

**Job Description:**
{job_description}

**JD Analysis:**
{analysis_json}

**Candidate Information:**
{config_json}

**Instructions:**
1. Tailor professional summary to match role focus
2. Select and reorder experiences to emphasize relevant skills
3. Rewrite achievement bullets using action verbs from JD
4. Incorporate ALL critical ATS keywords naturally
5. Match seniority level and tone
6. Quantify achievements wherever possible
7. Highlight technologies and tools from must-have list
8. Keep content 1-2 pages max
9. Use hyphens (-) not em dashes
10. Ensure keyword density without stuffing

Output as JSON with this structure:
{{
  "professional_summary": "2-3 sentences tailored to role",
  "experience": [
    {{
      "company": "Company Name",
      "position": "Job Title",
      "location": "City, State",
      "start_date": "Mon YYYY",
      "end_date": "Mon YYYY or Present",
      "achievements": ["Achievement 1", "Achievement 2", "Achievement 3"]
    }}
  ],
  "education": [...],
  "skills": {{"category": ["skill1", "skill2"]}},
  "projects": [...],
  "certifications": [...],
  "ats_keywords_used": ["keyword1", "keyword2"],
  "optimization_notes": "Key optimizations made"
}}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=16000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            resume_data = json.loads(content)
            print(f"  ✓ Generated resume with {len(resume_data.get('experience', []))} experiences")
            print(f"  ✓ Incorporated {len(resume_data.get('ats_keywords_used', []))} keywords")

            return resume_data

        except Exception as e:
            print(f"Error generating initial resume: {e}")
            sys.exit(1)

    def _refine_resume(self, resume_data: Dict[str, Any], jd_analysis: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """Agent 3: Refine resume for perfect JD alignment."""
        print("\n[Agent 3/4] Refining resume for perfect JD harmony...")

        resume_json = json.dumps(resume_data, indent=2)
        analysis_json = json.dumps(jd_analysis, indent=2)

        prompt = f"""You are a resume refinement specialist. Review this resume and improve its alignment with the job description.

**Job Description:**
{job_description}

**JD Analysis:**
{analysis_json}

**Current Resume:**
{resume_json}

**Your Task:**
Analyze the resume and identify opportunities to:
1. Strengthen keyword alignment (check if ALL critical ATS keywords are present)
2. Improve achievement bullet points for impact and relevance
3. Enhance professional summary to better match role focus
4. Ensure technologies are prominently featured
5. Add quantifiable metrics where missing
6. Improve action verb usage
7. Better highlight must-have requirements
8. Ensure natural flow and readability
9. Verify content fits 1-2 pages
10. Check for em dashes and replace with hyphens

**Return the IMPROVED resume** in the same JSON format. Focus on making meaningful improvements while keeping the candidate's authentic experience.

Output the enhanced JSON resume with all improvements applied."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=16000,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            refined_resume = json.loads(content)
            print(f"  ✓ Refinement complete")
            print(f"  ✓ Enhanced keywords: {', '.join(refined_resume.get('ats_keywords_used', [])[:12])}...")

            return refined_resume

        except Exception as e:
            print(f"Warning: Refinement failed, using initial version: {e}")
            return resume_data

    def _validate_ats_compatibility(self, resume_data: Dict[str, Any], jd_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Agent 4: Final ATS validation and scoring."""
        print("\n[Agent 4/4] Performing ATS validation...")

        resume_json = json.dumps(resume_data, indent=2)
        analysis_json = json.dumps(jd_analysis, indent=2)

        prompt = f"""You are an ATS (Applicant Tracking System) validation expert. Analyze this resume for ATS compatibility.

**JD Critical Keywords:**
{analysis_json}

**Resume:**
{resume_json}

**Validation Checklist:**
1. Check if ALL critical ATS keywords from JD are present
2. Verify standard section headings are used
3. Check for ATS-unfriendly elements (special chars, graphics, tables)
4. Verify keyword density is appropriate (not stuffing)
5. Ensure formatting is ATS-parseable
6. Check for em dashes (should be hyphens)
7. Verify skills match job requirements
8. Confirm experience relevance
9. Calculate estimated ATS score (0-100)

Output as JSON:
{{
  "ats_score": 85,
  "keywords_matched": ["keyword1", "keyword2"],
  "keywords_missing": ["missing1"],
  "issues_found": ["issue1", "issue2"],
  "recommendations": ["rec1", "rec2"],
  "compatibility_level": "Excellent|Good|Fair|Poor",
  "summary": "Brief assessment"
}}"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            validation = json.loads(content)

            print(f"\n  ✓ ATS Score: {validation.get('ats_score', 'N/A')}/100")
            print(f"  ✓ Compatibility: {validation.get('compatibility_level', 'N/A')}")
            print(f"  ✓ Keywords matched: {len(validation.get('keywords_matched', []))}")

            if validation.get('keywords_missing'):
                print(f"  ⚠ Missing keywords: {', '.join(validation.get('keywords_missing', []))}")

            if validation.get('recommendations'):
                print(f"\n  Recommendations:")
                for rec in validation.get('recommendations', [])[:3]:
                    print(f"    - {rec}")

            return validation

        except Exception as e:
            print(f"Warning: ATS validation failed: {e}")
            return {"ats_score": "N/A", "compatibility_level": "Unknown"}

    def generate_resume_content(self, job_description: str) -> Dict[str, Any]:
        """Multi-agent resume generation with refinement."""
        print("\n" + "="*70)
        print("AI MULTI-AGENT RESUME OPTIMIZATION".center(70))
        print("="*70)

        # Agent 1: Analyze JD
        jd_analysis = self._analyze_job_description(job_description)

        # Agent 2: Generate initial draft
        resume_data = self._generate_initial_resume(job_description, jd_analysis)

        # Agent 3: Refine for perfect alignment
        refined_resume = self._refine_resume(resume_data, jd_analysis, job_description)

        # Agent 4: Validate ATS compatibility
        validation = self._validate_ats_compatibility(refined_resume, jd_analysis)

        # Add validation results to resume data for reference
        refined_resume['ats_validation'] = validation

        print("\n" + "="*70)
        print("MULTI-AGENT OPTIMIZATION COMPLETE".center(70))
        print("="*70)

        return refined_resume

    def _format_experience_section(self, experiences: list) -> str:
        """Format experience section for LaTeX."""
        latex_items = []
        for exp in experiences:
            achievements = "\n".join([f"      \\resumeItem{{{item}}}" for item in exp['achievements']])

            latex_items.append(f"""  \\resumeSubheading
    {{{exp['company']}}}{{{exp['location']}}}
    {{{exp['position']}}}{{{exp['start_date']} - {exp['end_date']}}}
    \\begin{{itemize}}
{achievements}
    \\end{{itemize}}
    \\vspace{{2pt}}""")

        return "\n".join(latex_items)

    def _format_education_section(self, education: list) -> str:
        """Format education section for LaTeX."""
        latex_items = []
        for edu in education:
            details = edu['degree']
            if edu.get('gpa'):
                details += f", GPA: {edu['gpa']}"
            if edu.get('honors'):
                details += f", {edu['honors']}"

            latex_items.append(f"""  \\resumeSubheading
    {{{edu['institution']}}}{{{edu['location']}}}
    {{{details}}}{{{edu['graduation_date']}}}""")

        return "\n".join(latex_items)

    def _format_skills_section(self, skills: Dict[str, list]) -> str:
        """Format skills section for LaTeX."""
        skills_lines = []
        for category, items in skills.items():
            category_name = category.replace('_', ' ').title()
            skills_str = ", ".join(items)
            skills_lines.append(f"\\textbf{{{category_name}:}} {skills_str}")

        return " \\\\\n".join(skills_lines)

    def _format_projects_section(self, projects: list) -> str:
        """Format projects section for LaTeX."""
        if not projects:
            return ""

        latex_items = []
        for proj in projects:
            tech_str = ", ".join(proj['technologies'])
            latex_items.append(f"""  \\item[]
    \\textbf{{{proj['name']}}} - {{{tech_str}}} \\\\
    {proj['description']}""")

        section = f"""
% Projects
\\section{{Projects}}
\\begin{{itemize}}[leftmargin=0pt, label={{}}]
{chr(10).join(latex_items)}
\\end{{itemize}}"""

        return section

    def _format_certifications_section(self, certifications: list) -> str:
        """Format certifications section for LaTeX."""
        if not certifications:
            return ""

        cert_lines = []
        for cert in certifications:
            cert_lines.append(f"\\textbf{{{cert['name']}}} - {cert['issuer']}, {cert['date']}")

        section = f"""
% Certifications
\\section{{Certifications}}
{' \\\\ '.join(cert_lines)}"""

        return section

    def generate_latex(self, resume_data: Dict[str, Any], output_name: str) -> Path:
        """Generate LaTeX file from template and data."""
        print("\nGenerating LaTeX document...")

        # Read template
        template_path = self.template_dir / "resume_template.tex"
        with open(template_path, 'r') as f:
            template = f.read()

        # Format personal info
        personal = self.config['personal_info']
        links_parts = []
        if personal.get('linkedin'):
            links_parts.append(f"\\href{{https://{personal['linkedin']}}}{{{personal['linkedin']}}}")
        if personal.get('github'):
            links_parts.append(f"\\href{{https://{personal['github']}}}{{{personal['github']}}}")
        if personal.get('website'):
            links_parts.append(f"\\href{{https://{personal['website']}}}{{{personal['website']}}}")

        links = " $|$ ".join(links_parts)

        # Build summary section
        summary_section = f"""\\section{{Professional Summary}}
{resume_data['professional_summary']}"""

        # Replace placeholders
        latex_content = template.replace("{{NAME}}", personal['name'])
        latex_content = latex_content.replace("{{EMAIL}}", personal['email'])
        latex_content = latex_content.replace("{{PHONE}}", personal['phone'])
        latex_content = latex_content.replace("{{LOCATION}}", personal['location'])
        latex_content = latex_content.replace("{{LINKS}}", links)
        latex_content = latex_content.replace("{{SUMMARY_SECTION}}", summary_section)
        latex_content = latex_content.replace("{{EXPERIENCE_SECTION}}",
                                             self._format_experience_section(resume_data['experience']))
        latex_content = latex_content.replace("{{EDUCATION_SECTION}}",
                                             self._format_education_section(resume_data['education']))
        latex_content = latex_content.replace("{{SKILLS_SECTION}}",
                                             self._format_skills_section(resume_data['skills']))
        latex_content = latex_content.replace("{{PROJECTS_SECTION}}",
                                             self._format_projects_section(resume_data.get('projects', [])))
        latex_content = latex_content.replace("{{CERTIFICATIONS_SECTION}}",
                                             self._format_certifications_section(resume_data.get('certifications', [])))

        # Write LaTeX file
        output_tex = self.output_dir / f"{output_name}.tex"
        with open(output_tex, 'w') as f:
            f.write(latex_content)

        print(f"LaTeX file created: {output_tex}")
        return output_tex

    def compile_pdf(self, tex_file: Path) -> Optional[Path]:
        """Compile LaTeX to PDF."""
        print("\nCompiling PDF...")
        print("(This requires pdflatex to be installed)")

        try:
            # Run pdflatex twice for proper formatting
            for i in range(2):
                result = subprocess.run(
                    ["pdflatex", "-output-directory", str(self.output_dir),
                     "-interaction=nonstopmode", str(tex_file)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode != 0:
                    print(f"Warning: pdflatex returned non-zero exit code")
                    if i == 1:  # Only show error on second run
                        print("Error output:", result.stderr)

            pdf_file = tex_file.with_suffix('.pdf')

            if pdf_file.exists():
                print(f"\nSUCCESS! Resume generated: {pdf_file}")
                print(f"File size: {pdf_file.stat().st_size / 1024:.1f} KB")
                return pdf_file
            else:
                print("Error: PDF file was not created")
                return None

        except FileNotFoundError:
            print("\nError: pdflatex not found!")
            print("Please install LaTeX:")
            print("  - Mac: brew install --cask mactex-no-gui")
            print("  - Ubuntu: sudo apt-get install texlive-latex-base texlive-latex-extra")
            print("  - Windows: Download MiKTeX from https://miktex.org/")
            print(f"\nLaTeX source available at: {tex_file}")
            return None
        except subprocess.TimeoutExpired:
            print("Error: PDF compilation timed out")
            return None
        except Exception as e:
            print(f"Error compiling PDF: {e}")
            return None

    def build(self, job_description: str, output_name: Optional[str] = None) -> Optional[Path]:
        """Main build process."""
        if not output_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"resume_{timestamp}"

        # Generate content with Claude
        resume_data = self.generate_resume_content(job_description)

        # Generate LaTeX
        tex_file = self.generate_latex(resume_data, output_name)

        # Compile to PDF
        pdf_file = self.compile_pdf(tex_file)

        return pdf_file


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI-Powered Resume Builder - Generate ATS-optimized resumes with Claude AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using job description file
  python resume_builder.py job_description.txt

  # Using job description string
  python resume_builder.py "We are looking for a Senior Python Developer..."

  # Custom output name
  python resume_builder.py job_description.txt -o senior_dev_resume

  # Custom config file
  python resume_builder.py job_description.txt -c my_config.json
        """
    )

    parser.add_argument(
        "job_description",
        help="Job description (text string or path to file)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output filename (without extension)",
        default=None
    )
    parser.add_argument(
        "-c", "--config",
        help="Path to config file (default: config.json)",
        default="config.json"
    )

    args = parser.parse_args()

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found in environment")
        print("Please create a .env file with your API key:")
        print("  ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    # Build resume
    builder = ResumeBuilder(config_path=args.config)
    job_desc = builder._read_job_description(args.job_description)

    print("=" * 70)
    print("AI-Powered Resume Builder".center(70))
    print("=" * 70)
    print()

    pdf_file = builder.build(job_desc, args.output)

    if pdf_file:
        print("\n" + "=" * 70)
        print(f"Resume ready: {pdf_file}")
        print("=" * 70)
    else:
        print("\nResume generation completed with warnings.")
        print("Check the LaTeX file in the output directory.")


if __name__ == "__main__":
    main()
