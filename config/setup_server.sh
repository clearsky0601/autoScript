#!/bin/bash

# 函数：显示进度
show_progress() {
    echo "===> $1"
}

# 函数：错误处理
handle_error() {
    echo "错误: $1" >&2
    exit 1
}

# 更新软件源
show_progress "更新软件源"
sudo apt update || handle_error "无法更新软件源"

# 安装工具
show_progress "安装 tmux、zsh 和 git"
sudo apt install -y tmux zsh git || handle_error "无法安装 tmux、zsh 和 git"

# 下载并安装 Oh My Zsh
show_progress "安装 Oh My Zsh"
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended || handle_error "无法安装 Oh My Zsh"

# 安装 Zsh 插件
show_progress "安装 Zsh 插件"
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions || handle_error "无法安装 zsh-autosuggestions 插件"
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting || handle_error "无法安装 zsh-syntax-highlighting 插件"

# 配置 .zshrc
show_progress "配置 .zshrc"
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/' ~/.zshrc || handle_error "无法修改 .zshrc"

# 配置 Git
show_progress "配置 Git"
git config --global user.name "clearsky0601" || handle_error "无法设置 Git 用户名"
git config --global user.email "xinyuscl@163.com" || handle_error "无法设置 Git 邮箱"

# 应用新的 Zsh 配置
show_progress "应用新的 Zsh 配置"
source ~/.zshrc || handle_error "无法应用新的 Zsh 配置"

show_progress "配置完成!"
