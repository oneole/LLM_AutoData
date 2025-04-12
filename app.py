import streamlit as st
import pandas as pd
import plotly.express as px
# import mysql.connector # SQLAlchemy will handle the connection
from sqlalchemy import create_engine, text
from datetime import datetime
import os # 用于未来从环境变量获取凭据 (推荐)

# 设置页面基本配置
st.set_page_config(
    page_title="学生成绩分析平台",
    layout="wide"
)

# 添加自定义CSS
st.markdown("""
<style>
    .st-emotion-cache-16idsys p {
        font-size: 20px;
        font-weight: 600;
        color: #1e293b;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .sql-code {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
        font-size: 0.875rem;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# --- 数据库自动连接 ---

# 硬编码连接信息 (警告：不建议在生产环境中使用)
DB_HOST = "152.136.150.40"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "mariadb_zMWZZk"
DB_NAME = "llmauto"

# 使用 Streamlit 的缓存机制来管理数据库连接
@st.cache_resource
def get_db_engine():
    """建立并返回 SQLAlchemy 数据库引擎"""
    try:
        # 构建数据库连接 URI
        # 确保密码中的特殊字符已进行 URL 编码（如果需要，但通常 SQLAlchemy 处理得很好）
        db_uri = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4&collation=utf8mb4_general_ci"
        engine = create_engine(db_uri, echo=False) # echo=True 用于调试SQLAlchemy
        # 测试连接 (可选, create_engine 是惰性的)
        with engine.connect() as connection:
            pass # 如果连接成功，这里不会抛出异常
        return engine
    except Exception as err:
        st.error(f"数据库引擎创建失败: {err}")
        return None

# 尝试获取数据库连接
db_engine = get_db_engine() # Changed variable name

def save_query(query):
    """Saves the query to the database."""
    if not db_engine:
        st.error("数据库引擎不可用，无法保存查询。")
        return
    try:
        with db_engine.connect() as connection:
            connection.execute(
                text("INSERT INTO saved_queries (query) VALUES (:query)"),
                {"query": query}
            )
        st.success("查询已保存！")
    except Exception as e:
        st.error(f"保存查询失败: {e}")


# --- Helper Function to Run Queries ---
def run_query(query, engine=db_engine): # Pass engine as default argument
    """Executes a query using SQLAlchemy engine and returns results as a Pandas DataFrame."""
    if not engine:
        st.error("数据库引擎不可用，无法执行查询。")
        return None
    try:
        # 使用 Pandas 和 SQLAlchemy Engine 执行查询
        # 对于 SHOW TABLES, DESCRIBE 等非标准 SELECT 语句，最好使用 text()
        # 或者直接使用 engine.connect() 和 cursor
        with engine.connect() as connection:
             df = pd.read_sql(text(query), connection)
        return df
    except Exception as e:
        st.error(f"查询执行错误: {e}")
        # SQLAlchemy engine handles pooling, no need to manually reconnect here
        return None

# --- 侧边栏 ---
with st.sidebar:
    # 显示连接状态
    if db_engine: # Check engine status
        st.success(f"数据库引擎已连接到 '{DB_NAME}'")
    else:
        st.error("数据库引擎未连接")

    st.markdown("---")

    st.header("保存的查询")
    saved_queries = [
        "查询高一各班级数学平均分",
        "找出总分最高的学生",
        "统计各科目的及格率",
        "查询张小明的所有成绩"
    ]
    for query in saved_queries:
        if st.button(query, key=f"saved_{query}"):
            st.session_state.query_input = query
# 侧边栏结束
# 主内容区
st.title("学生成绩分析平台")

# 查询输入区域
query_container = st.container()
with query_container:
    st.subheader("自然语言查询")
    query_input = st.text_area(
        "使用自然语言描述您的查询需求（例如：查询高一(1)班的平均分）",
        placeholder="例如：显示高一(1)班所有学生的数学成绩，并按分数降序排列",
        height=100
    )

    # 示例查询
    st.markdown("### 示例查询")
    example_cols = st.columns(3)
    examples = [
        "查询高一年级所有班级的语文平均分",
        "找出数学成绩低于60分的学生名单",
        "统计每个班级的学生人数"
    ]
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(example, key=f"example_{i}"):
                st.session_state.query_input = example

    col1, col2 = st.columns([1, 6])
    with col1:
        execute = st.button("执行查询", type="primary")
    with col2:
        save = st.button("保存查询", on_click=save_query, args=(query_input,))

# --- 数据库内容预览 (仅当连接成功时显示) ---
if db_engine: # Check engine status
    with st.expander("数据库内容预览", expanded=False):
        st.write(f"当前数据库: `{DB_NAME}`")
        tables_df = run_query("SHOW TABLES;")

        if tables_df is not None and not tables_df.empty:
            table_list = tables_df.iloc[:, 0].tolist() # 获取第一列作为表名列表
            selected_table = st.selectbox("选择要预览的表:", table_list)

            if selected_table:
                # 显示表结构
                st.subheader(f"表结构: `{selected_table}`")
                schema_df = run_query(f"DESCRIBE `{selected_table}`;") # 使用反引号处理可能的特殊表名
                if schema_df is not None:
                    st.dataframe(schema_df, use_container_width=True)

                # 显示前5行数据
                st.subheader(f"前5行数据: `{selected_table}`")
                data_df = run_query(f"SELECT * FROM `{selected_table}` LIMIT 5;")
                if data_df is not None:
                    st.dataframe(data_df, use_container_width=True)
        elif tables_df is not None: # DataFrame is empty
             st.info("数据库中没有找到任何表。")
        # else: run_query already showed an error

# --- 结果展示区域 ---
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if execute or st.session_state.show_results:
    st.session_state.show_results = True

    tab1, tab2, tab3, tab4 = st.tabs(["SQL查询", "数据表格", "可视化", "数据分析"])

    with tab1:
        # 示例：显示一个与学校数据相关的SQL查询
        st.markdown("""
        <div class="sql-code">
        SELECT
            c.class_name AS '班级名称',
            AVG(sc.score) AS '数学平均分'
        FROM scores sc
        JOIN students s ON sc.student_id = s.student_id
        JOIN classes c ON s.class_id = c.class_id
        JOIN subjects sub ON sc.subject_id = sub.subject_id
        WHERE sub.subject_name = '数学' AND c.grade_level = '高一'
        GROUP BY c.class_name
        ORDER BY c.class_name;
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        # 示例：显示一个与学校数据相关的表格
        data = {
            "班级名称": ["高一(1)班", "高一(2)班", "高一(3)班"],
            "数学平均分": [85.50, 88.75, 86.20],
            "学生人数": [45, 46, 44]
        }
        df = pd.DataFrame(data)
        st.dataframe(df, hide_index=True, use_container_width=True)

    with tab3:
        # 示例：显示一个与学校数据相关的图表
        fig = px.bar(df, x="班级名称", y="数学平均分", title="高一各班级数学平均分对比",
                     labels={'班级名称':'班级', '数学平均分':'平均分'}, text_auto=True)
        fig.update_layout(xaxis_title="班级", yaxis_title="数学平均分")
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("数据洞察")
        st.write(
            "根据数据显示，高一(2)班的数学平均分最高（88.75分），略高于高一(3)班（86.20分）和高一(1)班（85.50分）。"
        )
        st.write("所有班级的数学平均分均在85分以上，表现良好。")
        st.write("可以进一步分析各班级内部的分数分布，了解是否存在较大的个体差异。")

        st.subheader("建议行动")
        st.write("1. 关注高一(1)班的数学成绩，分析是否存在普遍性问题或个别学生需要额外辅导。")
        st.write("2. 对高一(2)班的优秀表现进行总结，分享教学经验。")
        st.write("3. 鼓励各班级之间进行学习交流，共同提高。")
