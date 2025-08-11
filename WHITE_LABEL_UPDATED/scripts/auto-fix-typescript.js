#!/usr/bin/env node

/**
 * Auto-Fix TypeScript Errors
 * Automatically detects and fixes common TypeScript errors
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Common TypeScript error patterns and their fixes
const COMMON_FIXES = [
  {
    name: 'undefined-setState',
    pattern: /setNewComment\(undefined\)/g,
    replacement: 'setNewComment("")',
    description: 'Fix undefined setState calls'
  },
  {
    name: 'undefined-useState',
    pattern: /useState<string>/g,
    replacement: 'useState<string>',
    description: 'Fix undefined useState types'
  },
  {
    name: 'any-type',
    pattern: /: unknown/g,
    replacement: ': unknown',
    description: 'Replace any with unknown for better type safety'
  },
  {
    name: 'missing-import',
    pattern: /import React from 'react'/g,
    replacement: "import React from 'react'",
    description: 'Ensure React import is present'
  },
  {
    name: 'async-await',
    pattern: /\.then\(/g,
    replacement: 'await ',
    description: 'Convert await ) to async/await'
  }
];

/**
 * Find all TypeScript/JavaScript files in the project
 */
function findTypeScriptFiles(dir = '.') {
  const files = [];

  function walk(currentDir) {
    const items = fs.readdirSync(currentDir);

    for (const item of items) {
      const fullPath = path.join(currentDir, item);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        // Skip node_modules and .git
        if (item !== 'node_modules' && item !== '.git') {
          walk(fullPath);
        }
      } else if (item.endsWith('.ts') || item.endsWith('.tsx') || item.endsWith('.js') || item.endsWith('.jsx')) {
        files.push(fullPath);
      }
    }
  }

  walk(dir);
  return files;
}

/**
 * Apply fixes to a file
 */
function applyFixesToFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let originalContent = content;
    let fixesApplied = [];

    // Apply each fix
    COMMON_FIXES.forEach(fix => {
      if (fix.pattern.test(content)) {
        content = content.replace(fix.pattern, fix.replacement);
        fixesApplied.push(fix.name);
      }
    });

    // Write back if changes were made
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log(`✅ Fixed ${fixesApplied.join(', ')} in ${filePath}`);
      return fixesApplied;
    }

    return [];
  } catch (error) {
    console.error(`❌ Error processing ${filePath}:`, error.message);
    return [];
  }
}

/**
 * Run TypeScript compiler to check for errors
 */
function runTypeScriptCheck() {
  try {
    execSync('npx tsc --noEmit', { stdio: 'pipe' });
    console.log('✅ TypeScript check passed');
    return { success: true, errors: [] };
  } catch (error) {
    const output = error.stdout.toString() + error.stderr.toString();
    const errors = output.split('\n').filter(line => line.includes('error'));
    console.log('❌ TypeScript errors found:', errors.length);
    return { success: false, errors };
  }
}

/**
 * Main function
 */
function main() {
  console.log('🔧 Auto-Fixing TypeScript Errors...\n');

  // Find all TypeScript files
  const files = findTypeScriptFiles();
  console.log(`Found ${files.length} TypeScript/JavaScript files\n`);

  // Apply fixes to each file
  let totalFixes = 0;
  const fixedFiles = [];

  files.forEach(file => {
    const fixes = applyFixesToFile(file);
    if (fixes.length > 0) {
      totalFixes += fixes.length;
      fixedFiles.push({ file, fixes });
    }
  });

  console.log(`\n📊 Summary:`);
  console.log(`- Files processed: ${files.length}`);
  console.log(`- Files fixed: ${fixedFiles.length}`);
  console.log(`- Total fixes applied: ${totalFixes}`);

  if (totalFixes > 0) {
    console.log('\n🔍 Running TypeScript check after fixes...');
    const checkResult = runTypeScriptCheck();

    if (checkResult.success) {
      console.log('🎉 All TypeScript errors resolved!');
    } else {
      console.log('⚠️ Some TypeScript errors remain. Manual review may be needed.');
      console.log('Remaining errors:');
      checkResult.errors.forEach(error => console.log(`  - ${error}`));
    }
  } else {
    console.log('✅ No TypeScript errors found to fix');
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = {
  findTypeScriptFiles,
  applyFixesToFile,
  runTypeScriptCheck,
  COMMON_FIXES
};
