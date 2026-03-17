#!/usr/bin/env python3
"""
初始化开发环境数据库
创建 dev.db 并插入测试数据
"""
import sys
import os

# 添加 backend 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models import Database, Base, Student, User, UserStudentBinding, RelationType, ApprovalStatus
from datetime import datetime, date

def init_dev_db():
    """初始化开发数据库"""
    db_path = "data/dev.db"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # 创建数据库
    db = Database(db_path)
    db.create_tables()
    
    session = db.get_session()
    
    try:
        # 检查是否已有数据
        existing_students = session.query(Student).count()
        if existing_students > 0:
            print(f"⚠️  数据库已存在 {existing_students} 个学生，跳过初始化")
            return
        
        # 创建测试学生
        students_data = [
            {"id": "student-001", "name": "小明", "grade": 3},
            {"id": "student-002", "name": "小红", "grade": 5},
        ]
        
        for s in students_data:
            student = Student(
                id=s["id"],
                name=s["name"],
                grade=s["grade"],
                birthday=date(2020 - s["grade"] + 6, 1, 1)  # 估算生日
            )
            session.add(student)
            print(f"✅ 创建学生：{s['name']} (ID: {s['id']})")
        
        # 创建测试家长
        parent = User(
            id="parent-001",
            nickname="测试家长",
            role="parent"
        )
        session.add(parent)
        print(f"✅ 创建家长：{parent.nickname} (ID: {parent.id})")
        
        # 创建绑定关系
        binding = UserStudentBinding(
            id="binding-001",
            user_id="parent-001",
            student_id="student-001",
            relation=RelationType.FATHER,
            status=ApprovalStatus.APPROVED,
            approved_at=datetime.utcnow()
        )
        session.add(binding)
        print(f"✅ 创建绑定关系：{parent.nickname} → {students_data[0]['name']}")
        
        session.commit()
        print(f"\n✅ 开发数据库初始化完成！")
        print(f"📁 数据库文件：{db_path}")
        print(f"📊 数据概览:")
        print(f"   - 学生：{session.query(Student).count()}")
        print(f"   - 家长：{session.query(User).count()}")
        print(f"   - 绑定关系：{session.query(UserStudentBinding).count()}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ 初始化失败：{e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    init_dev_db()
