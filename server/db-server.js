#!/usr/bin/env node
/**
 * SQLite 数据库服务 - 支持开发/生产环境区分
 * 使用 better-sqlite3 (同步 API，性能更好)
 */

import express from 'express';
import Database from 'better-sqlite3';
import cors from 'cors';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 加载环境配置
const env = process.env.NODE_ENV || 'development';
dotenv.config({ path: join(__dirname, `.env.${env}`) });

const app = express();
const PORT = process.env.DB_PORT || 3001;
const DB_PATH = process.env.DB_PATH || join(__dirname, '../data', `${env}.db`);

// 确保数据目录存在
const dataDir = join(__dirname, '../data');
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// 中间件
app.use(cors());
app.use(express.json());

// 数据库连接
let db;

function initDatabase() {
  try {
    db = new Database(DB_PATH);
    console.log(`✅ 数据库已连接：${DB_PATH} (${env}环境)`);
    createTables();
    return true;
  } catch (error) {
    console.error('❌ 数据库连接失败:', error);
    return false;
  }
}

function createTables() {
  // 用户表
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      role TEXT DEFAULT 'parent',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // 孩子表
  db.exec(`
    CREATE TABLE IF NOT EXISTS children (
      id TEXT PRIMARY KEY,
      parent_id INTEGER NOT NULL,
      nickname TEXT NOT NULL,
      gender TEXT NOT NULL,
      grade TEXT NOT NULL,
      age INTEGER NOT NULL,
      textbook TEXT,
      hobbies TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (parent_id) REFERENCES users(id)
    )
  `);

  // 积分表
  db.exec(`
    CREATE TABLE IF NOT EXISTS points (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      child_id TEXT NOT NULL,
      points INTEGER DEFAULT 0,
      level TEXT DEFAULT 'star',
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (child_id) REFERENCES children(id)
    )
  `);

  // 恐龙表
  db.exec(`
    CREATE TABLE IF NOT EXISTS dinosaurs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      child_id TEXT UNIQUE NOT NULL,
      level INTEGER DEFAULT 1,
      attack INTEGER DEFAULT 10,
      defense INTEGER DEFAULT 10,
      streak_days INTEGER DEFAULT 0,
      exp INTEGER DEFAULT 0,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (child_id) REFERENCES children(id)
    )
  `);

  // 任务表
  db.exec(`
    CREATE TABLE IF NOT EXISTS tasks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      child_id TEXT NOT NULL,
      title TEXT NOT NULL,
      subject TEXT NOT NULL,
      content TEXT,
      status TEXT DEFAULT 'pending',
      completed_at DATETIME,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (child_id) REFERENCES children(id)
    )
  `);

  // 错题表
  db.exec(`
    CREATE TABLE IF NOT EXISTS wrong_questions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      child_id TEXT NOT NULL,
      subject TEXT NOT NULL,
      question TEXT NOT NULL,
      user_answer TEXT,
      correct_answer TEXT,
      reason TEXT,
      wrong_count INTEGER DEFAULT 1,
      mastered BOOLEAN DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (child_id) REFERENCES children(id)
    )
  `);

  // 阅读记录表
  db.exec(`
    CREATE TABLE IF NOT EXISTS reading_records (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      child_id TEXT NOT NULL,
      book_title TEXT NOT NULL,
      words_count INTEGER DEFAULT 0,
      progress INTEGER DEFAULT 0,
      status TEXT DEFAULT 'reading',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (child_id) REFERENCES children(id)
    )
  `);

  // AI 模型配置表
  db.exec(`
    CREATE TABLE IF NOT EXISTS ai_models (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      model_name TEXT NOT NULL,
      model_type TEXT NOT NULL,
      is_active BOOLEAN DEFAULT 0,
      config TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // 系统设置表
  db.exec(`
    CREATE TABLE IF NOT EXISTS settings (
      key TEXT PRIMARY KEY,
      value TEXT,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // 插入默认数据
  try {
    db.exec(`INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')`);
    
    db.exec(`
      INSERT OR IGNORE INTO ai_models (model_name, model_type, is_active, config)
      VALUES 
        ('moonshot-v1-8k', 'moonshot', 1, '{"temperature": 0.7}'),
        ('moonshot-v1-32k', 'moonshot', 0, '{"temperature": 0.7}'),
        ('qwen-plus', 'aliyun', 0, '{"temperature": 0.7}')
    `);
  } catch (error) {
    console.log('⚠️ 默认数据可能已存在');
  }
  
  console.log('✅ 数据库表初始化完成');
}

// ==================== API 路由 ====================

// 健康检查
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    environment: env,
    database: DB_PATH,
    timestamp: new Date().toISOString()
  });
});

// 获取环境信息
app.get('/env', (req, res) => {
  res.json({
    env: process.env.VITE_APP_ENV,
    title: process.env.VITE_APP_TITLE,
    debug: process.env.VITE_ENABLE_DEBUG === 'true'
  });
});

// ==================== 用户管理 ====================

// 获取所有用户（管理员）
app.get('/api/admin/users', (req, res) => {
  try {
    const rows = db.prepare('SELECT * FROM users').all();
    res.json(rows);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== AI 模型管理 ====================

// 获取所有 AI 模型（管理员）
app.get('/api/admin/models', (req, res) => {
  try {
    const rows = db.prepare('SELECT * FROM ai_models').all();
    res.json(rows);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 更新 AI 模型配置（管理员）
app.put('/api/admin/models/:id', (req, res) => {
  try {
    const { id } = req.params;
    const { is_active } = req.body;
    
    // 先将所有模型设为非激活
    db.prepare('UPDATE ai_models SET is_active = 0').run();
    
    // 激活选中的模型
    db.prepare('UPDATE ai_models SET is_active = ? WHERE id = ?').run(is_active ? 1 : 0, id);
    
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 获取当前激活的 AI 模型
app.get('/api/admin/models/active', (req, res) => {
  try {
    const row = db.prepare('SELECT * FROM ai_models WHERE is_active = 1').get();
    res.json(row || {});
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== 系统设置 ====================

// 获取系统设置
app.get('/api/admin/settings', (req, res) => {
  try {
    const rows = db.prepare('SELECT * FROM settings').all();
    res.json(rows);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 更新系统设置
app.put('/api/admin/settings/:key', (req, res) => {
  try {
    const { key } = req.params;
    const { value } = req.body;
    
    db.prepare(`
      INSERT INTO settings (key, value, updated_at) 
      VALUES (?, ?, CURRENT_TIMESTAMP)
      ON CONFLICT(key) DO UPDATE SET value = ?, updated_at = CURRENT_TIMESTAMP
    `).run(key, value, value);
    
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== 启动服务 ====================

function start() {
  try {
    initDatabase();
    app.listen(PORT, () => {
      console.log(`
╔════════════════════════════════════════════════════════╗
║                                                        ║
║   🚀 SQLite 数据库服务已启动                           ║
║                                                        ║
║   环境：${env.padEnd(12)}                                    ║
║   端口：${String(PORT).padEnd(12)}                                  ║
║   数据库：${DB_PATH.padEnd(38)}║
║                                                        ║
║   API: http://localhost:${String(PORT).padEnd(18)}          ║
║   健康检查：http://localhost:${String(PORT).padEnd(14)}/health     ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
      `);
    });
  } catch (error) {
    console.error('❌ 服务启动失败:', error);
    process.exit(1);
  }
}

start();
