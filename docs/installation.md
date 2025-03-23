# 安装指南

## 环境要求

### 本地开发环境
#### 后端环境
- Python 3.8+
- PostgreSQL 数据库
- Redis

#### 前端环境
- Node.js 16+
- npm 或 yarn

### Docker环境
- Docker 20.10+
- Docker Compose v2.0+

## 安装步骤

### 方式一：Docker部署（推荐）

1. 克隆项目
```bash
git clone <repository_url>
cd AlertAgent
```

2. 使用Docker Compose启动所有服务
```bash
docker compose up -d
```

这将自动完成以下操作：
- 启动PostgreSQL数据库
- 启动Redis服务
- 构建并启动后端服务
- 构建并启动前端服务

3. 访问应用
- 前端界面：http://localhost:5173
- 后端API：http://localhost:8000

### 方式二：本地开发

#### 1. 克隆项目
```bash
git clone <repository_url>
cd AlertAgent
```

#### 2. 后端安装

1. 进入后端目录
```bash
cd backend
```

2. 创建并激活虚拟环境（可选）
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
创建 `.env` 文件并配置以下变量：
```
DATABASE_URL=postgresql://user:password@localhost:5432/alert_agent
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
```

5. 初始化数据库
```bash
python -m app.db.init_db
```

#### 3. 前端安装

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
# 或
yarn
```

3. 配置环境变量
创建 `.env` 文件并配置：
```
VITE_API_BASE_URL=http://localhost:8000
```

### 本地开发模式启动服务

#### 启动后端
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 启动前端
```bash
cd frontend
npm run dev
# 或
yarn dev
```

访问 http://localhost:5173 即可看到应用界面。

## 常见问题

### Docker相关问题

#### 服务启动失败
- 检查Docker和Docker Compose是否正确安装
- 确保没有端口冲突（5173、8000、5432、6379）
- 查看容器日志：`docker compose logs [服务名]`

#### 数据持久化
- 数据库和Redis数据存储在Docker卷中
- 可以使用`docker compose down -v`清除所有数据

### 本地开发问题

#### 数据库连接失败
- 确保 PostgreSQL 服务已启动
- 检查数据库连接字符串是否正确
- 验证数据库用户权限

#### Redis 连接失败
- 确保 Redis 服务已启动
- 检查 Redis 连接字符串

#### 前端API请求失败
- 确保后端服务正在运行
- 检查 VITE_API_BASE_URL 配置是否正确
- 检查浏览器控制台是否有跨域错误