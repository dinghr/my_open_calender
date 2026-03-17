#!/bin/bash
# AI 伴学小程序 - Claude 开发状态监控脚本
# 功能：每 5 分钟检查后台开发进程状态

set -e

# ==================== 配置 ====================

# 日志文件
LOG_FILE="/home/ecs-user/my_open_calender/logs/claude-monitor.log"

# 通知标记文件
NOTIFY_FILE="/home/ecs-user/my_open_calender/logs/claude-notify.flag"

# 检查的进程关键词
PROCESS_KEYWORDS=("claude" "codex" "coding" "backend" "dev")

# ==================== 函数 ====================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

send_notification() {
    local message="$1"
    local priority="$2"  # normal, urgent
    
    # 创建通知标记文件（主程序可以检查）
    echo "$message" > "$NOTIFY_FILE"
    echo "[$priority] $message" >> "$LOG_FILE"
    
    # 如果是紧急通知，创建醒目标记
    if [ "$priority" = "urgent" ]; then
        touch "/home/ecs-user/my_open_calender/logs/URGENT_NOTIFY.flag"
    fi
}

check_processes() {
    local found_count=0
    
    log "🔍 检查后台开发进程..."
    
    # 检查是否有相关进程在运行
    for keyword in "${PROCESS_KEYWORDS[@]}"; do
        if pgrep -f "$keyword" > /dev/null 2>&1; then
            log "✅ 发现进程：$keyword"
            found_count=$((found_count + 1))
        fi
    done
    
    # 检查 tmux 会话
    if command -v tmux &> /dev/null; then
        tmux_sessions=$(tmux list-sessions 2>/dev/null | grep -E "(claude|code|dev)" | wc -l)
        if [ "$tmux_sessions" -gt 0 ]; then
            log "✅ 发现 tmux 会话：$tmux_sessions 个"
            found_count=$((found_count + tmux_sessions))
        fi
    fi
    
    # 检查 screen 会话
    if command -v screen &> /dev/null; then
        screen_sessions=$(screen -ls 2>/dev/null | grep -E "(claude|code|dev)" | wc -l)
        if [ "$screen_sessions" -gt 0 ]; then
            log "✅ 发现 screen 会话：$screen_sessions 个"
            found_count=$((found_count + screen_sessions))
        fi
    fi
    
    # 检查最近的 CPU 使用（可能有活跃进程）
    recent_cpu=$(top -bn1 | grep -E "(python|node|claude)" | head -5 | wc -l)
    if [ "$recent_cpu" -gt 0 ]; then
        log "✅ 发现活跃进程：$recent_cpu 个"
        found_count=$((found_count + recent_cpu))
    fi
    
    return $found_count
}

check_disk_activity() {
    # 检查项目目录是否有文件变化（过去 10 分钟内）
    recent_files=$(find /home/ecs-user/my_open_calender -type f -mmin -10 2>/dev/null | wc -l)
    if [ "$recent_files" -gt 0 ]; then
        log "📝 发现文件活动：$recent_files 个文件被修改"
        return 0
    fi
    return 1
}

# ==================== 主流程 ====================

log "🚀 Claude 开发状态监控开始"

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

# 清除旧的通知标记
rm -f "$NOTIFY_FILE"
rm -f "/home/ecs-user/my_open_calender/logs/URGENT_NOTIFY.flag"

# 检查进程
set +e
check_processes
process_result=$?
set -e

if [ "$process_result" -gt 0 ]; then
    log "✅ 开发进程运行中（发现 $process_result 个相关进程）"
    
    # 检查是否有文件活动
    if check_disk_activity; then
        log "✅ 开发正常进行中"
    else
        log "⚠️  进程存在但无文件活动（可能空闲或等待输入）"
        send_notification "⚠️ Claude 开发进程存在但似乎空闲，可能需要关注" "normal"
    fi
else
    log "❌ 未发现开发进程"
    send_notification "❌ Claude 开发进程已停止，需要重新启动！" "urgent"
fi

log "📊 监控检查完成"
