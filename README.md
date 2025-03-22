# LLM_AutoData

# 大语言模型结构化数据分析项目

![版本](https://img.shields.io/badge/版本-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![License](https://img.shields.io/badge/许可证-MIT-orange)

## 项目概述

本项目旨在利用大语言模型（LLM）技术结合结构化数据库，实现从自然语言描述到SQL查询的自动化转换，并生成可视化的数据分析结果。通过集成开源框架和提示词工程，为非技术用户提供直观的数据分析体验。

![系统架构](https://via.placeholder.com/800x400?text=系统架构图)

## 主要功能

- **自然语言转SQL**: 将用户输入的自然语言问题自动转换为SQL查询语句
- **数据库交互**: 连接MySQL数据库执行生成的SQL查询
- **数据可视化**: 自动为查询结果生成合适的图表展示
- **Web界面**: 提供直观易用的交互界面，使非技术用户能轻松分析数据

## 技术栈

- **前端**: Streamlit
- **后端**: Python, LangChain
- **数据库**: MySQL
- **大语言模型**: DeepSeek API (OpenAI兼容)
- **数据可视化**: Plotly

## 快速开始

### 环境要求

- Python 3.9+
- MySQL 8.0+
- Git

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/your-username/llm-data-analysis.git
cd llm-data-analysis
```

2. **创建并激活虚拟环境**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置环境变量**

创建`.env`文件并填入以下内容:

```
# DeepSeek API配置
OPENAI_API_KEY=你的DeepSeek_API密钥
OPENAI_API_BASE=https://api.deepseek.com/v1

# 数据库连接
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=你的数据库密码
DB_NAME=northwind
```

5. **准备示例数据库**

```bash
# 克隆Northwind示例数据库
git clone https://github.com/Musili-Adebayo/Northwind-Database.git

# 按照Northwind-Database中的说明导入数据库
```

6. **启动应用**

```bash
streamlit run src/web/app.py
```

应用将在 `http://localhost:8501` 运行。

## 使用指南

1. 在输入框中用自然语言描述你的查询需求，例如:
   - "显示所有来自德国的客户"
   - "计算每个产品类别的总销售额"
   - "找出2022年销售额最高的前5个产品"

2. 点击"分析"按钮，系统将:
   - 生成并显示对应的SQL查询
   - 执行查询并显示结果表格
   - 自动创建数据可视化图表

3. 查看和分析结果，如需修改查询，可调整输入并重新分析


## 进阶开发

### 使用Vanna框架

本项目可以集成[Vanna](https://github.com/vanna-ai/vanna)框架以提升Text-to-SQL的功能:

```python
from vanna.remote import VannaDefault

vanna = VannaDefault(
    api_key="your_vanna_api_key",
    model="deepseek-coder"
)

# 添加数据库结构信息
vanna.add_model(...)

# 生成SQL
sql = vanna.generate_sql("你的自然语言查询")
```

### 改进数据可视化

可以扩展数据可视化能力:

```python
# 在app.py中添加更多图表选项
chart_type = st.selectbox(
    "选择图表类型",
    ["柱状图", "折线图", "饼图", "散点图"]
)

# 根据选择生成相应图表
if chart_type == "柱状图":
    fig = px.bar(df, x=x_col, y=y_col)
elif chart_type == "折线图":
    fig = px.line(df, x=x_col, y=y_col)
# ...其他图表类型
```


## 致谢

- [LangChain](https://python.langchain.com/)提供LLM框架支持
- [Streamlit](https://streamlit.io/)提供简洁的Web应用开发能力
- [Northwind数据库](https://github.com/Musili-Adebayo/Northwind-Database)提供示例数据
