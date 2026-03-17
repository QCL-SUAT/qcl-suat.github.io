#!/usr/bin/env node
// encrypt-multi-user.js
// 多用户加密资源页面
// 原理：用随机主密钥加密页面，每个用户的凭据单独包装主密钥
// 登录时：用户凭据 → 解出主密钥 → 解密页面

const crypto = require('crypto');
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const SCRIPT_DIR = __dirname;
const PROJECT_DIR = path.dirname(SCRIPT_DIR);
const CRED_FILE = process.env.CRED_FILE || path.join(SCRIPT_DIR, 'credentials.conf');
const TEMPLATE = path.join(SCRIPT_DIR, 'staticrypt-template.html');
const INPUT = path.join(PROJECT_DIR, '_site', 'resources', 'index.html');

// 解析凭据文件：每行 username:password
function readCredentials(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const creds = [];
    for (const line of content.split('\n')) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) continue;
        const idx = trimmed.indexOf(':');
        if (idx === -1) {
            console.error(`格式错误（缺少冒号）：${trimmed}`);
            process.exit(1);
        }
        creds.push({
            username: trimmed.substring(0, idx),
            password: trimmed.substring(idx + 1)
        });
    }
    return creds;
}

// 用 PBKDF2 + AES-256-CBC 为某用户加密主密钥
function encryptForUser(masterKey, username, password) {
    const salt = Buffer.from(username, 'utf8');
    const key = crypto.pbkdf2Sync(password, salt, 100000, 32, 'sha256');
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
    const encrypted = Buffer.concat([cipher.update(masterKey, 'utf8'), cipher.final()]);
    return { iv: iv.toString('hex'), data: encrypted.toString('hex') };
}

function sha256(str) {
    return crypto.createHash('sha256').update(str, 'utf8').digest('hex');
}

// ---- 主流程 ----

if (!fs.existsSync(CRED_FILE)) {
    console.error(`错误：凭据文件不存在 ${CRED_FILE}`);
    process.exit(1);
}
if (!fs.existsSync(INPUT)) {
    console.error(`错误：${INPUT} 不存在，请先运行 bundle exec jekyll build`);
    process.exit(1);
}
if (!fs.existsSync(TEMPLATE)) {
    console.error(`错误：模板文件不存在 ${TEMPLATE}`);
    process.exit(1);
}

const credentials = readCredentials(CRED_FILE);
if (credentials.length === 0) {
    console.error('错误：没有有效凭据');
    process.exit(1);
}

console.log(`读取到 ${credentials.length} 个用户凭据`);

// 生成随机主密钥
const masterKey = crypto.randomBytes(32).toString('base64url');

// 用 StaticCrypt 以主密钥加密页面
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'qcl-encrypt-'));

const result = spawnSync('npx', [
    'staticrypt', INPUT,
    '-p', masterKey,
    '--short',
    '-d', tmpDir,
    '-c', 'false',
    '-t', TEMPLATE,
    '--template-title', '组内资源 — QCL',
    '--template-instructions', '请输入课题组凭据以访问内部资源',
    '--template-placeholder', '请输入密码',
    '--template-button', '登 录',
    '--template-error', '用户名或密码错误，请重试',
    '--template-remember', '记住登录状态',
    '--template-color-primary', '#4adeaa',
    '--template-color-secondary', '#080c10'
], { stdio: 'inherit', cwd: PROJECT_DIR });

if (result.status !== 0) {
    console.error('StaticCrypt 加密失败');
    fs.rmSync(tmpDir, { recursive: true, force: true });
    process.exit(1);
}

// 为每个用户包装主密钥
const userKeysMap = {};
for (const cred of credentials) {
    userKeysMap[sha256(cred.username)] = encryptForUser(masterKey, cred.username, cred.password);
    console.log(`  ✓ ${cred.username}`);
}

// 将 userKeys 注入加密后的 HTML
let html = fs.readFileSync(path.join(tmpDir, 'index.html'), 'utf8');
html = html.replace('"__USER_KEYS_PLACEHOLDER__"', JSON.stringify(userKeysMap));
fs.writeFileSync(INPUT, html);

// 清理
fs.rmSync(tmpDir, { recursive: true, force: true });

console.log('\n加密完成！所有用户均可使用各自的凭据登录。');
