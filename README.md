

# Script

[TOC]

## 初始化配置

**1️⃣ 安装必要的软件包:**

```
mkdir -p ~/workSpace/ && cd ~/workSpace/ && git clone https://github.com/clearsky0601/autoScript.git && bash autoScript/init.sh
```

**2️⃣ 安装oh-my-zsh: [官方网址](https://ohmyz.sh)**

```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

**3️⃣ 配置zsh和自动化脚本**

```
cd ~/workSpace/autoScript && ./zsh_config.sh && ./config_diyCommand.sh
```


```
source ~/.zshrc
```





## 远程仓库配置

1️⃣ 生成ssh密钥

```
ssh-keygen -t ed25519 -C "xinyuscl@163.com"
```

2️⃣ 启动 ssh-agent：

```
eval "$(ssh-agent -s)"
```

3️⃣ 添加 SSH 密钥到 ssh-agent：

```
ssh-add ~/.ssh/id_ed25519
```

4️⃣ 查看 SSH 公钥：

```
cat ~/.ssh/id_ed25519.pub
```

5️⃣ 登录到 GitHub 网站，进入 Settings -> SSH and GPG keys -> New SSH key，粘贴公钥内容并保存。

6️⃣ 测试 SSH 连接：

```
ssh -T git@github.com
```









## 文件目录

```
├── README.md
├── config_diyCommand.sh # 配置自定义命令
├── gitpush.sh # 用于自动推送代码到远程仓库 (gitpush)
├── init.sh # 用于初始化服务器
├── recordCommand.py # 记录zsh中输入过的命令,便于今后的学习(lgc)
├── 
└── zsh_config.sh # 配置zsh
```

