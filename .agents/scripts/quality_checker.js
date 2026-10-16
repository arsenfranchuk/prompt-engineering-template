const { spawn } = require('child_process');
const path = require('path');

const target = path.join(__dirname, '..', 'hooks', 'backend_post_tool_audit.py');
const child = spawn('py', [target], { stdio: 'inherit' });
child.on('exit', (code) => process.exit(code || 0));
