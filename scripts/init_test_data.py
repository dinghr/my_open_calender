"""
初始化测试数据
"""
import sys
sys.path.insert(0, '/home/ecs-user/my_open_calender/backend')

from datetime import datetime
from uuid import uuid4
from models import Database, User, Student, UserStudentBinding, LoginCode
from models import UserRole, RelationType, ApprovalStatus, LoginCodeStatus

db = Database("data/app.db")
session = db.get_session()

# 创建测试用户
user = User(
    id=str(uuid4()),
    nickname="测试家长",
    role=UserRole.PARENT
)
session.add(user)

# 创建测试学生
student = Student(
    id=str(uuid4()),
    name="乐乐",
    grade=2
)
session.add(student)

# 创建绑定关系
binding = UserStudentBinding(
    id=str(uuid4()),
    user_id=user.id,
    student_id=student.id,
    relation=RelationType.FATHER,
    status=ApprovalStatus.APPROVED
)
session.add(binding)

# 创建登录码
login_code = LoginCode(
    id=str(uuid4()),
    code="TEST-1234-5678",
    status=LoginCodeStatus.ACTIVE,
    note="测试登录码"
)
session.add(login_code)

session.commit()

print("✅ 测试数据创建成功！")
print(f"   用户ID: {user.id}")
print(f"   学生ID: {student.id}")
print(f"   学生姓名: {student.name}")