



```
cd 01.autoPush2Remote
chmod +x ./gitpush.sh

export PATH="$PATH:$HOME/workSpace/repositories/autoScript/01.autoPush2Remote"
alias gitpush="gitpush.sh"



```



# 自动化脚本的配置

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