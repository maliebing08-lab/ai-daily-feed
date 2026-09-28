# ai-daily-feed

gokmfun.com「AI 应用日报」的数据仓库。

- 每天北京时间早上，一个 Claude 定时任务按 [WRITING_GUIDE.md](WRITING_GUIDE.md) 搜集全球 AI 应用新闻，
  写成 `posts/YYYY-MM-DD.json` 并推送到这里。
- 服务器 `/opt/ai-daily` 每小时检查一次（08:00–11:59），读取当天的 JSON，生成封面并发布到 WordPress。
- 校验：`python3 tools/validate.py posts/YYYY-MM-DD.json`
