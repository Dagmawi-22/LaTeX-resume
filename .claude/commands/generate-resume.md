---
description: Generate an ATS-optimized resume from a job description
---

You are an expert resume optimization system with 4 specialized analysis stages.

## CRITICAL RULES - NEVER BREAK THESE:
1. **EXACTLY 1 PAGE - NO EXCEPTIONS** - Compress until it fits
2. **SECTION ORDER IS FIXED:** Summary → Experience → Skills → Education (Education ALWAYS last)
3. **MINIMAL SPACING:** Use \vspace{0pt} between sections, \vspace{2pt} max between items
4. **NEVER ASK FOR CLARIFICATION ON PAGE LENGTH OR SECTION ORDER** - These are fixed requirements

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
   - **IMPORTANT:** Don't just copy achievements from config.json - enrich and expand them based on the job context by inferring and adding similar relevant accomplishments that align with the role requirements
   - **AI-Native Style:** If the JD emphasizes AI/LLM integration, cutting-edge tools, or modern development practices, highlight AI-native working style and proficiency with advanced tools (Claude Code, MCP, AI-assisted development workflows, prompt engineering, etc.)
5. Creates a skills section organized by category with JD keywords
6. Uses hyphens (-) never em dashes
7. **CRITICAL: MUST FIT ON EXACTLY 1 PAGE - NO EXCEPTIONS**
8. Follows this format exactly for each experience:
   - Company name, location
   - Position title, dates (Mon YYYY - Mon YYYY or Present)
   - 2-3 achievement bullets focused on impact

## STAGE 3: Generate LaTeX File

Create the resume LaTeX file at: output/{{output_name}}.tex

**Section Order (NON-NEGOTIABLE - NEVER CHANGE THIS ORDER):**
1. Professional Summary
2. Experience (reverse chronological order - most recent first)
3. Skills (Technical Skills section)
4. Education (ALWAYS LAST - NEVER BEFORE SKILLS)
5. Projects (optional - rarely include unless explicitly relevant)
6. Certifications (optional - rarely include)

**ONE-PAGE OPTIMIZATION (ABSOLUTELY CRITICAL - NO EXCEPTIONS):**
- **MUST FIT ON EXACTLY 1 PAGE - If it doesn't fit, reduce content until it does**
- After summary section: \vspace{1pt} or \vspace{0pt}
- Between experience entries: \vspace{2pt} or less
- Between Education entries: \vspace{1pt}
- Between sections: \vspace{0pt} ALWAYS
- In skills section line breaks: just \\ with NO spacing like \\[1pt]
- Keep skills VERY concise - max 4 categories, remove all redundant/obvious items
- If still overflowing: reduce bullet points, shorten descriptions, or drop least relevant experience

Replace these placeholders in the template:
- {{NAME}}: Use name from config.json
- {{TITLE}}: Use the extracted job title from STAGE 0 (e.g., "React Native Developer", "Full-Stack Mobile Developer | React Native \& Node.js")
- {{EMAIL}}: Use email from config.json
- {{PHONE}}: Use phone from config.json
- {{LOCATION}}: Use location from config.json
- {{LINKS}}: Format as: linkedin | github | website with proper LaTeX hyperlinks
- {{SUMMARY_SECTION}}: Add \section{Professional Summary} with tailored summary
- {{EXPERIENCE_SECTION}}: Format all experiences using \resumeSubheading (reverse chronological - most recent first, add \vspace{2pt} between jobs)
- {{SKILLS_SECTION}}: Format skills by category with \textbf{Category:} skills \\ (no spacing)
- {{EDUCATION_SECTION}}: Format education entries (add \vspace{1pt} between entries)
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
