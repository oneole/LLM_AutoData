# 环境搭建指南：大语言模型结构化数据分析系统

## 1. 项目技术概览

本文档提供了搭建"大语言模型实现结构化数据分析"项目所需的环境配置步骤。该项目将自然语言转换为SQL查询，实现数据分析自动化，集成以下核心技术：

- 结构化数据库（MySQL）
- 大语言模型（LLM）与提示词工程
- LangChain框架
- Web界面（Streamlit）
- 数据可视化（Plotly）
- GitHub项目管理

## 2. 系统要求

- Python 3.9+
- MySQL 8.0+
- Git
- 至少8GB RAM
- 操作系统：Windows 10/11、macOS 10.15+或Linux（Ubuntu 20.04+推荐）

## 3. 环境搭建步骤

### 3.1 Python环境配置

```bash
# 创建并激活虚拟环境
python -m venv venv

# Windows激活
venv\Scripts\activate

# macOS/Linux激活
source venv/bin/activate

# 安装项目依赖包
pip install langchain openai pymysql pandas numpy plotly streamlit vanna python-dotenv
```

### 3.2 MySQL数据库安装与配置

#### Windows安装步骤

1. 从官方网站下载MySQL安装程序：https://dev.mysql.com/downloads/installer/
2. 运行安装程序，选择"Developer Default"选项
3. 按照安装向导设置root用户密码
4. 完成安装后，验证MySQL服务是否正常运行

#### macOS安装步骤

```bash
# 使用Homebrew安装MySQL
brew install mysql

# 启动MySQL服务
brew services start mysql

# 设置root密码
mysql_secure_installation
```

#### Linux (Ubuntu)安装步骤

```bash
# 更新软件包列表
sudo apt update

# 安装MySQL
sudo apt install mysql-server

# 配置MySQL安全选项
sudo mysql_secure_installation

# 启动MySQL服务
sudo systemctl start mysql
```

### 3.3 Northwind示例数据库导入

1. 克隆Northwind数据库示例项目：

```bash
git clone https://github.com/Musili-Adebayo/Northwind-Database.git
cd Northwind-Database
```

2. 登录MySQL并创建Northwind数据库：

```bash
mysql -u root -p
CREATE DATABASE northwind;
USE northwind;
```

3. 导入SQL文件（以下示例使用命令行，也可使用MySQL Workbench等图形界面工具）：

```bash
# 退出MySQL客户端
exit

# 导入数据（路径可能需要调整）
mysql -u root -p northwind < Northwind.sql
```

### 3.4 配置LangChain与大语言模型

1. 创建`.env`文件存储API密钥：

```
OPENAI_API_KEY=your_openai_api_key_here
```

2. 创建配置文件`config.py`：

```python
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',
    'database': 'northwind',
    'port': 3306
}

# OpenAI配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LLM_MODEL = "gpt-3.5-turbo"  # 或其他适用模型
```

### 3.5 安装Vanna框架

```bash
pip install vanna
```

### 3.6 配置Git与GitHub

1. 安装Git（若未安装）：
   - Windows：下载并安装 https://git-scm.com/download/win
   - macOS：`brew install git`
   - Linux：`sudo apt install git`

2. 配置Git用户信息：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

3. 初始化项目版本控制：

```bash
# 创建项目目录
mkdir llm-sql-analysis
cd llm-sql-analysis

# 初始化Git仓库
git init

# 创建.gitignore文件
echo ".env
__pycache__/
venv/
*.pyc
.DS_Store" > .gitignore

# 创建项目基本结构
mkdir -p src/database src/models src/web
```

### 3.7 安装代码辅助工具（可选）

#### Codeium

1. 访问VSCode扩展市场搜索"Codeium"或直接访问：https://marketplace.visualstudio.com/items?itemName=Codeium.codeium
2. 安装扩展并按提示注册/登录Codeium账号

#### GitHub Copilot（需订阅）

1. 访问VSCode扩展市场搜索"GitHub Copilot"
2. 安装扩展并使用GitHub账号登录
3. 确保您已订阅GitHub Copilot服务

## 4. 项目结构设置

创建以下文件结构：

```
llm-sql-analysis/
├── .env                   # 环境变量（API密钥等）
├── .gitignore             # Git忽略文件
├── config.py              # 配置文件
├── requirements.txt       # 项目依赖
├── README.md              # 项目说明
├── app.py                 # 主应用入口
├── src/
│   ├── database/         # 数据库连接与操作
│   │   ├── __init__.py
│   │   ├── connection.py # 数据库连接模块
│   │   └── schema.py     # 数据库表结构定义
│   ├── models/           # LLM与提示词工程
│   │   ├── __init__.py
│   │   ├── text_to_sql.py # 文本转SQL实现
│   │   └── prompts.py    # 提示词模板
│   └── web/              # Web界面
│       ├── __init__.py
│       ├── streamlit_app.py # Streamlit应用
│       └── visualization.py # 数据可视化
└── tests/                # 测试目录
    ├── __init__.py
    ├── test_database.py
    └── test_models.py
```

## 5. 验证环境配置

创建一个简单的测试脚本`test_setup.py`来验证环境配置：

```python
import os
import pymysql
from langchain.llms import OpenAI
import streamlit as st
import plotly.express as px
import pandas as pd

def test_database_connection():
    try:
        # 使用config.py中的配置
        from config import DB_CONFIG
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("数据库连接成功！表列表：", tables)
        conn.close()
        return True
    except Exception as e:
        print(f"数据库连接失败：{e}")
        return False

def test_langchain_connection():
    try:
        from config import OPENAI_API_KEY
        if not OPENAI_API_KEY:
            print("未找到OpenAI API密钥")
            return False
            
        # 简单测试LangChain
        llm = OpenAI(temperature=0)
        result = llm("Hello, world!")
        print(f"LangChain测试成功，返回结果：{result}")
        return True
    except Exception as e:
        print(f"LangChain连接失败：{e}")
        return False

if __name__ == "__main__":
    print("开始环境测试...")
    db_test = test_database_connection()
    llm_test = test_langchain_connection()
    
    if db_test and llm_test:
        print("环境配置完成！所有组件测试通过。")
    else:
        print("环境测试未通过，请检查配置。")
```

运行测试脚本：

```bash
python test_setup.py
```

## 6. 常见问题解决

### 6.1 MySQL连接问题

问题：`Access denied for user 'root'@'localhost'`
解决：
```bash
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_new_password';
FLUSH PRIVILEGES;
```

### 6.2 Python依赖安装失败

问题：安装某些包时出现编译错误
解决（Linux/macOS）：
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential  # Ubuntu
# 或
brew install mysql-client  # macOS
```

### 6.3 OpenAI API认证错误

问题：`InvalidRequestError: No API key provided`
解决：确保`.env`文件正确设置，并已使用`load_dotenv()`加载环境变量。

## 7. 后续步骤

完成环境搭建后，您可以继续：
1. 实现数据库连接模块
2. 开发文本到SQL的转换功能
3. 创建Streamlit Web界面
4. 整合所有组件

## 8. 参考资源

- MySQL文档：https://dev.mysql.com/doc/
- LangChain文档：https://python.langchain.com/v0.1/docs/get_started/quickstart/
- Streamlit文档：https://docs.streamlit.io/
- Vanna文档：https://github.com/vanna-ai/vanna
- Plotly文档：https://plotly.com/python/​​​​​​​​​​​​​​​​