# Cloudflare Worker 定时任务示例

这是一个简单的 Cloudflare Worker 定时任务示例，每10分钟执行一次 Hello World 任务。

## 部署方法

### 方法一：通过 GitHub 直接部署

1. Fork 这个仓库到你的 GitHub 账户
2. 登录到 [Cloudflare Dashboard](https://dash.cloudflare.com)
3. 进入 Workers & Pages
4. 点击 "Create application"
5. 选择 "Connect to Git"
6. 选择你 fork 的仓库
7. 选择 "Workers" 类型
8. 在部署设置中确认配置无误后点击 "Deploy"

Cloudflare 会自动读取 `wrangler.toml` 中的配置，包括定时任务设置（每10分钟执行一次）。

### 方法二：通过 Wrangler CLI 部署

1. 安装 Wrangler CLI：
```bash
npm install -g wrangler
```

2. 登录到你的 Cloudflare 账户：
```bash
wrangler login
```

3. 部署项目：
```bash
wrangler deploy
```

## 配置说明

- `worker.py`: 包含要执行的任务代码
- `wrangler.toml`: Cloudflare Workers 配置文件，设置了定时执行规则
- `requirements.txt`: 项目依赖文件

你可以在 `wrangler.toml` 文件中修改 cron 表达式来调整任务执行频率。
