



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

