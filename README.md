# 新闻推送服务

这是一个基于 Cloudflare Workers 的定时新闻推送服务，每10分钟检查一次所有新闻源的更新。

## 功能说明

- 自动从多个新闻源获取最新新闻
- 将新闻存储到数据库中
- 创建推送记录用于后续处理
- 支持多数据源配置

## 项目结构

```
├── api/
│   └── newsApi.py          # 新闻API调用接口
├── db/
│   ├── dbManager.py        # 数据库管理基类
│   ├── dbNewsInfos.py      # 新闻信息表操作类
│   ├── dbPushInfoLatest.py # 推送信息表操作类
│   └── tableStruct/        # 数据库表结构
├── worker.py               # 主要任务代码
├── test_worker.py         # 测试文件
├── wrangler.toml          # Cloudflare配置
├── requirements.txt       # 项目依赖
└── news-source.json      # 新闻源配置
```

## 配置说明

1. 数据库配置
在 `db/.env` 文件中配置数据库连接信息：
```env
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
DB_CHARSET=utf8mb4
```

2. 新闻源配置
在 `news-source.json` 中配置新闻源信息：
```json
[
  {
    "id": "source_id",
    "name": "源名称"
  }
]
```

## 部署方法

### 方法一：通过 GitHub 直接部署

1. Fork 这个仓库到你的 GitHub 账户
2. 登录到 [Cloudflare Dashboard](https://dash.cloudflare.com)
3. 进入 Workers & Pages
4. 点击 "Create application"
5. 选择 "Connect to Git"
6. 选择你 fork 的仓库
7. 选择 "Workers" 类型
8. 设置环境变量（数据库配置等）
9. 在部署设置中确认配置无误后点击 "Deploy"

### 方法二：通过 Wrangler CLI 部署

1. 安装 Wrangler CLI：
```bash
npm install -g wrangler
```

2. 登录到你的 Cloudflare 账户：
```bash
wrangler login
```

3. 配置环境变量：
```bash
wrangler secret put DB_HOST
wrangler secret put DB_USER
wrangler secret put DB_PASSWORD
wrangler secret put DB_NAME
```

4. 部署项目：
```bash
wrangler deploy
```

## 本地测试

运行测试脚本：
```bash
python test_worker.py
```

## 定时设置

当前配置为每10分钟执行一次（在 `wrangler.toml` 中配置）。你可以修改 cron 表达式来调整执行频率：
```toml
[triggers]
crons = ["*/10 * * * *"]  # 每10分钟执行一次
