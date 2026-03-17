#!/usr/bin/env python3
"""
生成静态登录码
用于家庭/小范围使用，避免微信小程序认证费用

使用方法：
    python3 scripts/generate_login_codes.py 100
"""
import sys
import os
import random
import string
from datetime import datetime, timedelta
from uuid import uuid4

# 添加 backend 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models import Database, LoginCode, LoginCodeStatus

def generate_code():
    """生成登录码：FAMILY-XXXX-XXXX"""
    chars = string.ascii_uppercase + string.digits
    part1 = ''.join(random.choices(chars, k=4))
    part2 = ''.join(random.choices(chars, k=4))
    return f"FAMILY-{part1}-{part2}"

def generate_login_codes(count=100, expire_days=365, max_uses=None, output_file=None):
    """生成一批登录码
    
    Args:
        count: 生成数量
        expire_days: 过期天数（365=1 年，None=永不过期）
        max_uses: 最大使用次数（None=无限次）
        output_file: 输出文件路径
    """
    # 确保目录存在
    os.makedirs('data', exist_ok=True)
    
    db = Database("data/prod.db")
    session = db.get_session()
    
    codes = []
    for i in range(count):
        code = generate_code()
        
        # 检查是否重复
        attempts = 0
        while session.query(LoginCode).filter(LoginCode.code == code).first():
            code = generate_code()
            attempts += 1
            if attempts > 100:
                print(f"⚠️  警告：生成唯一代码困难，当前已生成 {i} 个")
                break
        
        login_code = LoginCode(
            id=str(uuid4()),
            code=code,
            status=LoginCodeStatus.ACTIVE,
            max_uses=max_uses,
            expires_at=datetime.utcnow() + timedelta(days=expire_days) if expire_days else None,
            note="生产环境登录码"
        )
        
        session.add(login_code)
        codes.append(code)
        
        # 进度显示
        if (i + 1) % 10 == 0:
            print(f"已生成 {i + 1}/{count} 个登录码...")
    
    session.commit()
    session.close()
    
    # 输出到文件
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"login_codes_{timestamp}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# AI 伴学小程序 - 登录码列表\n")
        f.write(f"# 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# 数量：{count}\n")
        f.write(f"# 过期时间：{expire_days}天（如设置）\n")
        f.write(f"# 使用次数：{'无限次' if max_uses is None else f'{max_uses}次'}\n")
        f.write("#\n")
        f.write("# 使用说明：\n")
        f.write("# 1. 将此文件安全保存，不要上传到 Git\n")
        f.write("# 2. 将登录码分发给家长使用\n")
        f.write("# 3. 首次登录自动识别为管理员\n")
        f.write("# 4. 管理员可以绑定孩子账号\n")
        f.write("#\n")
        f.write("# ====================\n\n")
        
        for idx, code in enumerate(codes, 1):
            f.write(f"{idx:3d}. {code}\n")
    
    return codes, output_file

if __name__ == "__main__":
    # 解析命令行参数
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    expire_days = int(sys.argv[2]) if len(sys.argv) > 2 else 365
    max_uses = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    print(f"🔑 开始生成 {count} 个登录码...")
    print(f"   - 过期时间：{expire_days}天")
    print(f"   - 使用次数：{'无限次' if max_uses is None else f'{max_uses}次'}")
    print()
    
    try:
        codes, output_file = generate_login_codes(count, expire_days, max_uses)
        
        print()
        print(f"✅ 生成成功！")
        print(f"📁 文件：{output_file}")
        print(f"📊 统计:")
        print(f"   - 总数量：{count}")
        print(f"   - 文件大小：{os.path.getsize(output_file) / 1024:.2f} KB")
        print()
        print(f"📝 示例登录码（前 5 个）：")
        for i, code in enumerate(codes[:5], 1):
            print(f"   {i}. {code}")
        print()
        print(f"⚠️  重要提示:")
        print(f"   1. 将此文件安全保存，不要上传到 Git")
        print(f"   2. 建议备份到安全位置")
        print(f"   3. 分发给家长时注意保密")
        print(f"   4. 首次登录的登录码自动识别为管理员")
        print()
        print(f"💡 下一步:")
        print(f"   1. 将登录码分发给家长")
        print(f"   2. 家长使用登录码登录小程序")
        print(f"   3. 管理员绑定孩子账号")
        
    except Exception as e:
        print(f"❌ 生成失败：{e}")
        sys.exit(1)
