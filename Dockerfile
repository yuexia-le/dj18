FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 先拷贝依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝项目所有代码
COPY . .

# 暴露端口（对应 app.py 中的默认端口）
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]