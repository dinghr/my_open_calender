#!/bin/bash
# AI 伴学小程序 - 数据库备份脚本
# 功能：每日备份 SQLite 数据库到本地和阿里云 OSS

set -e

# ==================== 配置 ====================

# 项目根目录
PROJECT_DIR="/home/ecs-user/my_open_calender"

# 数据库文件路径
DB_FILE="$PROJECT_DIR/data/app.db"

# 备份目录
BACKUP_DIR="$PROJECT_DIR/backup"

# 日志文件
LOG_FILE="$PROJECT_DIR/logs/backup.log"

# 阿里云 OSS 配置（可选）
OSS_BUCKET="your-bucket-name"
OSS_PATH="backups/ai-tutor"
ENABLE_OSS=false  # 设为 true 启用 OSS 备份

# 保留天数
RETENTION_DAYS=30

# ==================== 函数 ====================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ==================== 主流程 ====================

log "🚀 开始备份数据库..."

# 创建备份目录
mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

# 检查数据库文件是否存在
if [ ! -f "$DB_FILE" ]; then
    log "❌ 数据库文件不存在：$DB_FILE"
    exit 1
fi

# 生成备份文件名
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/app.db.$TIMESTAMP"

# 复制数据库文件
log "📋 复制数据库文件..."
cp "$DB_FILE" "$BACKUP_FILE"

# 压缩备份
log "📦 压缩备份文件..."
cd "$BACKUP_DIR"
tar -czf "$BACKUP_FILE.tar.gz" "app.db.$TIMESTAMP"
rm "$BACKUP_FILE"

log "✅ 本地备份完成：$BACKUP_FILE.tar.gz"

# 上传到阿里云 OSS（如果启用）
if [ "$ENABLE_OSS" = true ]; then
    log "☁️ 上传到阿里云 OSS..."
    
    # 检查 ossutil 是否安装
    if ! command -v ossutil &> /dev/null; then
        log "⚠️  ossutil 未安装，跳过 OSS 上传"
    else
        ossutil cp "$BACKUP_FILE.tar.gz" "oss://$OSS_BUCKET/$OSS_PATH/"
        log "✅ OSS 上传完成"
    fi
fi

# 清理旧备份
log "🧹 清理 $RETENTION_DAYS 天前的旧备份..."
find "$BACKUP_DIR" -name "app.db.*.tar.gz" -mtime +$RETENTION_DAYS -delete

# 显示备份统计
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/app.db.*.tar.gz 2>/dev/null | wc -l)
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

log "📊 备份统计："
log "   - 备份文件数量：$BACKUP_COUNT"
log "   - 备份目录大小：$BACKUP_SIZE"
log "   - 最新备份：$BACKUP_FILE.tar.gz"

log "🎉 备份完成！"
