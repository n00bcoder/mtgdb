-- phpMyAdmin SQL Dump
-- version 4.0.4.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Feb 26, 2014 at 06:19 AM
-- Server version: 5.6.11
-- PHP Version: 5.5.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `mtgdb`
--
CREATE DATABASE IF NOT EXISTS `mtgdb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `mtgdb`;

-- --------------------------------------------------------

--
-- Table structure for table `cards`
--

CREATE TABLE IF NOT EXISTS `cards` (
  `id` int(10) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `castingCost` varchar(10) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `subtype` varchar(40) DEFAULT NULL,
  `text` varchar(2000) DEFAULT NULL,
  `cardset` varchar(40) DEFAULT NULL,
  `rarity` varchar(5) DEFAULT NULL,
  `pt` varchar(10) DEFAULT NULL,
  `card_number` varchar(10) NOT NULL,
  `qty` int(3) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `cardset`
--

CREATE TABLE IF NOT EXISTS `cardset` (
  `id` int(4) NOT NULL,
  `cardset` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `cardstest`
--

CREATE TABLE IF NOT EXISTS `cardstest` (
  `id` int(10) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `castingCost` varchar(10) DEFAULT NULL,
  `type` varchar(30) DEFAULT NULL,
  `subtype` varchar(40) DEFAULT NULL,
  `text` varchar(2000) DEFAULT NULL,
  `cardset` varchar(40) DEFAULT NULL,
  `rarity` varchar(5) DEFAULT NULL,
  `pt` varchar(10) DEFAULT NULL,
  `card_number` varchar(10) NOT NULL,
  `qty` int(3) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `cardtype`
--

CREATE TABLE IF NOT EXISTS `cardtype` (
  `id` int(5) NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `rarity`
--

CREATE TABLE IF NOT EXISTS `rarity` (
  `id` int(2) NOT NULL,
  `rarity` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
