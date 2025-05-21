### 启动命令
```
sh run.sh
```

### 停止
```
ps aux | grep uv
lsof -i :8000
kill -9 2493

pkill -f "uv run cg-api" && sh run.sh
```