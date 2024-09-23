#!/bin/bash

# 获取当前时间作为提交信息
current_time=$(date "+%Y-%m-%d %H:%M:%S")

# 添加所有变动到暂存区
git add .

# 提交变动，使用当前时间作为提交信息
git commit -m "$current_time"

# 推送到远程仓库
git push

echo "Changes committed and pushed successfully at $current_time"
