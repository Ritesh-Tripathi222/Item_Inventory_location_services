-- phpMyAdmin SQL Dump
-- version 4.8.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 30, 2021 at 07:45 PM
-- Server version: 10.1.32-MariaDB
-- PHP Version: 5.6.36

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_iteminvloc`
--

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE IF NOT EXISTS `inventory` (
  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `quantity` decimal(5,2) NOT NULL DEFAULT 0.00,
  `quantity_unit` varchar(20) NOT NULL DEFAULT '',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` int(11) NULL,
  `updated_by_role` varchar(20) NOT NULL DEFAULT '',
  `status_code` tinyint(4) NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `inventory_attribute_settings`
--

CREATE TABLE IF NOT EXISTS `inventory_attribute_settings` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL DEFAULT '',
  `code` char(5) NOT NULL DEFAULT '',
  `status_code` tinyint(4) NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `inventory_attribute_settings`
--

INSERT INTO `inventory_attribute_settings` (`id`, `name`, `code`, `status_code`) VALUES
(1, 'lot_no', 'LOTNO', 1),
(2, 'expiry_date', 'EXPDT', 1);

-- --------------------------------------------------------

--
-- Table structure for table `item`
--

CREATE TABLE IF NOT EXISTS `item` (
  `id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL DEFAULT '',
  `sku` varchar(20) NOT NULL DEFAULT '',
  `upc` varchar(20) NOT NULL DEFAULT '',
  `ean` varchar(20) NOT NULL DEFAULT '',
  `size` varchar(20) NOT NULL DEFAULT '',
  `barcode` varchar(20) NOT NULL DEFAULT '',
  `department` varchar(50) NOT NULL DEFAULT '',
  `item_class` varchar(50) NOT NULL DEFAULT '',
  `unit` varchar(20) NOT NULL DEFAULT '' ,
  `short_description` tinytext,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` int(11)  NULL,
  `updated_by_role` varchar(20) NOT NULL DEFAULT '',
  `status_code` tinyint(4)  NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `item`
--

-- --------------------------------------------------------

--
-- Table structure for table `item_detail`
--

CREATE TABLE IF NOT EXISTS `item_detail` (
  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `description` text,
  `lead_time` decimal(5,2) DEFAULT 0.00 NOT NULL,
  `lead_time_unit` varchar(20) NOT NULL DEFAULT '',
  `protection_level` varchar(20) NOT NULL DEFAULT '',
  `min_quantity` decimal(5,2) DEFAULT 0.00  NOT NULL,
  `channel_type` varchar(100) NOT NULL DEFAULT '',
  `is_dropship_only` enum('yes','no') NOT NULL DEFAULT 'yes',
  `shipping_restrictions` varchar(100) NOT NULL DEFAULT '',
  `delivery_method` varchar(30) NOT NULL DEFAULT '',
  `fulfillment_types` varchar(100) NOT NULL DEFAULT '',
  `shipping_service_level` varchar(20) NOT NULL DEFAULT '',
  `is_returnable` enum('yes','no') DEFAULT 'yes',
  `manufacturer` varchar(50) NOT NULL DEFAULT '',
  `vendor_name` varchar(50) NOT NULL DEFAULT '',
  `mpn` varchar(30) NOT NULL DEFAULT '',
  `isbn` varchar(30) NOT NULL DEFAULT '',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` int(11) NULL,
  `updated_by_role` varchar(30) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `item_purchase_info`
--

CREATE TABLE IF NOT EXISTS `item_purchase_info` (
  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `purchase_price_unit` char(3) NOT NULL DEFAULT '',
  `purchase_price` decimal(10,2) DEFAULT 0.00 NOT NULL,
  `purchase_account` varchar(30) NOT NULL DEFAULT '',
  `purchase_account_id` varchar(30) NOT NULL DEFAULT '',
  `purchase_description` varchar(100) NOT NULL DEFAULT '',
  `purchase_tax` decimal(5,2) DEFAULT 0.00 NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` int(11) NULL,
  `updated_by_role` varchar(20) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `item_selling_info`
--

CREATE TABLE IF NOT EXISTS `item_selling_info` (
  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `selling_price_unit` char(3) NOT NULL DEFAULT '',
  `selling_price` decimal(10,2) DEFAULT 0.00 NOT NULL,
  `selling_account` varchar(30) NOT NULL DEFAULT '',
  `selling_account_id` varchar(30) NOT NULL DEFAULT '',
  `sales_description` varchar(100) NOT NULL DEFAULT '',
  `sales_tax` decimal(5,2) DEFAULT 0.00 NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` int(11) NULL,
  `updated_by_role` varchar(20) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE IF NOT EXISTS `location` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL DEFAULT '',
  `ref_location_id` varchar(20) NOT NULL DEFAULT '',
  `location_type_id` int(11) NOT NULL,
  `timezone` varchar(50) NOT NULL DEFAULT '',
  `currency` char(3) NOT NULL DEFAULT 'USD',
  `payment_terms` varchar(30) NOT NULL DEFAULT '',
  `address1` varchar(100) NOT NULL DEFAULT '',
  `address2` varchar(100) NOT NULL DEFAULT '',
  `city` varchar(30) NOT NULL DEFAULT '',
  `state` varchar(30) NOT NULL DEFAULT '',
  `postal_code` varchar(10) NOT NULL DEFAULT '',
  `country_code` char(2) NOT NULL DEFAULT '',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_role` varchar(20) NOT NULL DEFAULT '',
  `updated_by_id` int(11) NULL,
  `status_code` tinyint(4) NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `location_contact_info`
--

CREATE TABLE IF NOT EXISTS `location_contact_info` (
  `id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `first_name` varchar(30) NOT NULL DEFAULT '',
  `last_name` varchar(30) NOT NULL DEFAULT '',
  `designation` varchar(30) NOT NULL DEFAULT '',
  `phone` varchar(30) NOT NULL DEFAULT '',
  `email` varchar(50) NOT NULL DEFAULT '',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_role` varchar(20) NOT NULL DEFAULT '',
  `updated_by_id` int(11) NULL,
  `status_code` tinyint(4) NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `location_receiving_info`
--

CREATE TABLE IF NOT EXISTS `location_receiving_info` (
  `id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `day` enum('sun','mon','tue','wed','thu','fri','sat') NOT NULL,
  `receiving_start_time` time NOT NULL,
  `receiving_end_time` time NOT NULL,
  `service_level_id` tinyint(4) NOT NULL,
  `carrier_last_pickup` time NOT NULL,
  `receiving_capacity` int(11) NOT NULL,
  `processing_time_unit` varchar(10) NOT NULL DEFAULT '',
  `processing_time` decimal(5,2) NOT NULL DEFAULT 0.00,
  `additional_info` tinytext NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_role` varchar(20) NOT NULL DEFAULT '',
  `updated_by_id` int(11) NULL,
  `status_code` tinyint(4) NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `location_shipping_info`
--

CREATE TABLE IF NOT EXISTS `location_shipping_info` (
  `id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `day` enum('sun','mon','tue','wed','thu','fri','sat') NOT NULL,
  `shipping_start_time` time NOT NULL,
  `shipping_end_time` time NOT NULL,
  `service_level_id` tinyint(4) NOT NULL,
  `carrier_last_pickup` time NOT NULL,
  `shipping_capacity` int(11) NOT NULL,
  `processing_time_unit` varchar(10) NOT NULL DEFAULT '',
  `processing_time` decimal(5,2) DEFAULT 0.00 NOT NULL,
  `additional_info` tinytext NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_role` varchar(20) NOT NULL DEFAULT '',
  `updated_by_id` int(11)  NULL,
  `status_code` tinyint(4) NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------
--
-- Table structure for table `inventory_attribute_info`
--
CREATE TABLE IF NOT EXISTS `inventory_attribute_info` (
  `id` int(11) NOT NULL,
  `inventory_id` int(11) NOT NULL,
  `inventory_attribute_id` int(11) NOT NULL,
  `inventory_attribute_value` varchar(100) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `location_types`
--

CREATE TABLE IF NOT EXISTS `location_types` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL DEFAULT '',
  `code` varchar(10) NOT NULL DEFAULT '',
  `status_code` tinyint(4) NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `location_types`
--

INSERT INTO `location_types` (`id`, `name`, `code`, `status_code`) VALUES
(1, 'Store', 'St', 1),
(2, 'Fulfillment Center', 'FC', 1),
(3, 'Cross Dock', 'CD', 1),
(4, 'Return Center', 'RC', 1),
(5, 'Vendor Facility', 'VF', 1),
(6, 'Hub', 'Hub', 1);

-- --------------------------------------------------------

--
-- Table structure for table `service_levels`
--

CREATE TABLE IF NOT EXISTS `service_levels` (
  `id` tinyint(4) NOT NULL,
  `name` varchar(20) NOT NULL DEFAULT '',
  `code` char(3) NOT NULL DEFAULT '',
  `status_code` tinyint(4) NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `service_levels`
--

INSERT INTO `service_levels` (`id`, `name`, `code`, `status_code`) VALUES
(1, 'Standard', 'std', 1),
(2, 'Expedited', 'exp', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventory_attribute_settings`
--
ALTER TABLE `inventory_attribute_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `item_detail`
--
ALTER TABLE `item_detail`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `item_purchase_info`
--
ALTER TABLE `item_purchase_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `item_selling_info`
--
ALTER TABLE `item_selling_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`id`);


--
-- Indexes for table `location_contact_info`
--
ALTER TABLE `location_contact_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `location_receiving_info`
--
ALTER TABLE `location_receiving_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `location_shipping_info`
--
ALTER TABLE `location_shipping_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `location_types`
--
ALTER TABLE `location_types`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `service_levels`
--
ALTER TABLE `service_levels`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `inventory_attribute_info`
--
ALTER TABLE `inventory_attribute_info`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inventory_attribute_settings`
--
ALTER TABLE `inventory_attribute_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `item`
--
ALTER TABLE `item`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `item_detail`
--
ALTER TABLE `item_detail`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `item_purchase_info`
--
ALTER TABLE `item_purchase_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `item_selling_info`
--
ALTER TABLE `item_selling_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `location`
--
ALTER TABLE `location`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `location_contact_info`
--
ALTER TABLE `location_contact_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `location_receiving_info`
--
ALTER TABLE `location_receiving_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `location_shipping_info`
--
ALTER TABLE `location_shipping_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `location_types`
--
ALTER TABLE `location_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `service_levels`
--
ALTER TABLE `service_levels`
  MODIFY `id` tinyint(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `inventory_attribute_info`
--
ALTER TABLE `inventory_attribute_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


COMMIT;



