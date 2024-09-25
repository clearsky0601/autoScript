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


# 将自定义的命令拷贝到 /usr/local/bin/ 目录下


将autoScript目录下的gitpush.sh,recordCommand.py,[待填充,以后还有,考虑脚本的可拓展性]添加可执行权限并将其移动到/usr/local/bin/目录下(该目录会请求权限)



# 自定义别名添加到.zshrc文件中
alias lgc='/path/to/recordCommand.py'
alias gitpush='/path/to/gitpush.sh'

这里gitpush.sh recordCommand.py 需要替换成实际的路径,也就是/usr/local/bin/目录下的路径

source .zshrc