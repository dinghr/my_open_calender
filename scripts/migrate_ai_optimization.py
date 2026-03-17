#!/usr/bin/env python3
"""
AI 伴学小程序 - AI 推荐优化迁移脚本

功能：添加 AI 推荐所需的字段和索引
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

from sqlalchemy import text


def migrate():
    """执行数据库迁移"""
    print("🚀 开始 AI 推荐优化迁移...")
    
    from models import Database
    db = Database("data/app.db")
    session = db.get_session()
    
    try:
        # ========== 1. question_bank 表优化 ==========
        print("\n📝 优化 question_bank 表...")
        
        # 添加 AI 特征字段
        session.execute(text("""
            ALTER TABLE question_bank ADD COLUMN ai_features JSON
        """))
        print("  ✅ 添加 ai_features 字段")
        
        # 添加知识点向量（用于相似度计算）
        session.execute(text("""
            ALTER TABLE question_bank ADD COLUMN knowledge_vector JSON
        """))
        print("  ✅ 添加 knowledge_vector 字段")
        
        session.commit()
        
        # ========== 2. wrong_questions 表优化 ==========
        print("\n📝 优化 wrong_questions 表...")
        
        # 添加错误详细分析
        session.execute(text("""
            ALTER TABLE wrong_questions ADD COLUMN error_analysis JSON
        """))
        print("  ✅ 添加 error_analysis 字段")
        
        # 添加掌握度评分
        session.execute(text("""
            ALTER TABLE wrong_questions ADD COLUMN mastery_score FLOAT
        """))
        print("  ✅ 添加 mastery_score 字段")
        
        # 添加推荐优先级
        session.execute(text("""
            ALTER TABLE wrong_questions ADD COLUMN recommendation_priority FLOAT
        """))
        print("  ✅ 添加 recommendation_priority 字段")
        
        # 添加相似题生成策略
        session.execute(text("""
            ALTER TABLE wrong_questions ADD COLUMN similar_strategy JSON
        """))
        print("  ✅ 添加 similar_strategy 字段")
        
        session.commit()
        
        # ========== 3. learning_records 表优化 ==========
        print("\n📝 优化 learning_records 表...")
        
        # 添加用时
        session.execute(text("""
            ALTER TABLE learning_records ADD COLUMN time_spent_seconds INTEGER
        """))
        print("  ✅ 添加 time_spent_seconds 字段")
        
        # 添加尝试次数
        session.execute(text("""
            ALTER TABLE learning_records ADD COLUMN attempt_count INTEGER DEFAULT 1
        """))
        print("  ✅ 添加 attempt_count 字段")
        
        # 添加 AI 评分
        session.execute(text("""
            ALTER TABLE learning_records ADD COLUMN ai_score FLOAT
        """))
        print("  ✅ 添加 ai_score 字段")
        
        # 添加行为数据
        session.execute(text("""
            ALTER TABLE learning_records ADD COLUMN behavior_data JSON
        """))
        print("  ✅ 添加 behavior_data 字段")
        
        session.commit()
        
        # ========== 4. vocabulary 表优化 ==========
        print("\n📝 优化 vocabulary 表...")
        
        # 添加字频排名
        session.execute(text("""
            ALTER TABLE vocabulary ADD COLUMN frequency_rank INTEGER
        """))
        print("  ✅ 添加 frequency_rank 字段")
        
        # 添加部首
        session.execute(text("""
            ALTER TABLE vocabulary ADD COLUMN radical VARCHAR(20)
        """))
        print("  ✅ 添加 radical 字段")
        
        # 添加笔画数
        session.execute(text("""
            ALTER TABLE vocabulary ADD COLUMN stroke_count INTEGER
        """))
        print("  ✅ 添加 stroke_count 字段")
        
        # 添加组词示例
        session.execute(text("""
            ALTER TABLE vocabulary ADD COLUMN word_examples JSON
        """))
        print("  ✅ 添加 word_examples 字段")
        
        # 添加 AI 特征
        session.execute(text("""
            ALTER TABLE vocabulary ADD COLUMN ai_features JSON
        """))
        print("  ✅ 添加 ai_features 字段")
        
        session.commit()
        
        # ========== 5. poetry_memory 表优化 ==========
        print("\n📝 优化 poetry_memory 表...")
        
        # 添加古诗元数据
        session.execute(text("""
            ALTER TABLE poetry_memory ADD COLUMN poetry_metadata JSON
        """))
        print("  ✅ 添加 poetry_metadata 字段")
        
        # 添加复习历史
        session.execute(text("""
            ALTER TABLE poetry_memory ADD COLUMN review_history JSON
        """))
        print("  ✅ 添加 review_history 字段")
        
        session.commit()
        
        # ========== 6. growth_tree 表优化 ==========
        print("\n📝 优化 growth_tree 表...")
        
        # 添加成就记录
        session.execute(text("""
            ALTER TABLE growth_tree ADD COLUMN achievements JSON
        """))
        print("  ✅ 添加 achievements 字段")
        
        # 添加连续学习天数
        session.execute(text("""
            ALTER TABLE growth_tree ADD COLUMN streak_days INTEGER DEFAULT 0
        """))
        print("  ✅ 添加 streak_days 字段")
        
        # 添加动力分析
        session.execute(text("""
            ALTER TABLE growth_tree ADD COLUMN motivation_analysis JSON
        """))
        print("  ✅ 添加 motivation_analysis 字段")
        
        session.commit()
        
        # ========== 7. knowledge_points 表优化 ==========
        print("\n📝 优化 knowledge_points 表...")
        
        # 添加前置知识点
        session.execute(text("""
            ALTER TABLE knowledge_points ADD COLUMN prerequisites JSON
        """))
        print("  ✅ 添加 prerequisites 字段")
        
        # 添加后续知识点
        session.execute(text("""
            ALTER TABLE knowledge_points ADD COLUMN next_steps JSON
        """))
        print("  ✅ 添加 next_steps 字段")
        
        # 添加知识图谱向量
        session.execute(text("""
            ALTER TABLE knowledge_points ADD COLUMN knowledge_vector JSON
        """))
        print("  ✅ 添加 knowledge_vector 字段")
        
        # 添加常见错误模式
        session.execute(text("""
            ALTER TABLE knowledge_points ADD COLUMN common_error_patterns JSON
        """))
        print("  ✅ 添加 common_error_patterns 字段")
        
        session.commit()
        
        # ========== 8. students 表优化 ==========
        print("\n📝 优化 students 表...")
        
        # 添加学习风格
        session.execute(text("""
            ALTER TABLE students ADD COLUMN learning_style VARCHAR(20)
        """))
        print("  ✅ 添加 learning_style 字段")
        
        # 添加学习目标
        session.execute(text("""
            ALTER TABLE students ADD COLUMN learning_goals JSON
        """))
        print("  ✅ 添加 learning_goals 字段")
        
        session.commit()
        
        # ========== 9. 创建索引 ==========
        print("\n🔧 创建 AI 推荐查询索引...")
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_question_subject_grade ON question_bank(subject, grade)",
            "CREATE INDEX IF NOT EXISTS idx_question_knowledge ON question_bank(knowledge_point)",
            "CREATE INDEX IF NOT EXISTS idx_question_difficulty ON question_bank(difficulty)",
            "CREATE INDEX IF NOT EXISTS idx_question_error_rate ON question_bank(error_rate)",
            "CREATE INDEX IF NOT EXISTS idx_wrong_student ON wrong_questions(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_wrong_mastered ON wrong_questions(mastered)",
            "CREATE INDEX IF NOT EXISTS idx_wrong_reason ON wrong_questions(wrong_reason)",
            "CREATE INDEX IF NOT EXISTS idx_learning_student_date ON learning_records(student_id, date)",
            "CREATE INDEX IF NOT EXISTS idx_poetry_next_review ON poetry_memory(next_review_at)",
            "CREATE INDEX IF NOT EXISTS idx_vocabulary_status ON vocabulary(status)",
        ]
        
        for idx_sql in indexes:
            session.execute(text(idx_sql))
            print(f"  ✅ {idx_sql.split('ON')[1].strip() if 'ON' in idx_sql else ''}")
        
        session.commit()
        
        print("\n" + "="*50)
        print("✅ AI 推荐优化迁移完成！")
        print("="*50)
        
        print("\n新增字段统计：")
        print("  - question_bank: +2 字段（ai_features, knowledge_vector）")
        print("  - wrong_questions: +4 字段（error_analysis, mastery_score, priority, strategy）")
        print("  - learning_records: +4 字段（time, attempts, ai_score, behavior）")
        print("  - vocabulary: +5 字段（frequency, radical, stroke, examples, ai_features）")
        print("  - poetry_memory: +2 字段（metadata, review_history）")
        print("  - growth_tree: +3 字段（achievements, streak, motivation）")
        print("  - knowledge_points: +4 字段（prerequisites, next_steps, vector, patterns）")
        print("  - students: +2 字段（style, goals）")
        print("  - 索引：+10 个查询索引")
        
        print("\n🎯 现在数据库已优化，支持：")
        print("  ✅ 学生画像构建")
        print("  ✅ 题目特征提取")
        print("  ✅ 薄弱点分析")
        print("  ✅ 举一反三推荐")
        print("  ✅ 记忆曲线追踪")
        print("  ✅ 学习行为分析")
        print("  ✅ 个性化推荐算法")
        
    except Exception as e:
        session.rollback()
        print(f"\n❌ 迁移失败：{e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    migrate()
