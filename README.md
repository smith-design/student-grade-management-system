# 学生成绩管理系统

基于 Python Flask 框架开发的学生成绩管理系统。

## 技术栈
- 后端：Python 3.8+
- Web 框架：Flask
- 模板引擎：Jinja2
- 数据库：MySQL (支持，默认降级为本地 JSON 存储)
- 前端：Bootstrap 5

## 数据库配置
项目默认使用本地 JSON 文件存储数据，无需安装数据库即可运行。
如果需要使用 MySQL 数据库：
1. 安装 MySQL 8.0+
2. 创建数据库并导入 `backend/schema.sql` 脚本
3. 修改 `backend/data_storage.py` 中的 `USE_MYSQL = True` 并配置数据库连接信息

## 快速开始
1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 启动服务
```bash
python app.py
```

3. 访问系统
打开浏览器访问 http://localhost:5001
