def hello_world():
    return "Hello, Scheduled Task!"

# Cloudflare Workers 需要一个特定的入口函数，名字必须是 scheduled
# 这个函数会在 wrangler.toml 中配置的 cron 时间被自动调用
# event 参数包含了触发事件的信息，比如触发时间等
async def scheduled(event, env, ctx):
    # 处理定时任务的逻辑
    result = hello_world()
    print(f"Task executed at: {event.time}, Result: {result}")
    return result
