/**
 * Forwarder to .agents/hooks/backend_safety_guard.py
 */
const { spawn } = require('child_process');
const path = require('path');

const target = path.join(__dirname, '..', 'hooks', 'backend_safety_guard.py');
const child = spawn('py', [target], { stdio: 'inherit' });
child.on('exit', (code) => process.exit(code || 0));
