#!/bin/bash
# AI 伴学小程序 - 生产环境部署脚本
# 使用方法：sudo bash deploy/deploy.sh

set -e

echo "🦞 AI 伴学小程序 - 生产环境部署"
echo "================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}请使用 sudo 运行此脚本${NC}"
    exit 1
fi

PROJECT_DIR="/home/ecs-user/my_open_calender"
SECRETS_DIR="/etc/ai-study"

# ==================== 1. 安装系统依赖 ====================
echo -e "\n${YELLOW}[1/7] 安装系统依赖...${NC}"
apt update
apt install -y nginx certbot python3-certbot-nginx ufw

# ==================== 2. 创建 Secrets 目录 ====================
echo -e "\n${YELLOW}[2/7] 创建配置目录...${NC}"
mkdir -p $SECRETS_DIR
chmod 700 $SECRETS_DIR

# 创建 .htpasswd 文件（用于 API 文档认证）
if [ ! -f "$SECRETS_DIR/.htpasswd" ]; then
    echo -e "${YELLOW}设置 API 文档访问密码:${NC}"
    htpasswd -c $SECRETS_DIR/.htpasswd admin
fi

# ==================== 3. 配置 Nginx ====================
echo -e "\n${YELLOW}[3/7] 配置 Nginx...${NC}"

# 复制 Nginx 配置
cp $PROJECT_DIR/deploy/nginx-prod.conf /etc/nginx/sites-available/ai-study-prod
cp $PROJECT_DIR/deploy/nginx-test.conf /etc/nginx/sites-available/ai-study-test

# 启用站点
ln -sf /etc/nginx/sites-available/ai-study-prod /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/ai-study-test /etc/nginx/sites-enabled/

# 移除默认站点
rm -f /etc/nginx/sites-enabled/default

# 测试 Nginx 配置
nginx -t

# ==================== 4. 配置 Systemd 服务 ====================
echo -e "\n${YELLOW}[4/7] 配置 Systemd 服务...${NC}"

cp $PROJECT_DIR/deploy/ai-study-prod.service /etc/systemd/system/
cp $PROJECT_DIR/deploy/ai-study-test.service /etc/systemd/system/

# 重新加载 systemd
systemctl daemon-reload

# ==================== 5. 配置防火墙 ====================
echo -e "\n${YELLOW}[5/7] 配置防火墙...${NC}"

ufw allow 22/tcp comment "SSH"
ufw allow 80/tcp comment "HTTP"
ufw allow 443/tcp comment "HTTPS (Production)"
ufw allow 8443/tcp comment "HTTPS (Test)"

# 启用 UFW（如果未启用）
ufw --force enable || true

echo -e "${GREEN}✓ 防火墙规则已配置${NC}"

# ==================== 6. 申请 SSL 证书 ====================
echo -e "\n${YELLOW}[6/7] 申请 SSL 证书...${NC}"

# 创建 certbot webroot 目录
mkdir -p /var/www/certbot

echo -e "${YELLOW}请输入生产环境域名 (例如：api.ai-study.com):${NC}"
read PROD_DOMAIN

echo -e "${YELLOW}请输入测试环境域名 (例如：test-api.ai-study.com):${NC}"
read TEST_DOMAIN

# 申请生产环境证书
echo -e "${YELLOW}申请生产环境 SSL 证书...${NC}"
certbot certonly --webroot -w /var/www/certbot -d $PROD_DOMAIN --agree-tos --non-interactive || {
    echo -e "${RED}生产环境证书申请失败，请检查域名解析${NC}"
}

# 申请测试环境证书
echo -e "${YELLOW}申请测试环境 SSL 证书...${NC}"
certbot certonly --webroot -w /var/www/certbot -d $TEST_DOMAIN --agree-tos --non-interactive || {
    echo -e "${YELLOW}测试环境证书申请失败，可以稍后手动申请${NC}"
}

# ==================== 7. 启动服务 ====================
echo -e "\n${YELLOW}[7/7] 启动服务...${NC}"

# 启动 Nginx
systemctl enable nginx
systemctl restart nginx

# 启动应用服务（如果 secrets 文件已存在）
if [ -f "$SECRETS_DIR/prod.secrets" ]; then
    systemctl enable ai-study-prod
    systemctl start ai-study-prod
    echo -e "${GREEN}✓ 生产服务已启动${NC}"
else
    echo -e "${YELLOW}⚠️  Secrets 文件不存在，跳过服务启动${NC}"
    echo -e "${YELLOW}请创建 $SECRETS_DIR/prod.secrets 后手动启动:${NC}"
    echo -e "  systemctl start ai-study-prod"
fi

if [ -f "$SECRETS_DIR/test.secrets" ]; then
    systemctl enable ai-study-test
    systemctl start ai-study-test
    echo -e "${GREEN}✓ 测试服务已启动${NC}"
else
    echo -e "${YELLOW}⚠️  Secrets 文件不存在，跳过服务启动${NC}"
fi

# ==================== 完成 ====================
echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}✓ 部署完成！${NC}"
echo -e "${GREEN}================================${NC}"

echo -e "\n${YELLOW}下一步操作:${NC}"
echo "1. 创建 secrets 文件："
echo "   sudo nano $SECRETS_DIR/prod.secrets"
echo "   sudo nano $SECRETS_DIR/test.secrets"
echo ""
echo "2. 初始化生产数据库："
echo "   cd $PROJECT_DIR"
echo "   python3 scripts/init_prod_db.py"
echo ""
echo "3. 启动服务（如果未自动启动）："
echo "   sudo systemctl start ai-study-prod"
echo "   sudo systemctl start ai-study-test"
echo ""
echo "4. 检查服务状态："
echo "   sudo systemctl status ai-study-prod"
echo "   sudo systemctl status ai-study-test"
echo "   sudo systemctl status nginx"
echo ""
echo "5. 测试健康检查："
echo "   curl https://$PROD_DOMAIN/health"
echo "   curl https://$TEST_DOMAIN:8443/health"
echo ""
