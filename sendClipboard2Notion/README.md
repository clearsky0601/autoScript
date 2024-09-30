


## 把剪切板的内容保存到Notion的database

1️⃣ 为sendClipboard2Notion.py添加执行权限
```
chmod +x sendClipboard2Notion.py
```

2️⃣ 将sendClipboard2Notion.py添加到/usr/local/bin目录下
```
sudo cp sendClipboard2Notion.py /usr/local/bin/
```

3️⃣ sendClipboard2Notion.py 更换别名`lgno` 并添加到zshrc
```
echo "alias lgno='/usr/local/bin/sendClipboard2Notion.py'" >> ~/.zshrc 
```

4️⃣ 使zshrc生效
```
source ~/.zshrc
```


```



```


```
