# requirementsL.txt 保护机制

## 保护说明

本系统提供保护机制，确保 `requirementsL.txt` 始终保持精简版本，防止被意外修改或覆盖。

### 保护文件

- **requirementsL.txt**: 精简的核心依赖列表（38个依赖包）
- **保护状态**: 受保护，不会被修改机制覆盖

### 不保护的文件

- **requirements.txt**: 完整依赖列表（150+依赖包）
- **状态**: 可自由修改，不受保护

## 解决方案

### 1. 快速检查和恢复（推荐）

每次操作前后运行：
```bash
./check_requirements.sh
```

这个脚本会：
- 检查 requirementsL.txt 行数是否为61行
- 如果不是，自动从 git 恢复
- 恢复后设置为只读

### 2. 守护进程监控

启动守护进程，持续监控文件：
```bash
./watchdog_requirements.sh
```

守护进程会：
- 每5秒检查一次 requirementsL.txt
- 如果发现文件被修改，立即恢复
- 按Ctrl+C停止守护进程

### 3. 定时任务（可选）

添加 cron 任务，定期检查：
```bash
# 编辑 crontab
crontab -e

# 添加以下行（每5分钟检查一次）
*/5 * * * * cd /path/to/project && ./check_requirements.sh >> /tmp/requirementsL_watch.log 2>&1
```

## 精简后的依赖

- **原始版本** (requirements.txt): 150+ 依赖包
- **精简版本** (requirementsL.txt): 38 个核心依赖包（61行，含注释）
- **减少比例**: 约 75%

## 关键命令

### 检查状态
```bash
./check_requirements.sh
```

### 手动恢复
```bash
git restore requirementsL.txt
chmod 444 requirementsL.txt
```

### 查看当前行数
```bash
wc -l requirementsL.txt
```

### 查看文件权限
```bash
ls -l requirementsL.txt
```

## 部署建议

1. **首次部署**: 运行 `./check_requirements.sh` 确保文件正确
2. **持续运行**: 启动 `./watchdog_requirements.sh` 守护进程
3. **定期检查**: 添加 cron 任务定期检查
4. **版本控制**: 确保提交前运行 `./check_requirements.sh`

## 注意事项

- ⚠️ requirementsL.txt 会被设置为只读（444），如需修改请先改为可写
- ⚠️ 守护进程需要保持运行，否则文件仍可能被修改
- ⚠️ 定时任务需要确保脚本路径正确
- ✅ Git 仓库中已保存精简版本，可以随时恢复
- ⚠️ requirements.txt 不受保护，可以自由修改

## 紧急恢复

如果 requirementsL.txt 被覆盖，立即执行：
```bash
git restore requirementsL.txt
./check_requirements.sh
```

## 监控日志

如果使用 cron 任务，可以查看日志：
```bash
tail -f /tmp/requirementsL_watch.log
```

## 新增依赖

如果需要新增依赖，请参考 `REQUIREMENTS_FILES.md` 文档。

---

**创建时间**: $(date)
**精简版本**: 61行，38个依赖包
**保护文件**: requirementsL.txt
