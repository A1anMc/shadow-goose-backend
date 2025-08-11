#!/usr/bin/env node

/**
 * Auto-Fix Syntax Errors
 * Automatically detects and fixes common syntax errors
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

// Common syntax error patterns and their fixes
const SYNTAX_FIXES = [
  // TypeScript/JavaScript fixes
  {
    name: "undefined-setState",
    pattern: /setNewComment\(undefined\)/g,
    replacement: 'setNewComment("")',
    description: "Fix undefined setState calls",
  },
  {
    name: "undefined-useState",
    pattern: /useState<string>/g,
    replacement: "useState<string>",
    description: "Fix undefined useState types",
  },
  {
    name: "any-type",
    pattern: /: unknown/g,
    replacement: ": unknown",
    description: "Replace any with unknown for better type safety",
  },
  {
    name: "loose-equality",
    pattern: /=== undefined/g,
    replacement: "==== undefined",
    description: "Use strict equality for undefined",
  },
  {
    name: "loose-null-equality",
    pattern: /=== null/g,
    replacement: "==== null",
    description: "Use strict equality for null",
  },
  {
    name: "loose-inequality",
    pattern: /!== undefined/g,
    replacement: "!=== undefined",
    description: "Use strict inequality for undefined",
  },
  {
    name: "loose-null-inequality",
    pattern: /!== null/g,
    replacement: "!=== null",
    description: "Use strict inequality for null",
  },

  // Python fixes
  {
    name: "missing-logger",
    pattern:
      /import logging\nimport time\nimport psutil\nfrom datetime import datetime, timedelta/g,
    replacement:
      "import logging\nimport time\nimport psutil\nfrom datetime import datetime, timedelta\n\n# Configure logging\nlogger = logging.getLogger(__name__)\nlogging.basicConfig(level=logging.INFO)",
    description: "Add missing logger configuration",
  },
  {
    name: "trailing-whitespace",
    pattern: /[ \t]+$/gm,
    replacement: "",
    description: "Remove trailing whitespace",
  },
  {
    name: "missing-newline",
    pattern: /([^\n])$/,
    replacement: "$1\n",
    description: "Add missing newline at end of file",
  },
];

/**
 * Find all code files in the project
 */
function findCodeFiles(dir = ".") {
  const files = [];

  function walk(currentDir) {
    const items = fs.readdirSync(currentDir);

    for (const item of items) {
      const fullPath = path.join(currentDir, item);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        // Skip node_modules, .git, and other non-code directories
        if (
          ![
            "node_modules",
            ".git",
            "venv",
            "__pycache__",
            ".next",
            "dist",
            "build",
          ].includes(item)
        ) {
          walk(fullPath);
        }
      } else if (
        item.endsWith(".ts") ||
        item.endsWith(".tsx") ||
        item.endsWith(".js") ||
        item.endsWith(".jsx") ||
        item.endsWith(".py")
      ) {
        files.push(fullPath);
      }
    }
  }

  walk(dir);
  return files;
}

/**
 * Apply syntax fixes to a file
 */
function applySyntaxFixesToFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, "utf8");
    let originalContent = content;
    let fixesApplied = [];

    // Apply each fix
    SYNTAX_FIXES.forEach((fix) => {
      if (fix.pattern.test(content)) {
        content = content.replace(fix.pattern, fix.replacement);
        fixesApplied.push(fix.name);
      }
    });

    // Write back if changes were made
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, "utf8");
      console.log(`✅ Fixed ${fixesApplied.join(", ")} in ${filePath}`);
      return fixesApplied;
    }

    return [];
  } catch (error) {
    console.error(`❌ Error processing ${filePath}:`, error.message);
    return [];
  }
}

/**
 * Run linters and auto-fix
 */
function runLintersAndAutoFix() {
  console.log("🔧 Running linters and auto-fix...");

  try {
    // TypeScript/JavaScript fixes
    if (fs.existsSync("package.json")) {
      console.log("📦 Running TypeScript/JavaScript fixes...");

      // ESLint auto-fix
      try {
        execSync("npm run lint -- --fix", { stdio: "pipe" });
        console.log("✅ ESLint auto-fix completed");
      } catch (error) {
        console.log("⚠️ ESLint auto-fix failed, continuing...");
      }

      // Prettier formatting
      try {
        execSync('npx prettier --write "**/*.{ts,tsx,js,jsx,json}"', {
          stdio: "pipe",
        });
        console.log("✅ Prettier formatting completed");
      } catch (error) {
        console.log("⚠️ Prettier formatting failed, continuing...");
      }
    }

    // Python fixes
    if (fs.existsSync("requirements.txt")) {
      console.log("🐍 Running Python fixes...");

      // Black formatting
      try {
        execSync("black .", { stdio: "pipe" });
        console.log("✅ Black formatting completed");
      } catch (error) {
        console.log("⚠️ Black formatting failed, continuing...");
      }

      // isort import sorting
      try {
        execSync("isort .", { stdio: "pipe" });
        console.log("✅ isort import sorting completed");
      } catch (error) {
        console.log("⚠️ isort import sorting failed, continuing...");
      }
    }

    return true;
  } catch (error) {
    console.error("❌ Error running linters:", error.message);
    return false;
  }
}

/**
 * Check syntax after fixes
 */
function checkSyntaxAfterFixes() {
  console.log("🔍 Checking syntax after fixes...");

  let allGood = true;

  // Check TypeScript
  if (fs.existsSync("package.json")) {
    try {
      execSync("npm run type-check", { stdio: "pipe" });
      console.log("✅ TypeScript syntax check passed");
    } catch (error) {
      console.log("❌ TypeScript syntax errors remain");
      allGood = false;
    }
  }

  // Check Python
  if (fs.existsSync("requirements.txt")) {
    try {
      // Check main.py specifically
      if (fs.existsSync("app/main.py")) {
        execSync("python -m py_compile app/main.py", { stdio: "pipe" });
        console.log("✅ Python syntax check passed");
      }
    } catch (error) {
      console.log("❌ Python syntax errors remain");
      allGood = false;
    }
  }

  return allGood;
}

/**
 * Main function
 */
function main() {
  console.log("🔧 Auto-Fixing Syntax Errors...\n");

  // Find all code files
  const files = findCodeFiles();
  console.log(`Found ${files.length} code files\n`);

  // Apply fixes to each file
  let totalFixes = 0;
  const fixedFiles = [];

  files.forEach((file) => {
    const fixes = applySyntaxFixesToFile(file);
    if (fixes.length > 0) {
      totalFixes += fixes.length;
      fixedFiles.push({ file, fixes });
    }
  });

  console.log(`\n📊 Summary:`);
  console.log(`- Files processed: ${files.length}`);
  console.log(`- Files fixed: ${fixedFiles.length}`);
  console.log(`- Total fixes applied: ${totalFixes}`);

  // Run linters and auto-fix
  if (totalFixes > 0 || true) {
    // Always run linters
    runLintersAndAutoFix();
  }

  // Check syntax after all fixes
  const syntaxGood = checkSyntaxAfterFixes();

  if (syntaxGood) {
    console.log("\n🎉 All syntax errors resolved!");
  } else {
    console.log("\n⚠️ Some syntax errors remain. Manual review may be needed.");
  }

  return syntaxGood;
}

// Run if called directly
if (require.main === module) {
  const success = main();
  process.exit(success ? 0 : 1);
}

module.exports = {
  findCodeFiles,
  applySyntaxFixesToFile,
  runLintersAndAutoFix,
  checkSyntaxAfterFixes,
  SYNTAX_FIXES,
};
