# 🚀 快速部署指南

**目标：** 15 分钟内部署生产环境和测试环境

---

## 📋 前置条件

### 1. 域名准备

确保以下域名已解析到服务器 IP (`172.27.151.210`)：

```
api.ai-study.com          →  172.27.151.210  (生产环境)
test-api.ai-study.com     →  172.27.151.210  (测试环境)
```

**验证：**
```bash
ping api.ai-study.com
ping test-api.ai-study.com
```

### 2. 服务器要求

- ✅ Ubuntu 20.04+ / Debian 10+
- ✅ 至少 2GB RAM
- ✅ 至少 20GB 磁盘空间
- ✅ root 或 sudo 权限
- ✅ Python 3.10+ (已安装)
- ✅ Node.js 18+ (已安装)

---

## 🔧 快速部署（一键脚本）

### Step 1: 运行部署脚本

```bash
cd ~/my_open_calender
sudo bash deploy/deploy.sh
```

脚本会自动：
- ✅ 安装 Nginx、Certbot、UFW
- ✅ 配置 Nginx 反向代理
- ✅ 配置 Systemd 服务
- ✅ 配置防火墙规则
- ✅ 申请 SSL 证书
- ✅ 启动所有服务

### Step 2: 创建 Secrets 文件

部署脚本会提示你创建 secrets 文件：

```bash
# 生产环境
sudo nano /etc/ai-study/prod.secrets
```

复制 `deploy/prod.secrets.example` 的内容，填入真实值：

```bash
# AI API 密钥
AI_API_KEY=sk-your-actual-api-key

# 管理员密码
ADMIN_USERNAME=admin
ADMIN_PASSWORD=YourSecurePassword123!

# JWT 密钥（随机生成）
JWT_SECRET=$(openssl rand -hex 32)
```

保存后设置权限：
```bash
sudo chmod 600 /etc/ai-study/prod.secrets
```

### Step 3: 初始化生产数据库

```bash
cd ~/my_open_calender
python3 scripts/init_prod_db.py
```

### Step 4: 启动服务

```bash
# 启动生产环境
sudo systemctl start ai-study-prod
sudo systemctl enable ai-study-prod

# 启动测试环境
sudo systemctl start ai-study-test
sudo systemctl enable ai-study-test

# 检查状态
sudo systemctl status ai-study-prod
sudo systemctl status ai-study-test
```

---

## ✅ 验证部署

### 1. 健康检查

```bash
# 生产环境
curl https://api.ai-study.com/health

# 应该返回：
# {"status":"ok"}
```

```bash
# 测试环境
curl https://test-api.ai-study.com:8443/health
```

### 2. 检查 API 文档

访问：
- 生产：https://api.ai-study.com/docs (需要密码)
- 测试：https://test-api.ai-study.com:8443/docs (公开)

### 3. 检查日志

```bash
# 应用日志
sudo journalctl -u ai-study-prod -f

# Nginx 日志
sudo tail -f /var/log/nginx/ai-study-prod-access.log
```

---

## 🔐 安全加固

### 1. 检查防火墙

```bash
sudo ufw status verbose

# 应该看到：
# 22/tcp (SSH)          ALLOW
# 80/tcp (HTTP)         ALLOW
# 443/tcp (HTTPS)       ALLOW
# 8443/tcp (HTTPS Test) ALLOW
```

### 2. 检查 SSL 证书

```bash
sudo certbot certificates
```

### 3. 自动续期 SSL

Certbot 会自动续期，验证自动续期：

```bash
sudo certbot renew --dry-run
```

---

## 🛠️ 常用命令

### 服务管理

```bash
# 重启服务
sudo systemctl restart ai-study-prod
sudo systemctl restart ai-study-test

# 停止服务
sudo systemctl stop ai-study-prod

# 查看日志
sudo journalctl -u ai-study-prod -n 50
```

### Nginx 管理

```bash
# 重新加载配置
sudo nginx -t && sudo systemctl reload nginx

# 查看日志
sudo tail -f /var/log/nginx/ai-study-prod-error.log
```

### 数据库备份

```bash
# 备份生产数据库
cp ~/my_open_calender/data/prod.db ~/my_open_calender/backups/prod.db.$(date +%Y%m%d)

# 备份到远程服务器
scp ~/my_open_calender/data/prod.db backup-server:/backups/prod.db.$(date +%Y%m%d)
```

---

## 🚨 故障排查

### 问题 1: 服务无法启动

```bash
# 查看详细错误
sudo journalctl -u ai-study-prod -n 100 --no-pager

# 检查端口占用
sudo lsof -i :8001
sudo lsof -i :8002
```

### 问题 2: 502 Bad Gateway

```bash
# 检查后端服务
sudo systemctl status ai-study-prod

# 检查 Nginx 错误日志
sudo tail -f /var/log/nginx/ai-study-prod-error.log

# 测试后端直接访问
curl http://127.0.0.1:8001/health
```

### 问题 3: SSL 证书问题

```bash
# 检查证书状态
sudo certbot certificates

# 手动续期
sudo certbot renew --force-renewal
```

---

## 📊 监控建议

### 1. 系统监控

安装监控工具：

```bash
# 安装 htop
sudo apt install -y htop

# 安装 netdata（实时监控）
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

### 2. 应用监控

在 secrets 文件中配置 Sentry：

```bash
SENTRY_DSN=https://your-dsn@sentry.io/123456
```

### 3. 日志聚合

```bash
# 安装 lnav（日志查看器）
sudo apt install -y lnav

# 查看多个日志文件
lnav /var/log/nginx/*.log
```

---

## 📝 部署后检查清单

- [ ] 生产环境健康检查通过
- [ ] 测试环境健康检查通过
- [ ] SSL 证书有效
- [ ] 防火墙已启用
- [ ] 服务已设置开机自启
- [ ] 数据库已备份
- [ ] 监控已配置
- [ ] 文档已更新

---

## 🎯 下一步

1. **配置前端部署** - 将前端部署到 CDN 或静态托管
2. **配置 CI/CD** - 使用 GitHub Actions 自动部署
3. **配置监控告警** - 设置服务异常告警
4. **性能优化** - 配置 Redis 缓存、数据库优化

---

*部署愉快！有问题随时查看日志。*
