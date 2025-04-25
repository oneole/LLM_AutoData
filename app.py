import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from vanna_mysql_fix import DeepSeekVanna

# 设置页面配置
st.set_page_config(
    page_title="Text2SQL 智能数据分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
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
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #42A5F5;
        margin-bottom: 1rem;
    }
    .info-text {
        font-size: 1rem;
        color: #64B5F6;
    }
    .sql-code {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
        font-size: 0.875rem;
        color: #334155;
    }
    div.stButton > button {
        background-color: #1E88E5;
        color: white;
        border-radius: 4px;
    }
    div.stButton > button:hover {
        background-color: #1565C0;
        color: white;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .highlight {
        color: #FF5252;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 DeepSeekVanna
@st.cache_resource
def load_model():
    text2sql = DeepSeekVanna()
    
    # 训练数据库结构 - 班级表
    text2sql.train(ddl="""
    CREATE TABLE `classes` (
      `class_id` int(11) NOT NULL AUTO_INCREMENT,
      `grade_level` enum('高一','高二','高三') NOT NULL,
      `class_name` varchar(20) NOT NULL,
      `homeroom_teacher_id` int(11) DEFAULT NULL,
      `student_count` int(11) DEFAULT 0,
      PRIMARY KEY (`class_id`),
      KEY `homeroom_teacher_id` (`homeroom_teacher_id`),
      CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`homeroom_teacher_id`) REFERENCES `teachers` (`teacher_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
    """)

    # 学生表
    text2sql.train(ddl="""
    CREATE TABLE `students` (
      `student_id` int(11) NOT NULL AUTO_INCREMENT,
      `student_name` varchar(50) NOT NULL,
      `class_id` int(11) DEFAULT NULL,
      `admission_year` year(4) DEFAULT NULL,
      PRIMARY KEY (`student_id`),
      KEY `class_id` (`class_id`),
      CONSTRAINT `students_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
    """)

    # 教师表
    text2sql.train(ddl="""
    CREATE TABLE `teachers` (
      `teacher_id` int(11) NOT NULL AUTO_INCREMENT,
      `teacher_name` varchar(50) NOT NULL,
      `contact_number` varchar(20) DEFAULT NULL,
      PRIMARY KEY (`teacher_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
    """)

    # 学科表
    text2sql.train(ddl="""
    CREATE TABLE `subjects` (
      `subject_id` int(11) NOT NULL AUTO_INCREMENT,
      `subject_name` varchar(20) NOT NULL,
      PRIMARY KEY (`subject_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
    """)

    # 成绩表
    text2sql.train(ddl="""
    CREATE TABLE `scores` (
      `score_id` int(11) NOT NULL AUTO_INCREMENT,
      `student_id` int(11) DEFAULT NULL,
      `subject_id` int(11) DEFAULT NULL,
      `score` decimal(5,2) DEFAULT NULL,
      `exam_date` date DEFAULT NULL,
      PRIMARY KEY (`score_id`),
      KEY `student_id` (`student_id`),
      KEY `subject_id` (`subject_id`),
      CONSTRAINT `scores_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
      CONSTRAINT `scores_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
    """)

    # 视图结构
    text2sql.train(ddl="""
    CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `grade_scores` AS 
    SELECT 
      `c`.`grade_level` AS `grade_level`, 
      `c`.`class_name` AS `class_name`, 
      `s`.`student_name` AS `student_name`, 
      `sub`.`subject_name` AS `subject_name`, 
      `sc`.`score` AS `score`, 
      `t`.`teacher_name` AS `homeroom_teacher` 
    FROM 
      ((((`scores` `sc` 
      JOIN `students` `s` ON(`s`.`student_id` = `sc`.`student_id`)) 
      JOIN `classes` `c` ON(`c`.`class_id` = `s`.`class_id`)) 
      JOIN `subjects` `sub` ON(`sub`.`subject_id` = `sc`.`subject_id`)) 
      JOIN `teachers` `t` ON(`t`.`teacher_id` = `c`.`homeroom_teacher_id`));
    """)

    # 训练一些常见查询示例
    text2sql.train(
        question="查询所有高三学生",
        sql="SELECT `student_id`, `student_name`, `class_id` FROM `students` WHERE `class_id` IN (SELECT `class_id` FROM `classes` WHERE `grade_level` = '高三')"
    )

    text2sql.train(
        question="查询2022年入学的学生",
        sql="SELECT `student_id`, `student_name`, `class_id` FROM `students` WHERE `admission_year` = 2022"
    )

    text2sql.train(
        question="查询数学成绩90分以上的学生",
        sql="SELECT s.`student_id`, s.`student_name`, sc.`score` FROM `students` s JOIN `scores` sc ON s.`student_id` = sc.`student_id` JOIN `subjects` sub ON sc.`subject_id` = sub.`subject_id` WHERE sub.`subject_name` = '数学' AND sc.`score` > 90"
    )

    text2sql.train(
        question="查询各班级的班主任信息",
        sql="SELECT c.`class_name`, t.`teacher_name`, t.`contact_number` FROM `classes` c JOIN `teachers` t ON c.`homeroom_teacher_id` = t.`teacher_id`"
    )

    text2sql.train(
        question="查询高二年级各班级人数",
        sql="SELECT `class_id`, `class_name`, `student_count` FROM `classes` WHERE `grade_level` = '高二'"
    )

    text2sql.train(
        question="查询所有学科的名称",
        sql="SELECT `subject_id`, `subject_name` FROM `subjects`"
    )

    text2sql.train(
        question="计算每个学生的平均成绩",
        sql="SELECT s.`student_id`, s.`student_name`, AVG(sc.`score`) as average_score FROM `students` s JOIN `scores` sc ON s.`student_id` = sc.`student_id` GROUP BY s.`student_id`, s.`student_name`"
    )

    text2sql.train(
        question="查询高一年级学生的语文成绩",
        sql="SELECT c.`class_name`, s.`student_name`, sc.`score` FROM `students` s JOIN `classes` c ON s.`class_id` = c.`class_id` JOIN `scores` sc ON s.`student_id` = sc.`student_id` JOIN `subjects` sub ON sc.`subject_id` = sub.`subject_id` WHERE c.`grade_level` = '高一' AND sub.`subject_name` = '语文'"
    )
    
    # 新增训练示例
    text2sql.train(
        question="查询2021年入学的学生名单",
        sql="SELECT `student_id`, `student_name`, `class_id` FROM `students` WHERE `admission_year` = 2021"
    )
    
    text2sql.train(
        question="查询各年级的班级数量",
        sql="SELECT `grade_level`, COUNT(*) as class_count FROM `classes` GROUP BY `grade_level`"
    )
    
    text2sql.train(
        question="查询每个班级的学生人数",
        sql="SELECT c.`class_name`, c.`student_count` FROM `classes` c ORDER BY c.`class_name`"
    )
    
    text2sql.train(
        question="查询所有教师的联系方式",
        sql="SELECT `teacher_name`, `contact_number` FROM `teachers`"
    )
    
    text2sql.train(
        question="查询数学成绩最高的前3名学生",
        sql="SELECT s.`student_name`, sc.`score` FROM `students` s JOIN `scores` sc ON s.`student_id` = sc.`student_id` JOIN `subjects` sub ON sc.`subject_id` = sub.`subject_id` WHERE sub.`subject_name` = '数学' ORDER BY sc.`score` DESC LIMIT 3"
    )
    
    text2sql.train(
        question="查询每个班级的班主任姓名",
        sql="SELECT c.`class_name`, t.`teacher_name` FROM `classes` c JOIN `teachers` t ON c.`homeroom_teacher_id` = t.`teacher_id`"
    )
    
    text2sql.train(
        question="查询2023年12月20日的考试成绩",
        sql="SELECT s.`student_name`, sub.`subject_name`, sc.`score` FROM `scores` sc JOIN `students` s ON sc.`student_id` = s.`student_id` JOIN `subjects` sub ON sc.`subject_id` = sub.`subject_id` WHERE sc.`exam_date` = '2023-12-20'"
    )
    
    text2sql.train(
        question="查询各科目的平均分",
        sql="SELECT sub.`subject_name`, AVG(sc.`score`) as average_score FROM `scores` sc JOIN `subjects` sub ON sc.`subject_id` = sub.`subject_id` GROUP BY sub.`subject_name`"
    )
    
    text2sql.train(
        question="查询每个年级的学生总数",
        sql="SELECT c.`grade_level`, SUM(c.`student_count`) as total_students FROM `classes` c GROUP BY c.`grade_level`"
    )
    
    # 添加更多训练示例
    text2sql.train(
        question="查询每个班级的平均成绩",
        sql="SELECT c.`class_name`, AVG(sc.`score`) as avg_score FROM `classes` c JOIN `students` s ON c.`class_id` = s.`class_id` JOIN `scores` sc ON s.`student_id` = sc.`student_id` GROUP BY c.`class_name`"
    )
    
    text2sql.train(
        question="查询成绩排名前5的学生",
        sql="SELECT s.`student_name`, AVG(sc.`score`) as avg_score FROM `students` s JOIN `scores` sc ON s.`student_id` = sc.`student_id` GROUP BY s.`student_id`, s.`student_name` ORDER BY avg_score DESC LIMIT 5"
    )
    
    text2sql.train(
        question="查询每个科目的最高分和最低分",
        sql="SELECT sub.`subject_name`, MAX(sc.`score`) as max_score, MIN(sc.`score`) as min_score FROM `scores` sc JOIN `subjects` sub ON sc.`subject_id` = sub.`subject_id` GROUP BY sub.`subject_name`"
    )
    
    text2sql.train(
        question="查询每个班级的及格率",
        sql="SELECT c.`class_name`, COUNT(CASE WHEN sc.`score` >= 60 THEN 1 END) * 100.0 / COUNT(*) as pass_rate FROM `classes` c JOIN `students` s ON c.`class_id` = s.`class_id` JOIN `scores` sc ON s.`student_id` = sc.`student_id` GROUP BY c.`class_name`"
    )
    
    text2sql.train(
        question="查询每个学生的成绩波动情况",
        sql="SELECT s.`student_name`, STDDEV(sc.`score`) as score_std FROM `students` s JOIN `scores` sc ON s.`student_id` = sc.`student_id` GROUP BY s.`student_id`, s.`student_name` ORDER BY score_std DESC"
    )
    
    text2sql.train(
        question="查询每个班级的优秀率（90分以上）",
        sql="SELECT c.`class_name`, COUNT(CASE WHEN sc.`score` >= 90 THEN 1 END) * 100.0 / COUNT(*) as excellent_rate FROM `classes` c JOIN `students` s ON c.`class_id` = s.`class_id` JOIN `scores` sc ON s.`student_id` = sc.`student_id` GROUP BY c.`class_name`"
    )
    
    text2sql.train(
        question="查询每个科目的成绩分布情况",
        sql="SELECT sub.`subject_name`, COUNT(CASE WHEN sc.`score` >= 90 THEN 1 END) as excellent, COUNT(CASE WHEN sc.`score` >= 80 AND sc.`score` < 90 THEN 1 END) as good, COUNT(CASE WHEN sc.`score` >= 60 AND sc.`score` < 80 THEN 1 END) as pass, COUNT(CASE WHEN sc.`score` < 60 THEN 1 END) as fail FROM `scores` sc JOIN `subjects` sub ON sc.`subject_id` = sub.`subject_id` GROUP BY sub.`subject_name`"
    )
    
    text2sql.train(
        question="查询每个班级的班主任和班级人数",
        sql="SELECT c.`class_name`, t.`teacher_name`, c.`student_count` FROM `classes` c JOIN `teachers` t ON c.`homeroom_teacher_id` = t.`teacher_id`"
    )
    
    text2sql.train(
        question="查询每个学生的各科成绩排名",
        sql="SELECT s.`student_name`, sub.`subject_name`, sc.`score`, RANK() OVER (PARTITION BY sub.`subject_id` ORDER BY sc.`score` DESC) as rank FROM `students` s JOIN `scores` sc ON s.`student_id` = sc.`student_id` JOIN `subjects` sub ON sc.`subject_id` = sub.`subject_id`"
    )
    
    text2sql.train(
        question="查询每个班级的科目平均分",
        sql="SELECT c.`class_name`, sub.`subject_name`, AVG(sc.`score`) as avg_score FROM `classes` c JOIN `students` s ON c.`class_id` = s.`class_id` JOIN `scores` sc ON s.`student_id` = sc.`student_id` JOIN `subjects` sub ON sc.`subject_id` = sub.`subject_id` GROUP BY c.`class_name`, sub.`subject_name`"
    )
    
    text2sql.train(
        question="查询每个学生的成绩进步情况",
        sql="SELECT s.`student_name`, MAX(sc.`score`) - MIN(sc.`score`) as score_improvement FROM `students` s JOIN `scores` sc ON s.`student_id` = sc.`student_id` GROUP BY s.`student_id`, s.`student_name` ORDER BY score_improvement DESC"
    )
    
    text2sql.train(
        question="查询每个班级的科目及格率",
        sql="SELECT c.`class_name`, sub.`subject_name`, COUNT(CASE WHEN sc.`score` >= 60 THEN 1 END) * 100.0 / COUNT(*) as pass_rate FROM `classes` c JOIN `students` s ON c.`class_id` = s.`class_id` JOIN `scores` sc ON s.`student_id` = sc.`student_id` JOIN `subjects` sub ON sc.`subject_id` = sub.`subject_id` GROUP BY c.`class_name`, sub.`subject_name`"
    )
    
    return text2sql

# 推荐示例查询
example_queries = [
    "查询2022年入学的学生",
    "查询数学成绩90分以上的学生",
    "查询各班级的班主任信息",
    "计算每个学生的平均成绩",
    "查询高二年级各班级人数",
    "查询高三年级学生的各科成绩",
    "统计各年级学生的平均成绩",
    "查找成绩最高的前5名学生"
]

# 加载模型
text2sql = load_model()

# 侧边栏
with st.sidebar:
    st.title("数据查询助手")
    
    st.header("数据库信息")
    st.info("当前连接: 教育数据库")
    
    st.markdown("---")
    
    st.header("查询示例")
    st.write("点击以下示例尝试：")
    
    # 将示例查询分组显示
    for i, query in enumerate(example_queries):
        if st.button(query, key=f"sidebar_query_{i}"):
            st.session_state.query = query
            
    st.markdown("---")
    st.markdown("### 关于")
    st.write("本应用使用DeepSeek x Vanna将自然语言转换为SQL查询，并提供数据可视化功能。")
    st.write("支持查询学生、班级、教师和成绩等信息。")

# 主界面
st.title("Text2SQL 智能数据分析平台")
st.write("通过自然语言查询数据，自动生成SQL并可视化结果")

# 查询输入区域
query_container = st.container()
with query_container:
    st.subheader("自然语言查询")
    query = st.text_area(
        "输入你的查询问题",
        placeholder="例如: 查询数学成绩超过90分的学生",
        value=st.session_state.get("query", ""),
        height=100
    )

    
    col1, col2 = st.columns([1, 6])
    with col1:
        execute_query = st.button("执行查询", type="primary")

# 初始化结果显示状态
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# 当用户点击执行查询或已有查询
if execute_query or ('query' in st.session_state and st.session_state.query and not st.session_state.show_results):
    if execute_query and query:  # 新查询
        st.session_state.query = query
    
    st.session_state.show_results = True
    query_text = st.session_state.query

# 如果应该显示结果
if st.session_state.show_results and 'query' in st.session_state and st.session_state.query:
    query_text = st.session_state.query
    
    with st.spinner('正在处理查询...'):
        try:
            # 生成SQL查询
            sql = text2sql.generate_sql(query_text)
            
            # 执行SQL查询
            results = text2sql.execute_sql(sql)
            
            # 将结果转换为DataFrame
            if results:
                df = pd.DataFrame(results)
                
                # 确保score列被识别为数值类型
                if 'score' in df.columns:
                    df['score'] = pd.to_numeric(df['score'], errors='coerce')
                
                # 创建标签页
                tab1, tab2, tab3, tab4 = st.tabs(["SQL查询", "数据表格", "数据分析", "数据可视化"])
                
                with tab1:
                    st.subheader("SQL查询")
                    st.code(sql, language="sql")
                
                with tab2:
                    st.subheader("数据表格")
                    st.dataframe(df, use_container_width=True)
                
                with tab3:
                    st.subheader("数据分析")
                    # 数据分析区域已清空，只保留标签页结构
                    
                with tab4:
                    st.subheader("数据可视化")
                    if not df.empty:
                        # 根据数据列类型自动选择可视化方式
                        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                        categorical_cols = df.select_dtypes(include=['object']).columns
                        
                        # 检查是否有score列
                        if 'score' in df.columns:
                            # 如果有科目和学生信息，创建成绩分布图
                            if 'subject_name' in df.columns and 'student_name' in df.columns:
                                # 按科目分组的成绩箱线图
                                fig_box = px.box(df, x='subject_name', y='score', 
                                               title='各科目成绩分布',
                                               labels={'subject_name': '科目', 'score': '分数'})
                                st.plotly_chart(fig_box, use_container_width=True)
                                
                                # 按学生分组的成绩条形图
                                fig_bar = px.bar(df, x='student_name', y='score', color='subject_name',
                                               title='学生各科成绩',
                                               labels={'student_name': '学生', 'score': '分数', 'subject_name': '科目'})
                                st.plotly_chart(fig_bar, use_container_width=True)
                                
                                # 添加成绩热力图
                                pivot_df = df.pivot(index='student_name', columns='subject_name', values='score')
                                fig_heatmap = px.imshow(pivot_df, 
                                                      title='学生成绩热力图',
                                                      labels=dict(x='科目', y='学生', color='分数'))
                                st.plotly_chart(fig_heatmap, use_container_width=True)
                            
                        # 检查是否有班级信息
                        elif 'class_name' in df.columns:
                            if 'student_count' in df.columns:
                                # 班级人数分布
                                fig_bar = px.bar(df, x='class_name', y='student_count',
                                               title='各班级人数分布',
                                               labels={'class_name': '班级', 'student_count': '学生人数'})
                                st.plotly_chart(fig_bar, use_container_width=True)
                            
                            if 'teacher_name' in df.columns:
                                # 班主任信息
                                fig_bar = px.bar(df, x='class_name', y='teacher_name',
                                               title='班级班主任信息',
                                               labels={'class_name': '班级', 'teacher_name': '班主任'})
                                st.plotly_chart(fig_bar, use_container_width=True)
                        
                        # 检查是否有年级信息
                        elif 'grade_level' in df.columns:
                            if 'total_students' in df.columns:
                                # 年级学生总数
                                fig_pie = px.pie(df, values='total_students', names='grade_level',
                                               title='各年级学生总数分布')
                                st.plotly_chart(fig_pie, use_container_width=True)
                        
                        # 检查是否有及格率或优秀率
                        elif any(col.endswith('_rate') for col in df.columns):
                            rate_cols = [col for col in df.columns if col.endswith('_rate')]
                            for rate_col in rate_cols:
                                if 'class_name' in df.columns:
                                    fig_bar = px.bar(df, x='class_name', y=rate_col,
                                                   title=f'各班级{rate_col}分布',
                                                   labels={'class_name': '班级', rate_col: '比率(%)'})
                                    st.plotly_chart(fig_bar, use_container_width=True)
                                    
                                    # 添加饼图
                                    fig_pie = px.pie(df, values=rate_col, names='class_name',
                                                   title=f'各班级{rate_col}占比')
                                    st.plotly_chart(fig_pie, use_container_width=True)
                                    
                                    # 添加热力图
                                    if 'subject_name' in df.columns:
                                        pivot_df = df.pivot(index='class_name', columns='subject_name', values=rate_col)
                                        fig_heatmap = px.imshow(pivot_df, 
                                                              title=f'各班级科目{rate_col}热力图',
                                                              labels=dict(x='科目', y='班级', color='比率(%)'))
                                        st.plotly_chart(fig_heatmap, use_container_width=True)
                        
                        # 检查是否有pass_rate列（直接检查列名）
                        elif 'pass_rate' in df.columns:
                            if 'class_name' in df.columns:
                                # 柱状图
                                fig_bar = px.bar(df, x='class_name', y='pass_rate',
                                               title='各班级及格率分布',
                                               labels={'class_name': '班级', 'pass_rate': '及格率(%)'})
                                st.plotly_chart(fig_bar, use_container_width=True)
                                
                                # 饼图
                                fig_pie = px.pie(df, values='pass_rate', names='class_name',
                                               title='各班级及格率占比')
                                st.plotly_chart(fig_pie, use_container_width=True)
                                
                                # 热力图（如果有科目信息）
                                if 'subject_name' in df.columns:
                                    pivot_df = df.pivot(index='class_name', columns='subject_name', values='pass_rate')
                                    fig_heatmap = px.imshow(pivot_df, 
                                                          title='各班级科目及格率热力图',
                                                          labels=dict(x='科目', y='班级', color='及格率(%)'))
                                    st.plotly_chart(fig_heatmap, use_container_width=True)
                        
                        # 检查是否有排名信息
                        elif 'rank' in df.columns:
                            if 'student_name' in df.columns and 'subject_name' in df.columns:
                                # 成绩排名热力图
                                pivot_df = df.pivot(index='student_name', columns='subject_name', values='rank')
                                fig_heatmap = px.imshow(pivot_df, 
                                                      title='学生成绩排名热力图',
                                                      labels=dict(x='科目', y='学生', color='排名'))
                                st.plotly_chart(fig_heatmap, use_container_width=True)
                        
                        # 检查是否有进步情况
                        elif 'score_improvement' in df.columns:
                            if 'student_name' in df.columns:
                                fig_bar = px.bar(df, x='student_name', y='score_improvement',
                                               title='学生成绩进步情况',
                                               labels={'student_name': '学生', 'score_improvement': '进步幅度'})
                                st.plotly_chart(fig_bar, use_container_width=True)
                        
                        # 检查是否有成绩分布情况
                        elif all(col in df.columns for col in ['excellent', 'good', 'pass', 'fail']):
                            # 成绩分布堆叠柱状图
                            fig_bar = px.bar(df, x='subject_name', 
                                           y=['excellent', 'good', 'pass', 'fail'],
                                           title='各科目成绩分布情况',
                                           labels={'subject_name': '科目', 'value': '人数', 'variable': '等级'},
                                           barmode='stack')
                            st.plotly_chart(fig_bar, use_container_width=True)
                        
                        # 通用可视化选项
                        else:
                            if len(numeric_cols) > 0 and len(categorical_cols) > 0:
                                # 如果有数值列和分类列，创建柱状图
                                x_col = st.selectbox("选择X轴数据", categorical_cols, key="x_col")
                                y_col = st.selectbox("选择Y轴数据", numeric_cols, key="y_col")
                                
                                fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col}按{x_col}的分布")
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # 添加饼图选项
                                if len(categorical_cols) > 0:
                                    pie_col = st.selectbox("选择饼图数据", categorical_cols, key="pie_col")
                                    fig_pie = px.pie(df, names=pie_col, title=f"{pie_col}的分布")
                                    st.plotly_chart(fig_pie, use_container_width=True)
                                    
                            elif len(numeric_cols) > 1:
                                # 如果有多个数值列，创建散点图
                                x_num = st.selectbox("选择X轴数据", numeric_cols, key="x_num")
                                y_num = st.selectbox("选择Y轴数据", numeric_cols, key="y_num")
                                
                                fig = px.scatter(df, x=x_num, y=y_num, title=f"{y_num}与{x_num}的关系")
                                st.plotly_chart(fig, use_container_width=True)
                            
                            else:
                                st.info("当前数据不适合进行可视化，请尝试其他查询")
                    else:
                        st.warning("没有数据可供可视化")
                
            else:
                st.warning("查询没有返回结果")
                
        except Exception as e:
            st.error(f"发生错误: {str(e)}")
            st.error("请尝试修改查询或选择一个示例查询")

# 显示底部说明
st.markdown("---")
st.info("提示：尝试使用侧边栏中的示例查询，或使用自然语言描述您的查询需求") 