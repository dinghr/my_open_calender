#!/usr/bin/env python3
"""
AI 伴学小程序 - 数据库初始化脚本

功能：
1. 创建数据库和所有表
2. 创建初始管理员账号
3. 生成初始登录码
"""

import sys
import os
from datetime import datetime
import uuid

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

from models import Database, User, Student, LoginCode, GrowthTree
from sqlalchemy.orm import sessionmaker


def create_initial_data(db):
    """创建初始数据"""
    Session = sessionmaker(bind=db.engine)
    session = Session()
    
    try:
        # 检查是否已有数据
        user_count = session.query(User).count()
        if user_count > 0:
            print("⚠️  数据库中已有数据，跳过初始化")
            return
        
        print("📝 创建初始数据...")
        
        # 创建管理员账号
        admin_id = str(uuid.uuid4())
        admin = User(
            id=admin_id,
            nickname="管理员",
            role="admin"
        )
        session.add(admin)
        print(f"✅ 创建管理员账号：{admin_id}")
        
        # 创建初始登录码
        login_code_id = str(uuid.uuid4())
        login_code = LoginCode(
            id=login_code_id,
            code="FAMILY-INIT-0001",
            status="active",
            max_uses=None,  # 无限次
            note="初始登录码"
        )
        session.add(login_code)
        print(f"✅ 创建初始登录码：FAMILY-INIT-0001")
        
        # 提交事务
        session.commit()
        print("✅ 初始数据创建成功！")
        
    except Exception as e:
        session.rollback()
        print(f"❌ 初始化失败：{e}")
        raise
    finally:
        session.close()


def main():
    print("🚀 AI 伴学小程序 - 数据库初始化")
    print("=" * 50)
    
    # 确保目录存在
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # 创建数据库
    print("📁 数据库路径：data/app.db")
    db = Database("data/app.db")
    
    print("🔧 创建数据库表...")
    db.create_tables()
    print("✅ 数据库表创建成功！")
    
    # 创建初始数据
    create_initial_data(db)
    
    print("=" * 50)
    print("🎉 初始化完成！")
    print("\n下一步：")
    print("1. 启动后端服务：python backend/main.py")
    print("2. 使用登录码登录：FAMILY-INIT-0001")
    print("3. 在小程序中绑定小朋友账号")


if __name__ == "__main__":
    main()
