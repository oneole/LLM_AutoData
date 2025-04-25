# Text2SQL 智能数据分析平台

## 项目简介

Text2SQL智能数据分析平台是一个基于大语言模型（LLM）的智能数据分析系统，能够将自然语言自动转换为SQL查询语句，并提供数据可视化功能。本项目集成了DeepSeek大语言模型和MySQL数据库，通过Streamlit构建了直观的Web界面，为非技术用户提供了便捷的数据分析解决方案。

## 功能特点

- 🔍 自然语言转SQL：支持使用自然语言描述查询需求
- 📊 智能数据分析：自动生成SQL查询并执行
- 📈 数据可视化：提供多种图表展示分析结果
- 🎯 示例查询：内置常用查询示例
- 💡 实时反馈：即时显示查询结果和可视化图表

## 技术架构

### 核心技术
- 大语言模型：DeepSeek API
- 数据库：MySQL
- Web框架：Streamlit
- 可视化：Plotly
- 数据库连接：PyMySQL

### 系统架构
```
自然语言输入 → 提示词工程 → LLM处理 → SQL生成 → 数据库查询 → 数据分析 → 可视化输出
```

## 安装说明

### 环境要求
- Python 3.8+
- MySQL 5.7+
- 其他依赖包（见requirements.txt）

### 安装步骤

1. 克隆项目
```bash
git clone [项目地址]
cd [项目目录]
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建.env文件并配置以下参数：
```
DEEPSEEK_API_KEY=你的DeepSeek API密钥
DB_HOST=数据库主机地址
DB_USER=数据库用户名
DB_PASSWORD=数据库密码
DB_NAME=数据库名称
```

4. 初始化数据库
```bash
mysql -u [用户名] -p [数据库名] < llmauto.sql
```

## 使用方法

1. 启动应用
```bash
streamlit run app.py
```

2. 访问Web界面
打开浏览器访问 http://localhost:8501

3. 使用示例
- 在查询框中输入自然语言描述
- 点击"执行查询"按钮
- 查看SQL查询、数据表格和可视化结果

## 示例查询

- 查询2022年入学的学生
- 查询数学成绩90分以上的学生
- 查询各班级的班主任信息
- 计算每个学生的平均成绩
- 查询高二年级各班级人数
- 查询高三年级学生的各科成绩
- 统计各年级学生的平均成绩
- 查找成绩最高的前5名学生

## 数据库结构

项目使用以下数据表：
- classes：班级信息
- students：学生信息
- teachers：教师信息
- subjects：学科信息
- scores：成绩信息

## 开发团队

[团队信息]

## 许可证

MIT License

## 致谢

- DeepSeek AI
- Vanna AI
- Streamlit
- Plotly
- MySQL

## 更新日志

### v1.0.0 (2024-04-12)
- 初始版本发布
- 实现基础Text2SQL功能
- 集成数据可视化
- 支持多种查询示例 