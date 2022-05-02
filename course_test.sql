-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2022 年 05 月 02 日 17:19
-- 伺服器版本： 10.4.19-MariaDB
-- PHP 版本： 8.0.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `course_test`
--

-- --------------------------------------------------------

--
-- 資料表結構 `Course`
--

CREATE TABLE `Course` (
  `CourseID` int(5) UNSIGNED NOT NULL,
  `CourseName` char(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `CourseCredit` int(3) UNSIGNED NOT NULL,
  `CourseDesc` char(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CourseType` char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `DepartmentID` char(4) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `Department`
--

CREATE TABLE `Department` (
  `DepartmentID` char(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `DepartmentName` char(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `DepartmentDesc` char(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `Focus`
--

CREATE TABLE `Focus` (
  `SectionID` int(5) UNSIGNED NOT NULL,
  `StudentID` char(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Year` int(3) UNSIGNED NOT NULL,
  `Semester` int(1) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `Section`
--

CREATE TABLE `Section` (
  `SectionID` int(5) UNSIGNED NOT NULL,
  `Year` int(3) UNSIGNED NOT NULL,
  `Semester` int(1) UNSIGNED NOT NULL,
  `CourseID` int(5) UNSIGNED NOT NULL,
  `SectionCapacity` int(3) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `SectionAt`
--

CREATE TABLE `SectionAt` (
  `SectionID` int(5) UNSIGNED NOT NULL,
  `TimeID` int(2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `Student`
--

CREATE TABLE `Student` (
  `StudentID` char(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `StudentName` char(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `StudentGender` int(1) UNSIGNED NOT NULL DEFAULT 0,
  `DepartmentID` char(5) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `Takes`
--

CREATE TABLE `Takes` (
  `SectionID` int(5) UNSIGNED NOT NULL,
  `StudentID` char(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Year` int(3) UNSIGNED NOT NULL,
  `Semester` int(1) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `Teacher`
--

CREATE TABLE `Teacher` (
  `TeacherID` char(7) COLLATE utf8mb4_unicode_ci NOT NULL,
  `TeacherName` char(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `TeacherGender` int(1) UNSIGNED NOT NULL DEFAULT 0,
  `DepartmentID` char(5) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `Teaches`
--

CREATE TABLE `Teaches` (
  `TeacherID` char(7) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SectionID` int(5) UNSIGNED NOT NULL,
  `Year` int(3) UNSIGNED NOT NULL,
  `Semester` int(1) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `Time`
--

CREATE TABLE `Time` (
  `TimeID` int(2) UNSIGNED NOT NULL,
  `Day` int(1) NOT NULL,
  `Session` int(2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `User`
--

CREATE TABLE `User` (
  `StudentID` char(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Password` char(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `Course`
--
ALTER TABLE `Course`
  ADD PRIMARY KEY (`CourseID`),
  ADD KEY `course_which_department` (`DepartmentID`);

--
-- 資料表索引 `Department`
--
ALTER TABLE `Department`
  ADD PRIMARY KEY (`DepartmentID`);

--
-- 資料表索引 `Focus`
--
ALTER TABLE `Focus`
  ADD PRIMARY KEY (`SectionID`);

--
-- 資料表索引 `Section`
--
ALTER TABLE `Section`
  ADD PRIMARY KEY (`SectionID`,`Semester`,`Year`),
  ADD KEY `section_which_course` (`CourseID`);

--
-- 資料表索引 `SectionAt`
--
ALTER TABLE `SectionAt`
  ADD PRIMARY KEY (`SectionID`,`TimeID`),
  ADD KEY `sectionAt_which_time` (`TimeID`);

--
-- 資料表索引 `Student`
--
ALTER TABLE `Student`
  ADD PRIMARY KEY (`StudentID`),
  ADD KEY `student_which_department` (`DepartmentID`);

--
-- 資料表索引 `Takes`
--
ALTER TABLE `Takes`
  ADD PRIMARY KEY (`SectionID`,`StudentID`,`Semester`,`Year`),
  ADD KEY `takes_which_student` (`StudentID`),
  ADD KEY `takes_which_section` (`SectionID`,`Semester`,`Year`);

--
-- 資料表索引 `Teacher`
--
ALTER TABLE `Teacher`
  ADD PRIMARY KEY (`TeacherID`),
  ADD KEY `teacher_which_department` (`DepartmentID`);

--
-- 資料表索引 `Teaches`
--
ALTER TABLE `Teaches`
  ADD PRIMARY KEY (`TeacherID`,`SectionID`,`Semester`,`Year`),
  ADD KEY `teaches_which_section` (`SectionID`,`Semester`,`Year`);

--
-- 資料表索引 `Time`
--
ALTER TABLE `Time`
  ADD PRIMARY KEY (`TimeID`);

--
-- 資料表索引 `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`StudentID`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `Course`
--
ALTER TABLE `Course`
  MODIFY `CourseID` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `Time`
--
ALTER TABLE `Time`
  MODIFY `TimeID` int(2) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `Course`
--
ALTER TABLE `Course`
  ADD CONSTRAINT `course_which_department` FOREIGN KEY (`DepartmentID`) REFERENCES `Department` (`DepartmentID`);

--
-- 資料表的限制式 `Section`
--
ALTER TABLE `Section`
  ADD CONSTRAINT `section_which_course` FOREIGN KEY (`CourseID`) REFERENCES `Course` (`CourseID`);

--
-- 資料表的限制式 `SectionAt`
--
ALTER TABLE `SectionAt`
  ADD CONSTRAINT `sectionAt_which_section` FOREIGN KEY (`SectionID`) REFERENCES `Section` (`SectionID`),
  ADD CONSTRAINT `sectionAt_which_time` FOREIGN KEY (`TimeID`) REFERENCES `Time` (`TimeID`);

--
-- 資料表的限制式 `Student`
--
ALTER TABLE `Student`
  ADD CONSTRAINT `student_which_department` FOREIGN KEY (`DepartmentID`) REFERENCES `Department` (`DepartmentID`);

--
-- 資料表的限制式 `Takes`
--
ALTER TABLE `Takes`
  ADD CONSTRAINT `takes_which_section` FOREIGN KEY (`SectionID`,`Semester`,`Year`) REFERENCES `Section` (`SectionID`, `Semester`, `Year`),
  ADD CONSTRAINT `takes_which_student` FOREIGN KEY (`StudentID`) REFERENCES `Student` (`StudentID`);

--
-- 資料表的限制式 `Teacher`
--
ALTER TABLE `Teacher`
  ADD CONSTRAINT `teacher_which_department` FOREIGN KEY (`DepartmentID`) REFERENCES `Department` (`DepartmentID`);

--
-- 資料表的限制式 `Teaches`
--
ALTER TABLE `Teaches`
  ADD CONSTRAINT `teaches_which_section` FOREIGN KEY (`SectionID`,`Semester`,`Year`) REFERENCES `Section` (`SectionID`, `Semester`, `Year`),
  ADD CONSTRAINT `teaches_which_teacher` FOREIGN KEY (`TeacherID`) REFERENCES `Teacher` (`TeacherID`);

--
-- 資料表的限制式 `User`
--
ALTER TABLE `User`
  ADD CONSTRAINT `user_which_student` FOREIGN KEY (`StudentID`) REFERENCES `Student` (`StudentID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
