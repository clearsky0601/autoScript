#!/bin/bash

# 遍历当前目录下所有的 .txt 文件
for file in *.txt; do
    # 跳过没有匹配的文件
    [ -e "$file" ] || continue

    # 检查文件的首行是否为 #!/bin/bash
    first_line=$(head -n 1 "$file")
    if [[ "$first_line" == "#!/bin/bash" ]]; then
        # 获取文件名（去掉 .txt 扩展名）
        base_name="${file%.txt}"

        # 重命名文件，将扩展名改为 .sh
        mv "$file" "$base_name.sh"

        # 为脚本文件赋予执行权限
        chmod +x "$base_name.sh"

        echo "Processed $file -> $base_name.sh"
    else
        echo "Skipped $file (no #!/bin/bash in the first line)"
    fi
done

echo "Script execution completed."
