#!/bin/bash

# 确保当前的目录为$HOME/workSpace/autoScript
cd $HOME/workSpace/autoScript || exit

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    SUDO='sudo'
    echo "Please provide the administrator password to continue installation:"
else
    SUDO=''
fi
# 将自定义的命令封装成一个数组
scripts=(gitpush.sh recordCommand.py)

# 将自定义的命令拷贝到 /usr/local/bin/ 目录下并添加可执行权限
echo "Copying custom scripts to /usr/local/bin/ and adding executable permissions..."
for script in "${scripts[@]}"; do
    $SUDO cp "$script" /usr/local/bin/
    $SUDO chmod +x "/usr/local/bin/$script"
done

# 添加自定义别名到.zshrc文件中
echo "Adding custom aliases to .zshrc file..."
echo "alias lgc='/usr/local/bin/recordCommand.py'" >> $HOME/.zshrc
echo "alias gitpush='/usr/local/bin/gitpush.sh'" >> $HOME/.zshrc

# 不要尝试在bash中重新加载.zshrc
echo "Custom aliases have been added to .zshrc"
echo "Please run 'source ~/.zshrc' in your zsh shell to apply changes"

echo "Custom command configuration completed successfully!"