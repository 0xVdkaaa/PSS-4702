-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 07, 2013 at 02:40 
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `mvc`
--
CREATE DATABASE `mvc` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `mvc`;

-- --------------------------------------------------------

--
-- Table structure for table `mahasiswa`
--

CREATE TABLE IF NOT EXISTS `mahasiswa` (
  `nim` varchar(7) NOT NULL DEFAULT '',
  `nama` varchar(100) NOT NULL,
  `angkatan` varchar(10) NOT NULL,
  `fakultas` varchar(100) NOT NULL,
  `program` varchar(100) NOT NULL,
  PRIMARY KEY (`nim`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `mahasiswa`
--

INSERT INTO `mahasiswa` (`nim`, `nama`, `angkatan`, `fakultas`, `program`) VALUES
('1101234', 'Eva Nursamsi', '2011', 'Pendidikan Matematika dan Pengetahuan Alam', 'Ilmu Komputer - S1'),
('1102345', 'Sinta Laura', '2011', 'Pendidikan Matematika dan Pengetahuan Alam', 'Pendidikan Ilmu Komputer - S1'),
('1103456', 'Madun Ginanjar', '2011', 'Pendidikan Matematika dan Pengetahuan Alam', 'Pendidikan Ilmu Komputer - S1'),
('1201234', 'Zainal Abidin', '2009', 'Pendidikan Matematika dan Pengetahuan Alam', 'Pendidikan Ilmu Komputer - S1'),
('1202345', 'Surip Andri', '2009', 'Pendidikan Matematika dan Pengetahuan Alam', 'Ilmu Komputer - S1'),
('1203456', 'Ani Suryani', '2009', 'Pendidikan Matematika dan Pengetahuan Alam', 'Pendidikan Ilmu Komputer - S1');
