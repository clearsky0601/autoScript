#!/bin/bash

set -e

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    SUDO='sudo'
    echo "Please provide the administrator password to continue installation:"
else
    SUDO=''
fi

# 在家目录下创建workSpace目录
mkdir -p "$HOME/workSpace"
echo "Created workSpace directory in home folder"

# 更新软件源
$SUDO apt update
echo "Updated package lists"

# 必装软件列表
packages=(vim nnn python3 wget curl tree)

# 检查并安装必装软件
echo "Checking and installing required packages..."
for package in "${packages[@]}"; do
    if ! command -v "$package" &> /dev/null; then
        echo "Installing $package..."
        $SUDO apt install -y "$package"
    else
        echo "$package is already installed, skipping"
    fi
done

# 配置全局git
git config --global user.name "clearsky0601"
git config --global user.email "xinyuscl@163.com"
echo "Configured global Git settings"

# 配置vimrc
if [ -f "./vimrc" ]; then
    cp "./vimrc" "$HOME/.vimrc"
    echo "Copied vimrc configuration file to home directory"
else
    echo "Warning: vimrc file not found in the repository, please check the repository contents"
fi

echo "Initialization configuration completed successfully"
