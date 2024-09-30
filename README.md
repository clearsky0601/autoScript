
### 文件目录
.
```
├── README.md
├── config_diyCommand.sh # 配置自定义命令
├── gitpush.sh # 用于自动推送代码到远程仓库
├── init.sh # 用于初始化服务器
├── recordCommand.py # 记录zsh中输入过的命令,便于今后的学习
└── zsh_config.sh # 配置zsh
```








安装软件包等初始配置

```
cd ~/workSpace/autoScript
bash init.sh
```

## 安装必要的软件包:

```
mkdir -p ~/workSpace/ && cd ~/workSpace/ && git clone https://github.com/clearsky0601/autoScript.git && bash autoScript/init.sh
```

## 安装oh-my-zsh: [官方网址](https://ohmyz.sh)

```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```


配置zsh和自动化脚本

```
cd ~/workSpace/autoScript && ./zsh_config.sh && ./config_diyCommand.sh
``` 


```
source ~/.zshrc
```




```
cd ~/workSpace/autoScript
bash config/oh_my_zsh_config.sh
```

配置zsh
```
cd ~/workSpace/autoScript
bash config/zsh_config.sh
```



# 自动化脚本的配置
```
./cofig_diyCommand.sh
```



同步命令文件

```
rsync -avz ~/.useful_commands.log ~/workSpace/note/useful_commands.log
```




<!-- 
## recordCommand.py --用于记录命令

```
chmode +x recordCommand.py
cd ./cofig
cp recordCommand.py /usr/local/bin/recordCommand
echo "alias lgc='recordCommand'" >> ~/.zshrc
source ~/.zshrc
```
## 有关远程仓库的一些操作配置

### ssh-keygen --用于生成ssh密钥

```
ssh-keygen -t rsa -C "xinyuscl@163.com"
```

### ssh-copy-id --用于将ssh密钥复制到远程服务器

```
ssh-copy-id -i ~/.ssh/id_rsa.pub root@192.168.1.100
```

### gitconfig --用于配置git全局参数

```
git config --global user.name "xinyuscl"
git config --global user.email "xinyuscl@163.com"
```

### gitignore --用于配置.gitignore文件

```
echo "node_modules" >> .gitignore
```

### 自动推送代码到远程仓库

```
cd 01.autoPush2Remote
chmod +x ./gitpush.sh

export PATH="$PATH:$HOME/workSpace/repositories/autoScript/01.autoPush2Remote"
alias gitpush="gitpush.sh"
```

```
gitpush
```

## 脚本的使用

```
cd 项目目录
gitpush
```

## 脚本的原理       
### gitpush.sh --用于自动推送代码到远程仓库





配置Vscode -->



## 配置github ssh



生成ssh密钥
```
ssh-keygen -t ed25519 -C "xinyuscl@163.com"
```

启动 ssh-agent：
```
eval "$(ssh-agent -s)"
```

添加 SSH 密钥到 ssh-agent：
```
ssh-add ~/.ssh/id_ed25519
```


查看 SSH 公钥：
```
cat ~/.ssh/id_ed25519.pub
```

登录到 GitHub 网站，进入 Settings -> SSH and GPG keys -> New SSH key，粘贴公钥内容并保存。

测试 SSH 连接：
```
ssh -T git@github.com
```

