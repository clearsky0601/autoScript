#!/bin/bash

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    SUDO='sudo'
    echo "请提供管理员密码以继续安装:"
else
    SUDO=''
fi

# 更新软件源
$SUDO apt update

# 安装zsh
$SUDO apt install -y zsh

# 将zsh设置为默认的shell
chsh -s $(which zsh)

# 下载安装oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 安装自动补全插件和代码高亮插件
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# 修改zshrc
sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="af-magic"/' ~/.zshrc
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/' ~/.zshrc

# 加载新的zsh配置
source ~/.zshrc