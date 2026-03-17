#!/usr/bin/env python3
"""
AI 伴学小程序 - 数据库迁移脚本

功能：添加题库和错题管理相关表
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

from models import Database, QuestionBank, WrongQuestion, KnowledgePoint


def migrate():
    """执行数据库迁移"""
    print("🚀 开始数据库迁移...")
    
    db = Database("data/app.db")
    
    print("🔧 创建新表...")
    db.create_tables()
    
    print("✅ 迁移完成！")
    print("\n新增表：")
    print("  - question_bank (题库)")
    print("  - wrong_questions (错题)")
    print("  - knowledge_points (知识点)")
    
    print("\n✅ 所有新表已创建成功！")


if __name__ == "__main__":
    migrate()
