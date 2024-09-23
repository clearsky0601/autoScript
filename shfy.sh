#!/bin/bash

# 遍历当前目录下的所有 .txt 文件
for file in *.txt; do
    # 检查文件是否存在
    if [ -f "$file" ]; then
        # 使用 tr 命令删除所有的 \r 字符
        tr -d '\r' < "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
        
        # 检查文件的第一行是否为 #!/bin/bash
        if head -n 1 "$file" | grep -q "#!/bin/bash"; then
            # 获取不带扩展名的文件名
            filename="${file%.txt}"
            
            # 重命名文件，将 .txt 改为 .sh
            mv "$file" "${filename}.sh"
            
            # 给予执行权限
            chmod +x "${filename}.sh"
            
            echo "已处理并重命名: $file -> ${filename}.sh"
        else
            echo "已处理: $file"
        fi
    fi
done

echo "处理完成。"
