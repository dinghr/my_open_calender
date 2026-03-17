"""
AI 伴学小程序 - API 路由
"""
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import (
    Database, User, Student, UserStudentBinding, InviteLink, TeacherAdvice,
    LearningRecord, Subject, RelationType, ApprovalStatus, InviteLinkStatus,
    RecordType, RecordStatus,
    SpinosaurusRecord, PointsRecord, Reward, RewardRedemption, WishListItem,
    Book, ReadingRecord, Bookshelf
)
from ai_service import ai_service

# 数据库实例
db = Database("data/app.db")

# 获取数据库会话
def get_db():
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()


# ==================== Pydantic 模型 ====================

class InviteLinkCreate(BaseModel):
    """创建邀请链接请求"""
    student_id: str
    expire_type: str = "7days"  # 7days, 30days, forever
    usage_type: str = "once"  # once, multiple


class InviteLinkResponse(BaseModel):
    """邀请链接响应"""
    id: str
    code: str
    student_id: str
    student_name: str
    expire_type: str
    usage_type: str
    max_uses: int
    current_uses: int
    status: str
    expires_at: Optional[datetime]
    created_at: datetime
    link_url: str


class TeacherAdviceCreate(BaseModel):
    """创建老师建议请求"""
    student_id: str
    raw_content: str = Field(..., min_length=10, description="老师建议原文")


class TeacherAdviceParseResult(BaseModel):
    """AI 解析结果"""
    subject: Optional[str]
    topic: Optional[str]
    knowledge_points: List[str]
    tasks: List[dict]
    reminders: List[str]


class TeacherAdviceResponse(BaseModel):
    """老师建议响应"""
    id: str
    student_id: str
    raw_content: str
    subject: Optional[str]
    topic: Optional[str]
    knowledge_points: Optional[List[str]]
    tasks: Optional[List[dict]]
    reminders: Optional[List[str]]
    is_parsed: bool
    is_confirmed: bool
    created_at: datetime


class BindingCreate(BaseModel):
    """创建绑定请求"""
    invite_code: str
    relation: RelationType


class BindingResponse(BaseModel):
    """绑定关系响应"""
    id: str
    user_id: str
    user_nickname: str
    student_id: str
    student_name: str
    relation: str
    status: str
    created_at: datetime


class DailyPracticeResponse(BaseModel):
    """每日一练响应"""
    id: str
    student_id: str
    subject: str
    content: dict
    status: str
    parent_verified: bool
    date: str


# ==================== 路由 ====================

router = APIRouter(prefix="/api/v1")


# ---------- 邀请链接 API ----------

@router.post("/invite-links", response_model=InviteLinkResponse)
def create_invite_link(
    data: InviteLinkCreate,
    user_id: str = "default-user",  # TODO: 从认证获取
    session: Session = Depends(get_db)
):
    """创建邀请链接"""
    # 检查学生是否存在
    student = session.query(Student).filter(Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")

    # 检查用户是否有权限邀请
    binding = session.query(UserStudentBinding).filter(
        UserStudentBinding.user_id == user_id,
        UserStudentBinding.student_id == data.student_id,
        UserStudentBinding.status == ApprovalStatus.APPROVED
    ).first()
    if not binding:
        raise HTTPException(status_code=403, detail="您没有权限邀请他人绑定此学生")

    # 生成邀请码
    code = f"INV-{uuid4().hex[:8].upper()}"

    # 计算过期时间
    expires_at = None
    max_uses = 1 if data.usage_type == "once" else None

    if data.expire_type == "7days":
        expires_at = datetime.utcnow() + timedelta(days=7)
    elif data.expire_type == "30days":
        expires_at = datetime.utcnow() + timedelta(days=30)

    # 创建邀请链接
    invite = InviteLink(
        id=str(uuid4()),
        code=code,
        student_id=data.student_id,
        created_by=user_id,
        expire_type=data.expire_type,
        usage_type=data.usage_type,
        max_uses=max_uses,
        expires_at=expires_at,
        status=InviteLinkStatus.ACTIVE
    )

    session.add(invite)
    session.commit()

    return InviteLinkResponse(
        id=invite.id,
        code=invite.code,
        student_id=invite.student_id,
        student_name=student.name,
        expire_type=invite.expire_type,
        usage_type=invite.usage_type,
        max_uses=invite.max_uses or 0,
        current_uses=invite.current_uses,
        status=invite.status.value,
        expires_at=invite.expires_at,
        created_at=invite.created_at,
        link_url=f"https://ai-study.com/invite/{invite.code}"
    )


@router.get("/invite-links/{student_id}", response_model=List[InviteLinkResponse])
def get_invite_links(
    student_id: str,
    user_id: str = "default-user",
    session: Session = Depends(get_db)
):
    """获取学生的邀请链接列表"""
    # 检查权限
    binding = session.query(UserStudentBinding).filter(
        UserStudentBinding.user_id == user_id,
        UserStudentBinding.student_id == student_id,
        UserStudentBinding.status == ApprovalStatus.APPROVED
    ).first()
    if not binding:
        raise HTTPException(status_code=403, detail="没有权限查看")

    invites = session.query(InviteLink).filter(
        InviteLink.student_id == student_id,
        InviteLink.created_by == user_id
    ).order_by(InviteLink.created_at.desc()).all()

    student = session.query(Student).filter(Student.id == student_id).first()

    return [
        InviteLinkResponse(
            id=inv.id,
            code=inv.code,
            student_id=inv.student_id,
            student_name=student.name if student else "",
            expire_type=inv.expire_type,
            usage_type=inv.usage_type,
            max_uses=inv.max_uses or 0,
            current_uses=inv.current_uses,
            status=inv.status.value,
            expires_at=inv.expires_at,
            created_at=inv.created_at,
            link_url=f"https://ai-study.com/invite/{inv.code}"
        )
        for inv in invites
    ]


@router.post("/invite-links/{code}/disable")
def disable_invite_link(
    code: str,
    user_id: str = "default-user",
    session: Session = Depends(get_db)
):
    """关闭邀请链接"""
    invite = session.query(InviteLink).filter(InviteLink.code == code).first()
    if not invite:
        raise HTTPException(status_code=404, detail="邀请链接不存在")

    if invite.created_by != user_id:
        raise HTTPException(status_code=403, detail="没有权限操作")

    invite.status = InviteLinkStatus.DISABLED
    invite.disabled_at = datetime.utcnow()
    session.commit()

    return {"message": "邀请链接已关闭"}


# ---------- 账号绑定 API ----------

@router.post("/bindings", response_model=BindingResponse)
def create_binding(
    data: BindingCreate,
    user_id: str = "default-user",
    session: Session = Depends(get_db)
):
    """通过邀请码申请绑定"""
    # 查找邀请链接
    invite = session.query(InviteLink).filter(InviteLink.code == data.invite_code).first()
    if not invite:
        raise HTTPException(status_code=404, detail="邀请码无效")

    # 检查邀请链接状态
    if invite.status != InviteLinkStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="邀请链接已失效")

    # 检查是否过期
    if invite.expires_at and invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="邀请链接已过期")

    # 检查使用次数
    if invite.max_uses and invite.current_uses >= invite.max_uses:
        raise HTTPException(status_code=400, detail="邀请链接已用完")

    # 检查是否已绑定
    existing = session.query(UserStudentBinding).filter(
        UserStudentBinding.user_id == user_id,
        UserStudentBinding.student_id == invite.student_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="您已绑定此学生")

    # 创建绑定申请
    binding = UserStudentBinding(
        id=str(uuid4()),
        user_id=user_id,
        student_id=invite.student_id,
        relation=data.relation,
        status=ApprovalStatus.PENDING,
        invite_link_id=invite.id
    )

    # 更新邀请链接使用次数
    invite.current_uses += 1
    if invite.max_uses and invite.current_uses >= invite.max_uses:
        invite.status = InviteLinkStatus.USED

    session.add(binding)
    session.commit()

    user = session.query(User).filter(User.id == user_id).first()
    student = session.query(Student).filter(Student.id == invite.student_id).first()

    return BindingResponse(
        id=binding.id,
        user_id=binding.user_id,
        user_nickname=user.nickname if user else "",
        student_id=binding.student_id,
        student_name=student.name if student else "",
        relation=binding.relation.value,
        status=binding.status.value,
        created_at=binding.created_at
    )


@router.get("/bindings", response_model=List[BindingResponse])
def get_bindings(
    user_id: str = "default-user",
    session: Session = Depends(get_db)
):
    """获取当前用户的绑定关系"""
    bindings = session.query(UserStudentBinding).filter(
        UserStudentBinding.user_id == user_id
    ).all()

    result = []
    for b in bindings:
        user = session.query(User).filter(User.id == b.user_id).first()
        student = session.query(Student).filter(Student.id == b.student_id).first()
        result.append(BindingResponse(
            id=b.id,
            user_id=b.user_id,
            user_nickname=user.nickname if user else "",
            student_id=b.student_id,
            student_name=student.name if student else "",
            relation=b.relation.value,
            status=b.status.value,
            created_at=b.created_at
        ))

    return result


@router.post("/bindings/{binding_id}/approve")
def approve_binding(
    binding_id: str,
    user_id: str = "default-user",
    session: Session = Depends(get_db)
):
    """审批绑定申请（管理员）"""
    # TODO: 检查管理员权限

    binding = session.query(UserStudentBinding).filter(
        UserStudentBinding.id == binding_id
    ).first()
    if not binding:
        raise HTTPException(status_code=404, detail="绑定申请不存在")

    binding.status = ApprovalStatus.APPROVED
    binding.approved_at = datetime.utcnow()
    binding.approved_by = user_id
    session.commit()

    return {"message": "绑定已批准"}


# ---------- 老师学习建议 API ----------

@router.post("/teacher-advices", response_model=TeacherAdviceResponse)
def create_teacher_advice(
    data: TeacherAdviceCreate,
    user_id: str = "default-user",
    session: Session = Depends(get_db)
):
    """创建老师学习建议"""
    # 检查学生是否存在
    student = session.query(Student).filter(Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")

    advice = TeacherAdvice(
        id=str(uuid4()),
        student_id=data.student_id,
        user_id=user_id,
        raw_content=data.raw_content,
        is_parsed=False,
        is_confirmed=False
    )

    session.add(advice)
    session.commit()

    return TeacherAdviceResponse(
        id=advice.id,
        student_id=advice.student_id,
        raw_content=advice.raw_content,
        subject=advice.subject.value if advice.subject else None,
        topic=advice.topic,
        knowledge_points=advice.knowledge_points,
        tasks=advice.tasks,
        reminders=advice.reminders,
        is_parsed=advice.is_parsed,
        is_confirmed=advice.is_confirmed,
        created_at=advice.created_at
    )


@router.post("/teacher-advices/{advice_id}/parse", response_model=TeacherAdviceResponse)
async def parse_teacher_advice(
    advice_id: str,
    session: Session = Depends(get_db)
):
    """AI 解析老师建议"""
    advice = session.query(TeacherAdvice).filter(TeacherAdvice.id == advice_id).first()
    if not advice:
        raise HTTPException(status_code=404, detail="建议不存在")

    # 调用真实 AI 服务解析
    try:
        result = await ai_service.parse_teacher_advice(advice.raw_content)

        # 根据解析结果设置学科
        if result.get("subject") == "math":
            advice.subject = Subject.MATH
        else:
            advice.subject = Subject.CHINESE

        advice.topic = result.get("topic", "")
        advice.knowledge_points = result.get("knowledge_points", [])
        advice.tasks = result.get("tasks", [])
        advice.reminders = result.get("reminders", [])
        advice.is_parsed = True

    except Exception as e:
        # 如果 AI 调用失败，记录错误但仍返回结果
        print(f"AI 解析错误: {e}")
        advice.is_parsed = False
        raise HTTPException(status_code=500, detail=f"AI 解析失败: {str(e)}")

    session.commit()

    return TeacherAdviceResponse(
        id=advice.id,
        student_id=advice.student_id,
        raw_content=advice.raw_content,
        subject=advice.subject.value if advice.subject else None,
        topic=advice.topic,
        knowledge_points=advice.knowledge_points,
        tasks=advice.tasks,
        reminders=advice.reminders,
        is_parsed=advice.is_parsed,
        is_confirmed=advice.is_confirmed,
        created_at=advice.created_at
    )


@router.post("/teacher-advices/{advice_id}/confirm")
def confirm_teacher_advice(
    advice_id: str,
    session: Session = Depends(get_db)
):
    """确认老师建议并添加到计划"""
    advice = session.query(TeacherAdvice).filter(TeacherAdvice.id == advice_id).first()
    if not advice:
        raise HTTPException(status_code=404, detail="建议不存在")

    if not advice.is_parsed:
        raise HTTPException(status_code=400, detail="请先解析建议内容")

    advice.is_confirmed = True
    advice.confirmed_at = datetime.utcnow()

    # 创建学习记录
    if advice.tasks:
        for task in advice.tasks:
            record = LearningRecord(
                id=str(uuid4()),
                student_id=advice.student_id,
                date=datetime.utcnow().date(),
                type=RecordType.TASK,
                subject=advice.subject,
                content=task,
                status=RecordStatus.PENDING
            )
            session.add(record)

    session.commit()

    return {"message": "已确认并添加到学习计划"}


@router.get("/teacher-advices/{student_id}", response_model=List[TeacherAdviceResponse])
def get_teacher_advices(
    student_id: str,
    session: Session = Depends(get_db)
):
    """获取学生的学习建议列表"""
    advices = session.query(TeacherAdvice).filter(
        TeacherAdvice.student_id == student_id
    ).order_by(TeacherAdvice.created_at.desc()).limit(10).all()

    return [
        TeacherAdviceResponse(
            id=a.id,
            student_id=a.student_id,
            raw_content=a.raw_content,
            subject=a.subject.value if a.subject else None,
            topic=a.topic,
            knowledge_points=a.knowledge_points,
            tasks=a.tasks,
            reminders=a.reminders,
            is_parsed=a.is_parsed,
            is_confirmed=a.is_confirmed,
            created_at=a.created_at
        )
        for a in advices
    ]


# ---------- 每日一练 API ----------

@router.get("/daily-practice/{student_id}", response_model=List[DailyPracticeResponse])
def get_daily_practice(
    student_id: str,
    date: Optional[str] = None,
    session: Session = Depends(get_db)
):
    """获取每日一练内容（语文+数学）"""
    target_date = datetime.strptime(date, "%Y-%m-%d").date() if date else datetime.utcnow().date()

    records = session.query(LearningRecord).filter(
        LearningRecord.student_id == student_id,
        LearningRecord.date == target_date,
        LearningRecord.type == RecordType.DAILY_QUESTION,
        LearningRecord.subject.in_([Subject.CHINESE, Subject.MATH])
    ).all()

    return [
        DailyPracticeResponse(
            id=r.id,
            student_id=r.student_id,
            subject=r.subject.value if r.subject else "",
            content=r.content or {},
            status=r.status.value,
            parent_verified=r.parent_verified,
            date=str(r.date)
        )
        for r in records
    ]


@router.post("/daily-practice/{record_id}/verify")
def verify_daily_practice(
    record_id: str,
    session: Session = Depends(get_db)
):
    """家长确认每日一练"""
    record = session.query(LearningRecord).filter(LearningRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")

    record.parent_verified = True
    session.commit()

    return {"message": "已确认"}


@router.post("/daily-practice/{record_id}/complete")
def complete_daily_practice(
    record_id: str,
    session: Session = Depends(get_db)
):
    """完成每日一练"""
    record = session.query(LearningRecord).filter(LearningRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")

    record.status = RecordStatus.COMPLETED
    record.completed_at = datetime.utcnow()
    session.commit()

    return {"message": "已完成"}


# ---------- 棘龙伙伴 API ----------

class SpinosaurusResponse(BaseModel):
    """棘龙响应"""
    id: str
    student_id: str
    level: int
    attack: int
    defense: int
    experience: int
    streak_days: int
    exp_percent: float
    exp_to_next: int


@router.get("/spinosaurus/{student_id}", response_model=SpinosaurusResponse)
def get_spinosaurus(
    student_id: str,
    session: Session = Depends(get_db)
):
    """获取棘龙数据"""
    record = session.query(SpinosaurusRecord).filter(
        SpinosaurusRecord.student_id == student_id
    ).first()

    if not record:
        # 创建初始记录
        record = SpinosaurusRecord(
            id=str(uuid4()),
            student_id=student_id,
            level=1,
            attack=100,
            defense=50,
            experience=0,
            streak_days=0
        )
        session.add(record)
        session.commit()

    # 计算经验百分比和升级所需经验
    exp_per_level = 100  # 每级需要100经验
    current_level_exp = record.level * exp_per_level
    exp_percent = (record.experience % exp_per_level) / exp_per_level * 100
    exp_to_next = exp_per_level - (record.experience % exp_per_level)

    return SpinosaurusResponse(
        id=record.id,
        student_id=record.student_id,
        level=record.level,
        attack=record.attack,
        defense=record.defense,
        experience=record.experience,
        streak_days=record.streak_days,
        exp_percent=exp_percent,
        exp_to_next=exp_to_next
    )


class SpinosaurusUpdate(BaseModel):
    """棘龙更新"""
    attack_bonus: int = 0
    defense_bonus: int = 0
    exp_bonus: int = 0


@router.post("/spinosaurus/{student_id}/update")
def update_spinosaurus(
    student_id: str,
    data: SpinosaurusUpdate,
    session: Session = Depends(get_db)
):
    """更新棘龙属性（任务完成后调用）"""
    record = session.query(SpinosaurusRecord).filter(
        SpinosaurusRecord.student_id == student_id
    ).first()

    if not record:
        record = SpinosaurusRecord(
            id=str(uuid4()),
            student_id=student_id,
            level=1,
            attack=100,
            defense=50,
            experience=0,
            streak_days=0
        )
        session.add(record)

    # 更新属性
    record.attack += data.attack_bonus
    record.defense += data.defense_bonus
    record.experience += data.exp_bonus

    # 检查升级
    exp_per_level = 100
    while record.experience >= record.level * exp_per_level:
        record.level += 1
        record.attack += 10
        record.defense += 5

    session.commit()

    return {
        "message": "更新成功",
        "level": record.level,
        "attack": record.attack,
        "defense": record.defense,
        "experience": record.experience
    }


# ---------- 积分系统 API ----------

class PointsResponse(BaseModel):
    """积分响应"""
    student_id: str
    total_points: int
    level: str
    level_name: str


@router.get("/points/{student_id}", response_model=PointsResponse)
def get_points(
    student_id: str,
    session: Session = Depends(get_db)
):
    """获取积分"""
    # 计算总积分
    records = session.query(PointsRecord).filter(
        PointsRecord.student_id == student_id
    ).all()

    total = sum(r.points for r in records)

    # 确定等级
    if total >= 2000:
        level = "sun"
        level_name = "☀️ 太阳等级"
    elif total >= 700:
        level = "moon"
        level_name = "🌙 月亮等级"
    else:
        level = "star"
        level_name = "⭐ 星星等级"

    return PointsResponse(
        student_id=student_id,
        total_points=total,
        level=level,
        level_name=level_name
    )


class PointsAdd(BaseModel):
    """添加积分"""
    points: int
    source: str
    source_id: Optional[str] = None
    description: Optional[str] = None


@router.post("/points/{student_id}/add")
def add_points(
    student_id: str,
    data: PointsAdd,
    session: Session = Depends(get_db)
):
    """添加积分"""
    # 获取当前余额
    records = session.query(PointsRecord).filter(
        PointsRecord.student_id == student_id
    ).all()
    current_balance = sum(r.points for r in records)

    # 创建记录
    record = PointsRecord(
        id=str(uuid4()),
        student_id=student_id,
        points=data.points,
        source=data.source,
        source_id=data.source_id,
        description=data.description,
        balance_after=current_balance + data.points
    )

    session.add(record)
    session.commit()

    return {
        "message": "积分已添加",
        "points_added": data.points,
        "new_balance": current_balance + data.points
    }


# ---------- 奖励系统 API ----------

class RewardResponse(BaseModel):
    """奖励响应"""
    id: str
    name: str
    description: Optional[str]
    icon: Optional[str]
    points_cost: int
    required_level: str
    is_active: bool


class RewardItem(BaseModel):
    """奖励项"""
    id: str
    name: str
    description: Optional[str]
    icon: Optional[str]
    points_cost: int
    required_level: str
    can_exchange: bool
    status_text: str


@router.get("/rewards", response_model=List[RewardResponse])
def get_rewards(session: Session = Depends(get_db)):
    """获取可兑换奖励列表"""
    rewards = session.query(Reward).filter(Reward.is_active == True).all()

    if not rewards:
        # 初始化默认奖励
        default_rewards = [
            {"name": "冰淇淋一支", "description": "任意口味，周末享用", "icon": "🍦", "points_cost": 50, "required_level": "star"},
            {"name": "游戏时间 30 分钟", "description": "周末使用，需家长同意", "icon": "🎮", "points_cost": 100, "required_level": "star"},
            {"name": "看一部电影", "description": "周末家庭电影夜", "icon": "🎬", "points_cost": 200, "required_level": "star"},
            {"name": "游乐园一日游", "description": "需要月亮等级解锁", "icon": "🎢", "points_cost": 500, "required_level": "moon"},
            {"name": "心愿礼物（100元内）", "description": "需要太阳等级解锁", "icon": "🎁", "points_cost": 1000, "required_level": "sun"},
        ]

        for r in default_rewards:
            reward = Reward(
                id=str(uuid4()),
                name=r["name"],
                description=r["description"],
                icon=r["icon"],
                points_cost=r["points_cost"],
                required_level=r["required_level"]
            )
            session.add(reward)

        session.commit()
        rewards = session.query(Reward).filter(Reward.is_active == True).all()

    return [RewardResponse(
        id=r.id,
        name=r.name,
        description=r.description,
        icon=r.icon,
        points_cost=r.points_cost,
        required_level=r.required_level,
        is_active=r.is_active
    ) for r in rewards]


@router.get("/rewards/{student_id}", response_model=List[RewardItem])
def get_student_rewards(
    student_id: str,
    session: Session = Depends(get_db)
):
    """获取学生可兑换的奖励"""
    rewards = session.query(Reward).filter(Reward.is_active == True).all()

    if not rewards:
        # 初始化默认奖励
        get_rewards(session)
        rewards = session.query(Reward).filter(Reward.is_active == True).all()

    # 获取学生积分和等级
    records = session.query(PointsRecord).filter(
        PointsRecord.student_id == student_id
    ).all()
    total_points = sum(r.points for r in records)

    if total_points >= 2000:
        student_level = "sun"
    elif total_points >= 700:
        student_level = "moon"
    else:
        student_level = "star"

    level_order = {"star": 1, "moon": 2, "sun": 3}

    result = []
    for r in rewards:
        can_exchange = (
            level_order.get(student_level, 0) >= level_order.get(r.required_level, 0)
            and total_points >= r.points_cost
        )

        if level_order.get(student_level, 0) < level_order.get(r.required_level, 0):
            status_text = "🔒 等级不足"
        elif total_points < r.points_cost:
            status_text = "积分不足"
        else:
            status_text = "兑换"

        result.append(RewardItem(
            id=r.id,
            name=r.name,
            description=r.description,
            icon=r.icon,
            points_cost=r.points_cost,
            required_level=r.required_level,
            can_exchange=can_exchange,
            status_text=status_text
        ))

    return result


@router.post("/rewards/{student_id}/exchange/{reward_id}")
def exchange_reward(
    student_id: str,
    reward_id: str,
    session: Session = Depends(get_db)
):
    """兑换奖励"""
    reward = session.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="奖励不存在")

    # 获取学生积分
    records = session.query(PointsRecord).filter(
        PointsRecord.student_id == student_id
    ).all()
    total_points = sum(r.points for r in records)

    if total_points < reward.points_cost:
        raise HTTPException(status_code=400, detail="积分不足")

    # 创建兑换记录
    redemption = RewardRedemption(
        id=str(uuid4()),
        student_id=student_id,
        reward_id=reward_id,
        points_spent=reward.points_cost,
        status="pending"
    )
    session.add(redemption)

    # 扣除积分
    points_record = PointsRecord(
        id=str(uuid4()),
        student_id=student_id,
        points=-reward.points_cost,
        source="reward_exchange",
        source_id=redemption.id,
        description=f"兑换「{reward.name}」",
        balance_after=total_points - reward.points_cost
    )
    session.add(points_record)

    session.commit()

    return {
        "message": "兑换成功",
        "redemption_id": redemption.id,
        "reward_name": reward.name,
        "points_spent": reward.points_cost
    }


# ---------- 愿望清单 API ----------

class WishCreate(BaseModel):
    """创建愿望"""
    content: str
    icon: Optional[str] = "🎁"


class WishResponse(BaseModel):
    """愿望响应"""
    id: str
    content: str
    icon: str
    status: str
    parent_response: Optional[str]
    created_at: datetime


@router.get("/wishes/{student_id}", response_model=List[WishResponse])
def get_wishes(
    student_id: str,
    session: Session = Depends(get_db)
):
    """获取愿望清单"""
    wishes = session.query(WishListItem).filter(
        WishListItem.student_id == student_id
    ).order_by(WishListItem.created_at.desc()).all()

    return [WishResponse(
        id=w.id,
        content=w.content,
        icon=w.icon or "🎁",
        status=w.status,
        parent_response=w.parent_response,
        created_at=w.created_at
    ) for w in wishes]


@router.post("/wishes/{student_id}", response_model=WishResponse)
def create_wish(
    student_id: str,
    data: WishCreate,
    session: Session = Depends(get_db)
):
    """创建愿望"""
    wish = WishListItem(
        id=str(uuid4()),
        student_id=student_id,
        content=data.content,
        icon=data.icon or "🎁",
        status="pending"
    )

    session.add(wish)
    session.commit()

    return WishResponse(
        id=wish.id,
        content=wish.content,
        icon=wish.icon or "🎁",
        status=wish.status,
        parent_response=wish.parent_response,
        created_at=wish.created_at
    )


class WishReply(BaseModel):
    """家长回复"""
    status: str  # approved, rejected, pending
    response: str


@router.post("/wishes/{wish_id}/reply")
def reply_wish(
    wish_id: str,
    data: WishReply,
    session: Session = Depends(get_db)
):
    """家长回复愿望"""
    wish = session.query(WishListItem).filter(WishListItem.id == wish_id).first()
    if not wish:
        raise HTTPException(status_code=404, detail="愿望不存在")

    wish.status = data.status
    wish.parent_response = data.response
    wish.responded_at = datetime.utcnow()

    session.commit()

    return {"message": "回复成功"}


# ---------- 阅读系统 API ----------

class ReadingStatsResponse(BaseModel):
    """阅读统计响应"""
    student_id: str
    total_words: int
    completed_books: int
    reading_books: int
    total_points: int


@router.get("/reading/{student_id}/stats", response_model=ReadingStatsResponse)
def get_reading_stats(
    student_id: str,
    session: Session = Depends(get_db)
):
    """获取阅读统计"""
    records = session.query(ReadingRecord).filter(
        ReadingRecord.student_id == student_id
    ).all()

    total_words = sum(r.words_read or 0 for r in records)
    completed_books = sum(1 for r in records if r.status == "completed")
    reading_books = sum(1 for r in records if r.status == "reading")
    total_points = sum(r.points_earned or 0 for r in records)

    return ReadingStatsResponse(
        student_id=student_id,
        total_words=total_words,
        completed_books=completed_books,
        reading_books=reading_books,
        total_points=total_points
    )


class ReadingRecordResponse(BaseModel):
    """阅读记录响应"""
    id: str
    book_id: str
    book_title: str
    book_icon: str
    status: str
    progress: int
    words_read: int
    points_earned: int


@router.get("/reading/{student_id}/records", response_model=List[ReadingRecordResponse])
def get_reading_records(
    student_id: str,
    status: Optional[str] = None,
    session: Session = Depends(get_db)
):
    """获取阅读记录"""
    query = session.query(ReadingRecord).filter(
        ReadingRecord.student_id == student_id
    )

    if status:
        query = query.filter(ReadingRecord.status == status)

    records = query.all()

    result = []
    for r in records:
        book = session.query(Book).filter(Book.id == r.book_id).first()
        result.append(ReadingRecordResponse(
            id=r.id,
            book_id=r.book_id,
            book_title=book.title if book else "未知书籍",
            book_icon=book.cover_url or "📚" if book else "📚",
            status=r.status,
            progress=r.progress or 0,
            words_read=r.words_read or 0,
            points_earned=r.points_earned or 0
        ))

    return result


class ReadingProgressUpdate(BaseModel):
    """阅读进度更新"""
    progress: int
    words_read: int


@router.post("/reading/{record_id}/progress")
def update_reading_progress(
    record_id: str,
    data: ReadingProgressUpdate,
    session: Session = Depends(get_db)
):
    """更新阅读进度"""
    record = session.query(ReadingRecord).filter(ReadingRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")

    record.progress = data.progress
    record.words_read = data.words_read

    # 如果完成，计算积分
    if data.progress >= 100 and record.status != "completed":
        record.status = "completed"
        record.completed_at = datetime.utcnow()

        # 计算积分：每1000字 = 20积分
        points = (data.words_read // 1000) * 20

        # 创建积分记录
        points_record = PointsRecord(
            id=str(uuid4()),
            student_id=record.student_id,
            points=points,
            source="reading",
            source_id=record.id,
            description=f"完成阅读",
            balance_after=points
        )
        session.add(points_record)
        record.points_earned = points

    session.commit()

    return {"message": "进度已更新", "progress": data.progress}