# from vanna.vanna import VannaDefault
# from dotenv import load_dotenv
# import os
# load_dotenv()
# vn = VannaDefault(model="team_project")
# vn.connect_to_mysql(
#     host=os.getenv("DB_HOST"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     database=os.getenv("DB_NAME")
# )





from vanna_mysql_fix import DeepSeekVanna

# 初始化
text2sql = DeepSeekVanna()

# 训练数据库结构 - 从llmauto.sql中提取的表结构
# 班级表
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

# 生成并执行SQL
question = "查询入学时间在2023年以前的学生"
try:
    generated_sql = text2sql.generate_sql(question)
    print(f"生成的SQL: {generated_sql}")

    results = text2sql.execute_sql(generated_sql)
    print(f"查询结果: {results}")
except Exception as e:
    print(f"操作失败：{str(e)}")

# 尝试一个复杂点的查询
question2 = "查询数学成绩超过90分的学生及其班级"
try:
    generated_sql2 = text2sql.generate_sql(question2)
    print(f"\n新查询问题: {question2}")
    print(f"生成的SQL: {generated_sql2}")

    results2 = text2sql.execute_sql(generated_sql2)
    print(f"查询结果: {results2}")
except Exception as e:
    print(f"操作失败：{str(e)}")

# 尝试一个使用视图的查询
question3 = "查询高二年级数学成绩的学生信息"
try:
    generated_sql3 = text2sql.generate_sql(question3)
    print(f"\n新查询问题: {question3}")
    print(f"生成的SQL: {generated_sql3}")

    results3 = text2sql.execute_sql(generated_sql3)
    print(f"查询结果: {results3}")
except Exception as e:
    print(f"操作失败：{str(e)}")