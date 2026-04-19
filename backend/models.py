"""
AI 伴学小程序 - 数据库模型

数据库：SQLite
ORM: SQLAlchemy
"""

from datetime import datetime
from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Boolean, 
    DateTime, Date, ForeignKey, Text, Enum, JSON, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import enum

Base = declarative_base()


# ==================== 枚举类型 ====================

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    PARENT = "parent"


class RecordType(str, enum.Enum):
    DAILY_QUESTION = "daily_question"
    TASK = "task"
    PLAN = "plan"
    WRONG_QUESTION = "wrong_question"


class QuestionType(str, enum.Enum):
    """题型"""
    CHOICE = "choice"  # 选择题
    FILL_BLANK = "fill_blank"  # 填空题
    CALCULATION = "calculation"  # 计算题
    APPLICATION = "application"  # 应用题
    READING = "reading"  # 阅读理解
    WRITING = "writing"  # 作文
    POETRY = "poetry"  # 古诗
    CHARACTER = "character"  # 识字/写字


class Subject(str, enum.Enum):
    CHINESE = "chinese"
    MATH = "math"
    ENGLISH = "english"  # 保留英语用于其他功能，但每日一练只用语文和数学


class InviteLinkStatus(str, enum.Enum):
    """邀请链接状态"""
    ACTIVE = "active"
    USED = "used"
    EXPIRED = "expired"
    DISABLED = "disabled"


class ApprovalStatus(str, enum.Enum):
    """审批状态"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class RelationType(str, enum.Enum):
    """账号关系类型"""
    FATHER = "father"
    MOTHER = "mother"
    GRANDFATHER = "grandfather"
    GRANDMOTHER = "grandmother"
    MATERNAL_GRANDFATHER = "maternal_grandfather"
    MATERNAL_GRANDMOTHER = "maternal_grandmother"
    OTHER = "other"


class RecordStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    POSTPONED = "postponed"


class VocabularyStatus(str, enum.Enum):
    KNOWN = "known"
    LEARNING = "learning"
    UNKNOWN = "unknown"


class LoginCodeStatus(str, enum.Enum):
    ACTIVE = "active"
    USED = "used"
    DISABLED = "disabled"


class PoetryStatus(str, enum.Enum):
    LEARNING = "learning"
    REVIEWING = "reviewed"
    MASTERED = "mastered"


class MasteryLevel(str, enum.Enum):
    """掌握程度"""
    NEW = "new"  # 新学
    UNFAMILIAR = "unfamiliar"  # 不太熟
    FAMILIAR = "familiar"  # 熟悉
    MASTERED = "mastered"  # 会背了


class QuestionSource(str, enum.Enum):
    """题目来源"""
    TEXTBOOK = "textbook"  # 教材
    PARENT_IMPORT = "parent_import"  # 家长导入
    SCANNER = "scanner"  # 扫描录入
    AI_GENERATED = "ai_generated"  # AI 生成
    SYSTEM_PRESET = "system_preset"  # 系统预设


class WrongReason(str, enum.Enum):
    """错题原因"""
    CARELESS = "careless"  # 粗心
    CONCEPT_UNCLEAR = "concept_unclear"  # 概念不清
    METHOD_WRONG = "method_wrong"  # 方法错误
    NOT_LEARNED = "not_learned"  # 未学过
    OTHER = "other"  # 其他


# ==================== 核心数据模型 ====================

class User(Base):
    """用户表（家长/管理员）"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    login_code_id = Column(String(36), ForeignKey("login_codes.id"))
    nickname = Column(String(100))
    role = Column(Enum(UserRole), default=UserRole.PARENT)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    bindings = relationship("UserStudentBinding", foreign_keys="UserStudentBinding.user_id", back_populates="user")
    approved_bindings = relationship("UserStudentBinding", foreign_keys="UserStudentBinding.approved_by", backref="approver")
    teacher_advices = relationship("TeacherAdvice", back_populates="user")
    created_invites = relationship("InviteLink", foreign_keys="InviteLink.created_by", back_populates="creator")


class Student(Base):
    """学生表（小朋友）"""
    __tablename__ = "students"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    grade = Column(Integer)  # 年级
    birthday = Column(Date)  # 生日（用于年龄计算）
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    bindings = relationship("UserStudentBinding", back_populates="student")
    learning_records = relationship("LearningRecord", back_populates="student")
    vocabulary = relationship("Vocabulary", back_populates="student")
    growth_tree = relationship("GrowthTree", back_populates="student", uselist=False)
    poetry_memory = relationship("PoetryMemory", back_populates="student")
    poetry_learning = relationship("PoetryLearning", back_populates="student")
    wrong_questions = relationship("WrongQuestion", back_populates="student")
    teacher_advices = relationship("TeacherAdvice", back_populates="student")
    invite_links = relationship("InviteLink", back_populates="student")


class UserStudentBinding(Base):
    """用户 - 学生绑定关系（多对多）"""
    __tablename__ = "user_student_bindings"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    relation = Column(Enum(RelationType), default=RelationType.OTHER)  # 关系类型
    status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)  # 审批状态
    invite_link_id = Column(String(36), ForeignKey("invite_links.id"))  # 通过哪个邀请链接绑定
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime)  # 审批通过时间
    approved_by = Column(String(36), ForeignKey("users.id"))  # 审批人

    # 关系
    user = relationship("User", foreign_keys=[user_id], back_populates="bindings")
    student = relationship("Student", back_populates="bindings")
    invite_link = relationship("InviteLink", back_populates="bindings")

    __table_args__ = (
        UniqueConstraint('user_id', 'student_id', name='uq_user_student'),
    )


class InviteLink(Base):
    """邀请链接表"""
    __tablename__ = "invite_links"

    id = Column(String(36), primary_key=True)
    code = Column(String(50), unique=True, nullable=False)  # 邀请码
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)  # 邀请绑定的小朋友
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)  # 创建人

    # 链接设置
    expire_type = Column(String(20), default="7days")  # 7days, 30days, forever
    usage_type = Column(String(20), default="once")  # once, multiple
    max_uses = Column(Integer, default=1)  # 最大使用次数
    current_uses = Column(Integer, default=0)  # 当前使用次数

    # 状态
    status = Column(Enum(InviteLinkStatus), default=InviteLinkStatus.ACTIVE)
    expires_at = Column(DateTime)  # 过期时间

    created_at = Column(DateTime, default=datetime.utcnow)
    disabled_at = Column(DateTime)  # 手动关闭时间

    # 关系
    student = relationship("Student")
    creator = relationship("User", foreign_keys=[created_by])
    bindings = relationship("UserStudentBinding", foreign_keys="UserStudentBinding.invite_link_id", back_populates="invite_link")


class TeacherAdvice(Base):
    """老师学习建议表"""
    __tablename__ = "teacher_advices"

    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)  # 录入的家长

    # 原始内容
    raw_content = Column(Text, nullable=False)  # 家长粘贴的原始内容

    # AI 解析结果
    subject = Column(Enum(Subject))  # 学科
    topic = Column(String(200))  # 课题
    knowledge_points = Column(JSON)  # 知识点列表
    tasks = Column(JSON)  # 任务清单 [{"content": "...", "deadline": "..."}]
    reminders = Column(JSON)  # 提醒事项列表

    # 状态
    is_parsed = Column(Boolean, default=False)  # 是否已解析
    is_confirmed = Column(Boolean, default=False)  # 家长是否确认
    confirmed_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    student = relationship("Student")
    user = relationship("User")


class LoginCode(Base):
    """登录码表"""
    __tablename__ = "login_codes"
    
    id = Column(String(36), primary_key=True)
    code = Column(String(50), unique=True, nullable=False)  # 如 "FAMILY-XXXX-XXXX"
    status = Column(Enum(LoginCodeStatus), default=LoginCodeStatus.ACTIVE)
    max_uses = Column(Integer)  # 1=一次性，null=无限次
    current_uses = Column(Integer, default=0)
    bound_devices = Column(Integer)  # 绑定设备数限制（可选）
    created_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # 可选过期时间
    note = Column(String(200))  # 备注，如 "给孩子的登录码"


class LearningRecord(Base):
    """学习记录表"""
    __tablename__ = "learning_records"
    
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    type = Column(Enum(RecordType), nullable=False)
    subject = Column(Enum(Subject))
    content = Column(JSON)  # 题目内容、任务内容等
    status = Column(Enum(RecordStatus), default=RecordStatus.PENDING)
    parent_verified = Column(Boolean, default=False)  # 家长是否确认
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # 关系
    student = relationship("Student", back_populates="learning_records")


class Vocabulary(Base):
    """生字库表"""
    __tablename__ = "vocabulary"
    
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    character = Column(String(10), nullable=False)  # 汉字
    pinyin = Column(String(50))  # 拼音
    status = Column(Enum(VocabularyStatus), default=VocabularyStatus.UNKNOWN)
    learned_at = Column(DateTime)
    review_count = Column(Integer, default=0)
    last_reviewed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    student = relationship("Student", back_populates="vocabulary")
    
    __table_args__ = (
        UniqueConstraint('student_id', 'character', name='uq_student_character'),
    )


class GrowthTree(Base):
    """成长树状态表"""
    __tablename__ = "growth_tree"
    
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), unique=True, nullable=False)
    level = Column(Integer, default=1)  # 成长等级
    exp = Column(Integer, default=0)  # 经验值
    nutrients = Column(JSON)  # 养分来源记录 [{"date": "2026-03-12", "source": "task_completed", "count": 3}]
    appearance = Column(JSON)  # 外观状态 {"tree_type": "oak", "leaves": 10, "fruits": 3}
    last_watered = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # 关系
    student = relationship("Student", back_populates="growth_tree")


# ==================== 古诗系统 ====================

class Poetry(Base):
    """古诗库表"""
    __tablename__ = "poetry"

    id = Column(String(36), primary_key=True)
    title = Column(String(100), nullable=False)  # 诗题
    title_pinyin = Column(String(200))  # 诗题拼音
    author = Column(String(100))  # 作者
    dynasty = Column(String(50))  # 朝代

    # 诗句（每句包含文字和拼音）
    # [{"text": "床前明月光，", "pinyin": "chuáng qián míng yuè guāng", "chars": [{"char": "床", "pinyin": "chuáng"}, ...]}]
    lines = Column(JSON, nullable=False)

    translation = Column(Text)  # 译文
    annotation = Column(JSON)  # 注释 {"words": [...], "background": "..."}

    # 分类
    grade = Column(Integer)  # 适用年级
    semester = Column(String(20))  # 学期：上学期、下学期
    category = Column(String(50))  # 分类：必背、选背、拓展
    textbook = Column(String(50))  # 教材版本：人教版、北师大版等

    # 统计
    learn_count = Column(Integer, default=0)  # 学习人数

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    memory_records = relationship("PoetryMemory", back_populates="poetry")


class PoetryMemory(Base):
    """古诗记忆曲线表"""
    __tablename__ = "poetry_memory"

    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    poetry_id = Column(String(36), ForeignKey("poetry.id"), nullable=False)  # 古诗 ID
    poetry_title = Column(String(100))  # 古诗标题（冗余，方便查询）
    first_learned_at = Column(DateTime)
    last_reviewed_at = Column(DateTime)
    next_review_at = Column(DateTime)
    memory_strength = Column(Float, default=0.0)  # 记忆强度 0-1
    review_count = Column(Integer, default=0)  # 复习次数
    mastery_level = Column(Enum(MasteryLevel), default=MasteryLevel.NEW)  # 掌握程度
    status = Column(Enum(PoetryStatus), default=PoetryStatus.LEARNING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # 关系
    student = relationship("Student", back_populates="poetry_memory")
    poetry = relationship("Poetry", back_populates="memory_records")


class PoetryLearning(Base):
    """古诗学习记录 - AI动态生成方案"""
    __tablename__ = "poetry_learning"

    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)

    # 古诗标识（不依赖Poetry表）
    title = Column(String(100), nullable=False)       # 诗题
    author = Column(String(100))                      # 作者
    dynasty = Column(String(50))                      # 朝代
    grade = Column(Integer)                           # 年级
    semester = Column(String(20))                     # 学期
    textbook = Column(String(50))                     # 教材版本

    # 学习状态
    mastery_level = Column(Enum(MasteryLevel), default=MasteryLevel.NEW)
    review_count = Column(Integer, default=0)
    memory_strength = Column(Float, default=0.0)

    # 时间记录
    first_learned_at = Column(DateTime)
    last_reviewed_at = Column(DateTime)
    next_review_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # 关系
    student = relationship("Student", back_populates="poetry_learning")


class ParentAdjustment(Base):
    """家长调整记录表"""
    __tablename__ = "parent_adjustments"
    
    id = Column(String(36), primary_key=True)
    plan_id = Column(String(36), nullable=False)  # 关联的计划 ID
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    original_intent = Column(Text)  # 原始自然语言输入
    parsed_intent = Column(JSON)  # 解析后的意图
    weight_changes = Column(JSON)  # 权重调整详情
    adjustment_type = Column(String(50))  # content_swap, priority_change, skip_module
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== 题库与错题管理 ====================

class QuestionBank(Base):
    """题库表 - 所有题目的总库"""
    __tablename__ = "question_bank"
    
    id = Column(String(36), primary_key=True)
    subject = Column(Enum(Subject), nullable=False)  # 学科
    grade = Column(Integer)  # 适用年级
    unit = Column(String(100))  # 单元/章节
    knowledge_point = Column(String(200))  # 知识点标签
    question_type = Column(Enum(QuestionType))  # 题型
    source = Column(Enum(QuestionSource), default=QuestionSource.SYSTEM_PRESET)  # 来源
    
    # 题目内容
    content = Column(JSON, nullable=False)  # 题目内容 {"text": "...", "options": [...], "image": "..."}
    answer = Column(JSON)  # 答案 {"answer": "A", "explanation": "..."}
    analysis = Column(JSON)  # 解析 {"steps": [...], "tips": "..."}
    
    # 难度与统计
    difficulty = Column(Integer, default=1)  # 难度 1-5
    error_rate = Column(Float, default=0.0)  # 易错度 0-1（答错人数/总人数）
    wrong_count = Column(Integer, default=0)  # 答错次数
    total_count = Column(Integer, default=0)  # 总作答次数
    
    # 家长备课内容
    parent_guide = Column(JSON)  # 家长辅导指南 {"background": "...", "tips": "...", "common_mistakes": "..."}
    
    # 状态
    status = Column(String(20), default="active")  # active, archived, hidden
    created_by = Column(String(36), ForeignKey("users.id"))  # 创建者（家长导入时）
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # 关系
    wrong_questions = relationship("WrongQuestion", back_populates="question")


class WrongQuestion(Base):
    """错题表 - 学生的错题记录"""
    __tablename__ = "wrong_questions"
    
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    question_id = Column(String(36), ForeignKey("question_bank.id"))  # 关联题库（可选，家长导入的题目可能不在题库）
    
    # 题目快照（保留原始题目，即使题库修改也不影响）
    question_content = Column(JSON, nullable=False)  # 题目内容快照
    question_answer = Column(JSON)  # 答案快照
    subject = Column(Enum(Subject))  # 学科
    
    # 错题信息
    wrong_reason = Column(Enum(WrongReason))  # 错误原因
    student_answer = Column(JSON)  # 学生答案
    wrong_date = Column(Date, nullable=False)  # 错题日期
    source_type = Column(String(20))  # 来源类型：daily_question, scan, manual
    
    # 掌握情况
    mastered = Column(Boolean, default=False)  # 是否已掌握
    mastered_at = Column(DateTime)  # 掌握时间
    review_count = Column(Integer, default=0)  # 复习次数
    last_reviewed_at = Column(DateTime)  # 最后复习时间
    
    # 举一反三
    similar_questions = Column(JSON)  # 相似题 ID 列表
    similar_practice_done = Column(Boolean, default=False)  # 是否已完成相似题练习
    
    # 状态
    status = Column(String(20), default="active")  # active, mastered, archived
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # 关系
    student = relationship("Student", back_populates="wrong_questions")
    question = relationship("QuestionBank", back_populates="wrong_questions")


class KnowledgePoint(Base):
    """知识点表 - 学科知识点结构"""
    __tablename__ = "knowledge_points"
    
    id = Column(String(36), primary_key=True)
    subject = Column(Enum(Subject), nullable=False)
    grade = Column(Integer, nullable=False)
    semester = Column(String(20))  # 学期：fall, spring
    unit = Column(String(100))  # 单元
    name = Column(String(200), nullable=False)  # 知识点名称
    parent_id = Column(String(36), ForeignKey("knowledge_points.id"))  # 父知识点（层级结构）
    
    # 学习要点
    learning_points = Column(JSON)  # 学习要点列表
    common_mistakes = Column(JSON)  # 常见错误
    
    # 关联题目
    question_count = Column(Integer, default=0)  # 关联题目数量
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    children = relationship("KnowledgePoint", backref="parent", remote_side=[id])


# ==================== 棘龙与积分系统 ====================

class SpinosaurusRecord(Base):
    """棘龙记录表"""
    __tablename__ = "spinosaurus_records"

    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), unique=True, nullable=False)

    # 等级与属性
    level = Column(Integer, default=1)  # 等级 1-10
    attack = Column(Integer, default=100)  # 攻击力
    defense = Column(Integer, default=50)  # 防御力
    experience = Column(Integer, default=0)  # 经验值
    streak_days = Column(Integer, default=0)  # 连续打卡天数
    max_streak = Column(Integer, default=0)  # 最长连续天数

    # 外观
    appearance = Column(JSON)  # {"skin": "default", "accessory": "hat"}

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # 关系
    student = relationship("Student", backref="spinosaurus")


class PointsRecord(Base):
    """积分记录表"""
    __tablename__ = "points_records"

    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)

    # 积分变动
    points = Column(Integer, nullable=False)  # 变动数量（正数获得，负数消耗）
    source = Column(String(50), nullable=False)  # 来源：task_complete, reading, reward_exchange, bonus
    source_id = Column(String(36))  # 关联 ID（如任务 ID、阅读记录 ID）
    description = Column(String(200))  # 描述

    # 余额快照
    balance_after = Column(Integer)  # 变动后余额

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    student = relationship("Student", backref="points_records")


# ==================== 奖励系统 ====================

class Reward(Base):
    """奖励表"""
    __tablename__ = "rewards"

    id = Column(String(36), primary_key=True)

    # 基本信息
    name = Column(String(100), nullable=False)
    description = Column(String(200))
    icon = Column(String(50))  # emoji 图标

    # 兑换条件
    points_cost = Column(Integer, nullable=False)  # 积分消耗
    required_level = Column(String(20), default="star")  # 需要等级：star, moon, sun

    # 状态
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class RewardRedemption(Base):
    """奖励兑换记录表"""
    __tablename__ = "reward_redemptions"

    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    reward_id = Column(String(36), ForeignKey("rewards.id"), nullable=False)

    # 兑换信息
    points_spent = Column(Integer, nullable=False)
    status = Column(String(20), default="pending")  # pending, completed, cancelled

    # 完成信息
    completed_at = Column(DateTime)
    parent_note = Column(String(200))  # 家长备注

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    student = relationship("Student", backref="redemptions")
    reward = relationship("Reward")


class WishListItem(Base):
    """愿望清单表"""
    __tablename__ = "wish_list"

    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)

    # 愿望内容
    content = Column(String(200), nullable=False)
    icon = Column(String(50))  # emoji 图标

    # 状态
    status = Column(String(20), default="pending")  # pending, approved, rejected
    parent_response = Column(Text)  # 家长回复

    created_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime)

    # 关系
    student = relationship("Student", backref="wishes")


# ==================== 阅读系统 ====================

class Book(Base):
    """图书表"""
    __tablename__ = "books"

    id = Column(String(36), primary_key=True)

    # 基本信息
    title = Column(String(200), nullable=False)
    author = Column(String(100))
    word_count = Column(Integer)  # 字数
    category = Column(String(50))  # 分类
    description = Column(Text)
    cover_url = Column(String(500))

    # 推荐信息
    rating = Column(Float, default=0)  # 评分 1-5
    recommend_count = Column(Integer, default=0)  # 推荐数

    # 难度
    difficulty = Column(Integer, default=1)  # 难度 1-5
    suggested_days = Column(Integer)  # 建议阅读天数

    created_at = Column(DateTime, default=datetime.utcnow)


class ReadingRecord(Base):
    """阅读记录表"""
    __tablename__ = "reading_records"

    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    book_id = Column(String(36), ForeignKey("books.id"), nullable=False)

    # 阅读状态
    status = Column(String(20), default="reading")  # reading, completed
    progress = Column(Integer, default=0)  # 进度百分比 0-100
    words_read = Column(Integer, default=0)  # 已读字数

    # 时间
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    target_date = Column(Date)  # 目标完成日期

    # 读后感
    review_text = Column(Text)
    rating = Column(Integer)  # 评分 1-5

    # 积分
    points_earned = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # 关系
    student = relationship("Student", backref="reading_records")
    book = relationship("Book")


class Bookshelf(Base):
    """书架管理表"""
    __tablename__ = "bookshelf"

    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    book_id = Column(String(36), ForeignKey("books.id"), nullable=False)

    # 状态
    is_recommended = Column(Boolean, default=False)  # 是否推荐给书友
    is_lendable = Column(Boolean, default=False)  # 是否可借阅
    lend_status = Column(String(20), default="available")  # available, lent

    added_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    student = relationship("Student", backref="bookshelf")
    book = relationship("Book")


# ==================== 数据库连接 ====================

class Database:
    """数据库连接管理"""
    
    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = db_path
        self.engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False}  # SQLite 需要
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """创建所有表"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """获取数据库会话"""
        return self.SessionLocal()


# ==================== 初始化示例 ====================

if __name__ == "__main__":
    # 创建数据库和表
    db = Database()
    db.create_tables()
    print("✅ 数据库创建成功！")
    print(f"📁 数据库文件：{db.db_path}")
