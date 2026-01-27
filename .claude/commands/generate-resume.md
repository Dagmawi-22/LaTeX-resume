---
description: Generate an ATS-optimized resume from a job description
---

You are an expert resume optimization system with 4 specialized analysis stages.

Read the job description from: {{j}}
Read my resume data from: config.json
Use the LaTeX template from: templates/resume_template.tex

## STAGE 0: Extract Job Title

From the job description, extract the role title (e.g., "Software-Engineer", "Backend-Developer", "Node.js-Developer").
Generate output filename as: Dagmawi-Teka-{Role-Title}-{timestamp}
Format: Use hyphens, capitalize properly, keep concise (2-3 words max)

Example titles:
- "Senior Software Engineer" → "Senior-Software-Engineer"
- "Backend Developer - Node.js" → "Backend-Developer"
- "Full Stack Engineer" → "Full-Stack-Engineer"

## STAGE 1: Deep Job Analysis

Analyze the job description and extract:
- Must-have requirements vs nice-to-have
- All critical ATS keywords (minimum 20)
- Technologies, tools, frameworks mentioned
- Soft skills and competencies required
- Action verbs used in the JD
- Seniority level indicators
- Core responsibilities
- Success metrics mentioned

Print your analysis.

## STAGE 2: Resume Generation

Create an optimized resume that:
1. Tailors the professional summary to match the role focus
2. Selects 3-4 most relevant experiences from my background
3. **ORDERS EXPERIENCES IN REVERSE CHRONOLOGICAL ORDER** (most recent first)
4. Rewrites achievement bullets using:
   - Action verbs from the JD
   - Quantifiable metrics
   - Keywords naturally incorporated
   - 2-3 bullets per experience highlighting impact
5. Creates a skills section organized by category with JD keywords
6. Uses hyphens (-) never em dashes
7. Fits in 1-2 pages maximum
8. Follows this format exactly for each experience:
   - Company name, location
   - Position title, dates (Mon YYYY - Mon YYYY or Present)
   - 2-3 achievement bullets focused on impact

## STAGE 3: Generate LaTeX File

Create the resume LaTeX file at: output/{{output_name}}.tex

**Section Order (IMPORTANT):**
1. Professional Summary
2. Experience (reverse chronological order - most recent first)
3. Skills (before Education)
4. Education
5. Projects (optional)
6. Certifications (optional)

Replace these placeholders in the template:
- {{NAME}}: Use name from config.json
- {{EMAIL}}: Use email from config.json
- {{PHONE}}: Use phone from config.json
- {{LOCATION}}: Use location from config.json
- {{LINKS}}: Format as: linkedin | github | website with proper LaTeX hyperlinks
- {{SUMMARY_SECTION}}: Add \section{Professional Summary} with tailored summary
- {{EXPERIENCE_SECTION}}: Format all experiences using \resumeSubheading (reverse chronological - most recent first, add \vspace{4pt} between jobs)
- {{SKILLS_SECTION}}: Format skills by category with \textbf{Category:} skills \\[2pt]
- {{EDUCATION_SECTION}}: Format education entries
- {{PROJECTS_SECTION}}: Include if relevant, otherwise empty string
- {{CERTIFICATIONS_SECTION}}: Include if relevant, otherwise empty string

## STAGE 4: Compile and Validate

1. Compile the LaTeX to PDF:
   - Run: pdflatex -output-directory output output/{{output_name}}.tex
   - Run again for proper references

2. Provide ATS Validation Report:
   - Estimated ATS Score (0-100)
   - Keywords matched from JD (list all)
   - Keywords missing (if any)
   - Compatibility level: Excellent/Good/Fair/Poor
   - Top 3 recommendations

Print the full report and confirm the PDF location.

Variables:
- j: The job description file path (passed as argument)
- output_name: AUTOMATICALLY GENERATED from job title extraction in STAGE 0
  Format: Dagmawi-Teka-{Role-Title}-{timestamp}
  Example: Dagmawi-Teka-Backend-Developer-20260127_143022
