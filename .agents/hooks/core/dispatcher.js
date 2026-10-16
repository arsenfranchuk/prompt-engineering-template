const { spawn } = require('child_process');
const path = require('path');

const action = process.argv[2] || 'pre-tool-use';
let target;
if (action === 'pre-tool-use') {
  target = path.join(__dirname, '..', 'backend_safety_guard.py');
} else {
  target = path.join(__dirname, '..', 'backend_post_tool_audit.py');
}

const child = spawn('py', [target], { stdio: 'inherit' });
child.on('exit', (code) => process.exit(code || 0));
