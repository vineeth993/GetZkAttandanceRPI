-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 02, 2018 at 06:55 PM
-- Server version: 5.7.23-0ubuntu0.16.04.1
-- PHP Version: 7.0.30-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `zkAttendance`
--
CREATE DATABASE IF NOT EXISTS `zkAttendance` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `zkAttendance`;

-- --------------------------------------------------------

--
-- Table structure for table `Attandance`
--

DROP TABLE IF EXISTS `Attandance`;
CREATE TABLE `Attandance` (
  `id` int(11) NOT NULL,
  `EmpId` varchar(200) NOT NULL,
  `DateTime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `AttandanceParam`
--

DROP TABLE IF EXISTS `AttandanceParam`;
CREATE TABLE `AttandanceParam` (
  `id` int(11) NOT NULL,
  `lastDateTime` datetime NOT NULL,
  `InitalTime` time NOT NULL,
  `FinalTime` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `SystemParam`
--

DROP TABLE IF EXISTS `SystemParam`;
CREATE TABLE `SystemParam` (
  `ErpConn` varchar(250) NOT NULL,
  `ErpUser` varchar(250) NOT NULL,
  `ErpPasscode` varchar(250) NOT NULL,
  `ErpDB` varchar(250) NOT NULL,
  `DevIp` varchar(100) NOT NULL,
  `DevPort` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Attandance`
--
ALTER TABLE `Attandance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `AttandanceParam`
--
ALTER TABLE `AttandanceParam`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Attandance`
--
ALTER TABLE `Attandance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32552;
--
-- AUTO_INCREMENT for table `AttandanceParam`
--
ALTER TABLE `AttandanceParam`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
