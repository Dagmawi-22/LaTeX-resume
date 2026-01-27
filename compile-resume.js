#!/usr/bin/env node

/**
 * Resume LaTeX Compiler
 * Compiles .tex files to PDF using pdflatex
 */

import { execSync } from 'child_process';
import { existsSync, statSync, unlinkSync } from 'fs';
import { join, basename } from 'path';
import { argv } from 'process';

const COLORS = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  gray: '\x1b[90m',
};

function log(message, color = COLORS.reset) {
  console.log(`${color}${message}${COLORS.reset}`);
}

function checkPdfLatex() {
  try {
    execSync('which pdflatex', { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function compileLaTeX(texFile, outputDir = 'output') {
  const filename = basename(texFile, '.tex');

  log('\n═══════════════════════════════════════════════════════', COLORS.blue);
  log('           LaTeX → PDF Compiler', COLORS.blue);
  log('═══════════════════════════════════════════════════════\n', COLORS.blue);

  // Check if pdflatex is installed
  if (!checkPdfLatex()) {
    log('✗ Error: pdflatex not found!', COLORS.red);
    log('\nPlease install LaTeX:', COLORS.yellow);
    log('  macOS:   brew install --cask mactex-no-gui', COLORS.gray);
    log('  Ubuntu:  sudo apt-get install texlive-latex-base texlive-latex-extra', COLORS.gray);
    log('  Windows: Download from https://miktex.org/', COLORS.gray);
    process.exit(1);
  }

  // Check if input file exists
  if (!existsSync(texFile)) {
    log(`✗ Error: File not found: ${texFile}`, COLORS.red);
    process.exit(1);
  }

  log(`📄 Compiling: ${texFile}`, COLORS.blue);
  log(`📁 Output directory: ${outputDir}\n`, COLORS.gray);

  try {
    // Run pdflatex twice for proper references and formatting
    for (let i = 1; i <= 2; i++) {
      log(`⚙️  Pass ${i}/2...`, COLORS.yellow);

      execSync(
        `pdflatex -output-directory="${outputDir}" -interaction=nonstopmode "${texFile}"`,
        {
          stdio: 'pipe',
          encoding: 'utf-8'
        }
      );
    }

    const pdfFile = join(outputDir, `${filename}.pdf`);

    if (existsSync(pdfFile)) {
      const stats = statSync(pdfFile);
      const sizeKB = (stats.size / 1024).toFixed(1);

      log('\n✓ Compilation successful!', COLORS.green);
      log(`✓ PDF created: ${pdfFile}`, COLORS.green);
      log(`✓ File size: ${sizeKB} KB`, COLORS.green);

      // Clean up auxiliary files
      cleanAuxiliaryFiles(outputDir, filename);

      log('\n═══════════════════════════════════════════════════════', COLORS.blue);
      log(`Resume ready at: ${pdfFile}`, COLORS.green);
      log('═══════════════════════════════════════════════════════\n', COLORS.blue);

      return pdfFile;
    } else {
      log('✗ Error: PDF file was not created', COLORS.red);
      process.exit(1);
    }

  } catch (error) {
    log('\n✗ Compilation failed!', COLORS.red);
    log('Check the .log file in the output directory for details.\n', COLORS.yellow);

    // Show last few lines of log file if it exists
    const logFile = join(outputDir, `${filename}.log`);
    if (existsSync(logFile)) {
      try {
        const logContent = execSync(`tail -20 "${logFile}"`, { encoding: 'utf-8' });
        log('Last 20 lines of log file:', COLORS.gray);
        log('─────────────────────────────────────────────────', COLORS.gray);
        console.log(logContent);
        log('─────────────────────────────────────────────────', COLORS.gray);
      } catch {}
    }

    process.exit(1);
  }
}

function cleanAuxiliaryFiles(outputDir, filename) {
  const extensions = ['.aux', '.log', '.out'];
  let cleaned = 0;

  extensions.forEach(ext => {
    const file = join(outputDir, `${filename}${ext}`);
    if (existsSync(file)) {
      try {
        unlinkSync(file);
        cleaned++;
      } catch {}
    }
  });

  if (cleaned > 0) {
    log(`✓ Cleaned ${cleaned} auxiliary file(s)`, COLORS.gray);
  }
}

// Main
const args = argv.slice(2);

if (args.length === 0) {
  log('Usage: node compile-resume.js <path-to-tex-file> [output-dir]', COLORS.yellow);
  log('Example: node compile-resume.js output/resume.tex', COLORS.gray);
  process.exit(0);
}

const texFile = args[0];
const outputDir = args[1] || 'output';

compileLaTeX(texFile, outputDir);
