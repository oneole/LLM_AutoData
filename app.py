import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from datetime import datetime

# 设置页面基本配置
st.set_page_config(
    page_title="智能数据分析平台",
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

# 侧边栏
with st.sidebar:
    st.header("数据库连接")

    # 数据库列表
    databases = {
        "Northwind 数据库": "northwind",
        "销售数据库": "sales",
        "客户数据库": "customers"
    }
    selected_db = st.selectbox("选择数据库", list(databases.keys()))

    st.markdown("---")
    st.header("保存的查询")
    saved_queries = [
        "按国家统计销售额",
        "最畅销产品分析",
        "员工业绩对比",
        "季度销售趋势"
    ]
    for query in saved_queries:
        if st.button(query):
            st.session_state.query_input = query

# 主内容区
st.title("智能数据分析平台")

# 查询输入区域
query_container = st.container()
with query_container:
    st.subheader("自然语言查询")
    query_input = st.text_area(
        "使用自然语言描述您的查询需求",
        placeholder="例如：显示2023年每月销售额，并按产品类别分组",
        height=100
    )

    # 示例查询
    st.markdown("### 示例查询")
    example_cols = st.columns(3)
    examples = [
        "查询销量最高的前10个产品及其类别",
        "按地区统计今年第一季度的销售总额并与去年同期比较",
        "找出订单量最多的客户以及他们的购买频率"
    ]
    for i, example in enumerate(examples):
        with example_cols[i]:
            if st.button(example, key=f"example_{i}"):
                st.session_state.query_input = example

    col1, col2 = st.columns([1, 6])
    with col1:
        execute = st.button("执行查询", type="primary")
    with col2:
        save = st.button("保存查询")

# 结果展示区域
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if execute or st.session_state.show_results:
    st.session_state.show_results = True

    tab1, tab2, tab3, tab4 = st.tabs(["SQL查询", "数据表格", "可视化", "数据分析"])

    with tab1:
        st.markdown("""
        <div class="sql-code">
        SELECT c.CategoryName, SUM(od.Quantity * od.UnitPrice) as TotalSales
        FROM Categories c
        JOIN Products p ON c.CategoryID = p.CategoryID
        JOIN [Order Details] od ON p.ProductID = od.ProductID
        JOIN Orders o ON od.OrderID = o.OrderID
        WHERE YEAR(o.OrderDate) = 2023
        GROUP BY c.CategoryName
        ORDER BY TotalSales DESC;
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        # 示例数据
        data = {
            "类别名称": ["海鲜", "肉/家禽", "饮料", "乳制品", "调味品", "谷物/面包", "零食"],
            "销售总额": [265432.89, 187621.45, 125874.32, 95632.10, 75482.65, 45321.78, 21436.90],
            "占比": ["32.5%", "23.0%", "15.4%", "11.7%", "9.2%", "5.5%", "2.6%"]
        }
        df = pd.DataFrame(data)
        st.dataframe(df, hide_index=True)

    with tab3:
        fig = px.bar(df, x="类别名称", y="销售总额", title="各类别销售总额")
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("数据洞察")
        st.write(
            "海鲜类别是最畅销的产品分类，贡献了2023年总销售额的32.5%。肉/家禽类排名第二，占比23%。这两个类别合计占总销售额的一半以上（55.5%）。")
        st.write("饮料、乳制品和调味品类别处于中等销售水平，合计占总销售额的36.3%。")
        st.write("谷物/面包和零食类别销售额相对较低，仅占总销售额的8.1%。可以考虑针对这些类别推出促销活动或产品创新，提升销售表现。")

        st.subheader("建议行动")
        st.write("1. 增加海鲜和肉/家禽类产品的库存，以满足高需求")
        st.write("2. 分析饮料类别的增长潜力，可能通过季节性促销提升销售")
        st.write("3. 考虑调整谷物/面包和零食类别的营销策略，挖掘增长机会")
