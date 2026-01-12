-- 学生成绩管理系统数据库初始化脚本
-- 运行方式: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS student_management_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE student_management_system;

-- ==========================================
-- 表结构: 学生表 (students)
-- ==========================================
CREATE TABLE IF NOT EXISTS `students` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `student_id` VARCHAR(20) NOT NULL UNIQUE COMMENT '学号',
  `name` VARCHAR(50) NOT NULL COMMENT '姓名',
  `class_name` VARCHAR(50) NOT NULL COMMENT '班级',
  `gender` ENUM('男', '女') DEFAULT NULL COMMENT '性别',
  `age` INT DEFAULT NULL COMMENT '年龄',
  `phone` VARCHAR(20) DEFAULT NULL COMMENT '联系电话',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '电子邮箱',
  `address` TEXT DEFAULT NULL COMMENT '家庭住址',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生信息表';

-- ==========================================
-- 表结构: 成绩表 (grades)
-- ==========================================
CREATE TABLE IF NOT EXISTS `grades` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `student_id` VARCHAR(20) NOT NULL COMMENT '学号 (关联 students.student_id)',
  `subject` VARCHAR(50) NOT NULL COMMENT '科目',
  `score` DECIMAL(5, 2) NOT NULL COMMENT '分数',
  `exam_type` VARCHAR(50) DEFAULT '期末考试' COMMENT '考试类型',
  `exam_date` DATE DEFAULT NULL COMMENT '考试日期',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
  -- 外键约束 (可选，视需求而定)
  CONSTRAINT `fk_student_id` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生成绩表';

-- ==========================================
-- 示例数据
-- ==========================================
INSERT INTO `students` (`student_id`, `name`, `class_name`, `gender`, `age`, `phone`) VALUES
('2024001', '张三', '计算机一班', '男', 20, '13800138000'),
('2024002', '李四', '计算机一班', '女', 19, '13900139000'),
('2024003', '王五', '软件二班', '男', 21, '13700137000');

INSERT INTO `grades` (`student_id`, `subject`, `score`, `exam_type`, `exam_date`) VALUES
('2024001', '高等数学', 85.5, '期末考试', '2024-01-15'),
('2024001', '大学英语', 78.0, '期末考试', '2024-01-16'),
('2024002', '高等数学', 92.0, '期末考试', '2024-01-15'),
('2024003', 'Java程序设计', 88.5, '期末考试', '2024-01-17');
