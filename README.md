# LLM_AutoData

# 大语言模型结构化数据分析项目

![版本](https://img.shields.io/badge/版本-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)

## 项目概述

本项目旨在利用大语言模型（LLM）技术结合结构化数据库，实现从自然语言描述到SQL查询的自动化转换，并生成可视化的数据分析结果。通过集成开源框架和提示词工程，为非技术用户提供直观的数据分析体验。


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


## 致谢

- [LangChain](https://python.langchain.com/)提供LLM框架支持
- [Streamlit](https://streamlit.io/)提供简洁的Web应用开发能力
- [Northwind数据库](https://github.com/Musili-Adebayo/Northwind-Database)提供示例数据
