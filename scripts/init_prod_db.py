#!/usr/bin/env python3
"""
初始化生产环境数据库
仅创建数据库结构，不插入测试数据
"""
import sys
import os

# 添加 backend 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models import Database, Base

def init_prod_db():
    """初始化生产数据库"""
    db_path = "data/prod.db"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # 检查是否已存在
    if os.path.exists(db_path):
        print(f"⚠️  数据库文件已存在：{db_path}")
        print(f"   大小：{os.path.getsize(db_path) / 1024:.2f} KB")
        response = input("是否继续？这将保留现有数据 (y/N): ")
        if response.lower() != 'y':
            print("取消初始化")
            return
    
    # 创建数据库
    db = Database(db_path)
    db.create_tables()
    
    print(f"✅ 生产数据库初始化完成！")
    print(f"📁 数据库文件：{db_path}")
    print(f"📊 数据库结构已创建，等待用户注册...")
    print(f"\n⚠️  重要提示:")
    print(f"   - 生产数据库不包含测试数据")
    print(f"   - 请确保 secrets 文件已正确配置")
    print(f"   - 首次启动时会自动创建管理员账户")


if __name__ == "__main__":
    init_prod_db()
