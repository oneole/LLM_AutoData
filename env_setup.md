# 环境搭建文档

## 1. 操作系统

- **推荐操作系统**：Windows 10 或 macOS 10.15 及以上版本
- **虚拟环境**（可选）：建议使用 `conda` 或 `venv` 创建独立的 Python 环境

## 2. 软件安装

### 2.1 数据库安装

1. **MySQL 安装**：
   - 下载并安装 MySQL Community Server 和 MySQL Workbench：
     - 官方网站：[https://dev.mysql.com/downloads/installer/](https://dev.mysql.com/downloads/installer/)
   - 配置 MySQL：
     - 设置 root 用户密码
     - 创建一个新的数据库（如 `northwind`）
     - 导入 Northwind 数据库：
       - 下载 SQL 文件：[Northwind Database](https://github.com/Musili-Adebayo/Northwind-Database)
       - 使用 MySQL Workbench 或命令行工具执行 SQL 文件

### 2.2 开发环境

1. **Python 安装**：
   - 下载并安装 Python 3.9 或更高版本（不要安装最新版本）：
     - 官方网站：[https://www.python.org/downloads/](https://www.python.org/downloads/)
   - 安装 PyCharm 或 VSCode：
     - PyCharm：[https://www.jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/)
     - VSCode：[https://code.visualstudio.com/](https://code.visualstudio.com/)

### 2.3 必要工具安装

1. **Git 安装**：

   - 下载并安装 Git：
     - 官方网站：[https://git-scm.com/downloads](https://git-scm.com/downloads)
   - 配置 Git：

     ```bash
     git config --global user.name "Your Name"
     git config --global user.email "your.email@example.com"
     ```

2. **Node.js 和 npm 安装**（可选）：
   - 下载并安装 Node.js：
     - 官方网站：[https://nodejs.org/](https://nodejs.org/)

## 3. 语言与工具包安装

### 3.1 Python 包安装

在终端或命令提示符中执行以下命令：

```bash
pip install pymysql langchain vanna streamlit plotly
```

### 3.2 语言模型工具包

1. **Vanna 安装**：

   - 克隆仓库并安装：

     ```bash
     git clone https://github.com/vanna-ai/vanna.git
     cd vanna
     pip install -e .
     ```

2. **LangChain 安装**：

   - 安装 LangChain：

     ```bash
     pip install langchain
     ```

## 4. 项目配置

### 4.1 克隆项目仓库

```bash
git clone https://github.com/oneole/LLM_AutoData.git
cd LLM_AutoData
```

### 4.2 安装项目依赖

```bash
pip install -r requirements.txt
```

### 4.3 配置数据库连接

在项目目录中创建 `config.py` 文件，添加以下内容：

```python
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'your_password'
DB_NAME = 'northwind'
```

## 5. 环境验证

1. **验证 MySQL 连接**：

   ```bash
   mysql -u root -p
   ```

   输入密码后，执行：

   ```sql
   SHOW DATABASES;
   ```

2. **验证 Python 环境**：

   ```bash
   python --version
   pip list
   ```

3. **验证 Streamlit 运行**：

   ```bash
   streamlit run your_main_script.py
   ```

## 6. 常见问题解答

1. **权限问题**：

   - 数据库权限不足：检查 MySQL 用户权限配置。
   - 文件权限问题：确保当前用户有执行权限。

2. **依赖项安装失败**：

   - 检查网络连接。
   - 使用 `pip install --user` 安装。

3. **数据库连接问题**：
   - 检查 `config.py` 配置是否正确。
   - 确保 MySQL 服务正在运行。
