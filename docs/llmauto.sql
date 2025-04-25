-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- 主机： 152.136.150.40
-- 生成日期： 2025-04-12 09:19:23
-- 服务器版本： 11.6.2-MariaDB-ubu2404
-- PHP 版本： 8.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `llmauto`
--

-- --------------------------------------------------------

--
-- 表的结构 `classes`
--

CREATE TABLE `classes` (
  `class_id` int(11) NOT NULL,
  `grade_level` enum('高一','高二','高三') NOT NULL,
  `class_name` varchar(20) NOT NULL,
  `homeroom_teacher_id` int(11) DEFAULT NULL,
  `student_count` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- 转存表中的数据 `classes`
--

INSERT INTO `classes` (`class_id`, `grade_level`, `class_name`, `homeroom_teacher_id`, `student_count`) VALUES
(1, '高一', '高一(1)班', 1, 45),
(2, '高一', '高一(2)班', 2, 46),
(3, '高一', '高一(3)班', 3, 44),
(4, '高二', '高二(1)班', 4, 42),
(5, '高二', '高二(2)班', 5, 43),
(6, '高二', '高二(3)班', 6, 45),
(7, '高三', '高三(1)班', 7, 40),
(8, '高三', '高三(2)班', 8, 41),
(9, '高三', '高三(3)班', 9, 42);

-- --------------------------------------------------------

--
-- 替换视图以便查看 `grade_scores`
-- （参见下面的实际视图）
--
CREATE TABLE `grade_scores` (
`grade_level` enum('高一','高二','高三')
,`class_name` varchar(20)
,`student_name` varchar(50)
,`subject_name` varchar(20)
,`score` decimal(5,2)
,`homeroom_teacher` varchar(50)
);

-- --------------------------------------------------------

--
-- 表的结构 `scores`
--

CREATE TABLE `scores` (
  `score_id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  `score` decimal(5,2) DEFAULT NULL,
  `exam_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- 转存表中的数据 `scores`
--

INSERT INTO `scores` (`score_id`, `student_id`, `subject_id`, `score`, `exam_date`) VALUES
(1, 1, 1, 88.50, '2023-12-20'),
(2, 1, 2, 92.00, '2023-12-20'),
(3, 1, 3, 85.50, '2023-12-20'),
(4, 2, 1, 90.00, '2023-12-20'),
(5, 2, 2, 88.50, '2023-12-20'),
(6, 2, 3, 94.00, '2023-12-20'),
(7, 10, 1, 87.50, '2023-12-20'),
(8, 10, 2, 91.00, '2023-12-20'),
(9, 10, 3, 89.50, '2023-12-20'),
(10, 11, 1, 86.00, '2023-12-20'),
(11, 11, 2, 93.50, '2023-12-20'),
(12, 11, 3, 88.00, '2023-12-20'),
(13, 19, 1, 89.00, '2023-12-20'),
(14, 19, 2, 94.50, '2023-12-20'),
(15, 19, 3, 92.00, '2023-12-20'),
(16, 20, 1, 91.50, '2023-12-20'),
(17, 20, 2, 90.00, '2023-12-20'),
(18, 20, 3, 93.50, '2023-12-20');

-- --------------------------------------------------------

--
-- 表的结构 `students`
--

CREATE TABLE `students` (
  `student_id` int(11) NOT NULL,
  `student_name` varchar(50) NOT NULL,
  `class_id` int(11) DEFAULT NULL,
  `admission_year` year(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- 转存表中的数据 `students`
--

INSERT INTO `students` (`student_id`, `student_name`, `class_id`, `admission_year`) VALUES
(1, '张小明', 1, '2023'),
(2, '李小红', 1, '2023'),
(3, '王小军', 1, '2023'),
(4, '赵小华', 2, '2023'),
(5, '刘小燕', 2, '2023'),
(6, '陈小伟', 2, '2023'),
(7, '钱小林', 3, '2023'),
(8, '孙小梅', 3, '2023'),
(9, '周小杰', 3, '2023'),
(10, '张华', 4, '2022'),
(11, '李明', 4, '2022'),
(12, '王芳', 4, '2022'),
(13, '赵强', 5, '2022'),
(14, '刘洋', 5, '2022'),
(15, '陈静', 5, '2022'),
(16, '钱亮', 6, '2022'),
(17, '孙颖', 6, '2022'),
(18, '周涛', 6, '2022'),
(19, '张伟', 7, '2021'),
(20, '李娟', 7, '2021'),
(21, '王刚', 7, '2021'),
(22, '赵敏', 8, '2021'),
(23, '刘波', 8, '2021'),
(24, '陈霞', 8, '2021'),
(25, '钱军', 9, '2021'),
(26, '孙莉', 9, '2021'),
(27, '周磊', 9, '2021');

-- --------------------------------------------------------

--
-- 表的结构 `subjects`
--

CREATE TABLE `subjects` (
  `subject_id` int(11) NOT NULL,
  `subject_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- 转存表中的数据 `subjects`
--

INSERT INTO `subjects` (`subject_id`, `subject_name`) VALUES
(1, '语文'),
(2, '数学'),
(3, '英语'),
(4, '物理'),
(5, '化学'),
(6, '生物'),
(7, '政治'),
(8, '历史'),
(9, '地理');

-- --------------------------------------------------------

--
-- 表的结构 `teachers`
--

CREATE TABLE `teachers` (
  `teacher_id` int(11) NOT NULL,
  `teacher_name` varchar(50) NOT NULL,
  `contact_number` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- 转存表中的数据 `teachers`
--

INSERT INTO `teachers` (`teacher_id`, `teacher_name`, `contact_number`) VALUES
(1, '张明', '13800138001'),
(2, '李芳', '13800138002'),
(3, '王强', '13800138003'),
(4, '刘婷', '13800138004'),
(5, '陈伟', '13800138005'),
(6, '赵丽', '13800138006'),
(7, '钱峰', '13800138007'),
(8, '孙华', '13800138008'),
(9, '周红', '13800138009');

--
-- 转储表的索引
--

--
-- 表的索引 `classes`
--
ALTER TABLE `classes`
  ADD PRIMARY KEY (`class_id`),
  ADD KEY `homeroom_teacher_id` (`homeroom_teacher_id`);

--
-- 表的索引 `scores`
--
ALTER TABLE `scores`
  ADD PRIMARY KEY (`score_id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `subject_id` (`subject_id`);

--
-- 表的索引 `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`student_id`),
  ADD KEY `class_id` (`class_id`);

--
-- 表的索引 `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`subject_id`);

--
-- 表的索引 `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`teacher_id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `classes`
--
ALTER TABLE `classes`
  MODIFY `class_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- 使用表AUTO_INCREMENT `scores`
--
ALTER TABLE `scores`
  MODIFY `score_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- 使用表AUTO_INCREMENT `students`
--
ALTER TABLE `students`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- 使用表AUTO_INCREMENT `subjects`
--
ALTER TABLE `subjects`
  MODIFY `subject_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- 使用表AUTO_INCREMENT `teachers`
--
ALTER TABLE `teachers`
  MODIFY `teacher_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

-- --------------------------------------------------------

--
-- 视图结构 `grade_scores`
--
DROP TABLE IF EXISTS `grade_scores`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `grade_scores`  AS SELECT `c`.`grade_level` AS `grade_level`, `c`.`class_name` AS `class_name`, `s`.`student_name` AS `student_name`, `sub`.`subject_name` AS `subject_name`, `sc`.`score` AS `score`, `t`.`teacher_name` AS `homeroom_teacher` FROM ((((`scores` `sc` join `students` `s` on(`s`.`student_id` = `sc`.`student_id`)) join `classes` `c` on(`c`.`class_id` = `s`.`class_id`)) join `subjects` `sub` on(`sub`.`subject_id` = `sc`.`subject_id`)) join `teachers` `t` on(`t`.`teacher_id` = `c`.`homeroom_teacher_id`)) ;

--
-- 限制导出的表
--

--
-- 限制表 `classes`
--
ALTER TABLE `classes`
  ADD CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`homeroom_teacher_id`) REFERENCES `teachers` (`teacher_id`);

--
-- 限制表 `scores`
--
ALTER TABLE `scores`
  ADD CONSTRAINT `scores_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  ADD CONSTRAINT `scores_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`);

--
-- 限制表 `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;