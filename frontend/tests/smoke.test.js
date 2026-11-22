// frontend/tests/smoke.test.js
const fs = require('fs');
const path = require('path');

const requiredFiles = [
  'src/app/page.tsx',
  'src/app/layout.tsx',
  'src/app/landing/page.tsx',
  'src/app/login/page.tsx',
  'src/components/PosView.tsx',
  'src/components/ProductsView.tsx',
  'src/components/ReportsView.tsx',
  'src/components/SettlementsView.tsx',
  'src/components/ExpensesView.tsx',
  'src/components/IntegrationsView.tsx',
  'src/components/AdminConsoleView.tsx',
  'src/components/WhatsAppAssistantView.tsx',
  'src/components/TeamRolesView.tsx',
  'src/components/Sidebar.tsx',
  'src/components/Header.tsx'
];

let failed = 0;
console.log('Running frontend structure & component smoke tests...');

for (const file of requiredFiles) {
  const fullPath = path.join(__dirname, '..', file);
  if (fs.existsSync(fullPath)) {
    const stats = fs.statSync(fullPath);
    if (stats.size > 0) {
      console.log(`  ✓ Verified ${file} (${stats.size} bytes)`);
    } else {
      console.error(`  ✗ Empty file: ${file}`);
      failed++;
    }
  } else {
    console.error(`  ✗ Missing required file: ${file}`);
    failed++;
  }
}

if (failed > 0) {
  console.error(`Smoke test failed: ${failed} file(s) failed check.`);
  process.exit(1);
} else {
  console.log(`\nAll ${requiredFiles.length} critical frontend views and pages verified successfully!`);
  process.exit(0);
}
