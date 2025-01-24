-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 24, 2025 at 11:47 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fraud_detector_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `emails`
--

CREATE TABLE `emails` (
  `id` int(11) NOT NULL,
  `email_address` varchar(255) DEFAULT NULL,
  `email_content` text NOT NULL,
  `isSpam` int(11) NOT NULL,
  `date_created` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `emails`
--

INSERT INTO `emails` (`id`, `email_address`, `email_content`, `isSpam`, `date_created`) VALUES
(1, 'offer999@bestdeal.com', 'Congratulations! You\'ve been selected for a special offer. Claim your $1000 gift card now! Click here to claim your prize.', 1, '2025-01-24 17:54:42'),
(2, 'winbignow@cashprizes.com', 'You\'ve just won $5000! To claim your winnings, respond with your bank details immediately.', 1, '2025-01-24 17:54:51'),
(3, 'support@secure-login.com', 'Your account has been flagged for unusual activity. Please verify your information immediately to prevent suspension.', 1, '2025-01-24 17:54:59'),
(4, 'info@randompromos.com', 'Get 50% off on your next purchase. Hurry, this offer ends soon! Use code: SAVE50 at checkout.', 1, '2025-01-24 17:55:11'),
(5, 'service@vacinetrials.com', 'We are offering free COVID-19 vaccine trials. Sign up now to receive your dose for free.', 1, '2025-01-24 17:55:20'),
(6, '', 'You\'ve earned a $1000 reward! Simply click the link below to verify your identity and receive your funds.', 1, '2025-01-24 17:55:27'),
(7, 'john.doe@example.com', 'I hope you\'re doing well. I\'d like to schedule a meeting to discuss the upcoming Q1 project. Please let me know your availability.\nBest regards,\nJohn Doe', 0, '2025-01-24 17:55:59'),
(8, 'jane.smith@company.com', 'Dear Team,\nPlease find attached the updated marketing plan for the upcoming year. Let me know if you have any questions or suggestions.\nBest,\nJane Smith', 0, '2025-01-24 17:56:09'),
(9, 'support@techsupport.com', ' Hello Darwin,\nThank you for reaching out. We’ve reviewed your issue with the software, and we suggest reinstalling the application to resolve the problem. Please let us know if you need further assistance.\nSincerely,\nTech Support Team', 0, '2025-01-24 17:56:21'),
(10, 'info@travelagency.com', 'Hi James,\nYour vacation itinerary for the trip to Bali has been confirmed. Please find the details below:\n\nDeparture:\nDate: February 15, 2025\nFlight: XYZ Airlines, Flight #123\nDeparture Time: 10:00 AM (JFK Airport)\nArrival Time: 11:30 PM (Ngurah Rai International Airport)\n\nReturn:\nDate: February 22, 2025\nFlight: XYZ Airlines, Flight #456\nDeparture Time: 2:00 PM (Ngurah Rai International Airport)\nArrival Time: 9:00 PM (JFK Airport)\n\nWe hope you have a wonderful trip!\nBest regards,\nTravel Agency Team', 0, '2025-01-24 17:57:18'),
(11, 'laura.white@university.edu', 'Dear user,\nWe are pleased to inform you that your research grant application has been approved. Please check the attached document for the next steps.\nBest regards,\nLaura White\nResearch Department', 0, '2025-01-24 17:57:33'),
(12, 'info@makebigmoneyonline.com', 'Learn how to make $1000 every day from the comfort of your home. Join now for exclusive tips and tricks.', 1, '2025-01-24 17:57:49'),
(13, 'helpdesk@fraudalert.com', 'Your account may have been compromised. Click here to secure your account immediately.', 1, '2025-01-24 17:57:56');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `id` int(11) NOT NULL,
  `login_code` varchar(6) NOT NULL,
  `date_expiry` datetime NOT NULL,
  `date_created` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`id`, `login_code`, `date_expiry`, `date_created`) VALUES
(1, '850086', '2025-01-20 01:29:21', '2025-01-20 01:24:21'),
(2, '764412', '2025-01-20 01:35:35', '2025-01-20 01:30:35'),
(3, '993578', '2025-01-24 14:24:05', '2025-01-24 14:19:05'),
(4, '787469', '2025-01-24 14:31:33', '2025-01-24 14:26:33'),
(5, '528774', '2025-01-24 14:41:02', '2025-01-24 14:36:02'),
(6, '239198', '2025-01-24 14:53:09', '2025-01-24 14:48:09'),
(7, '574270', '2025-01-24 15:02:44', '2025-01-24 14:57:44'),
(8, '751688', '2025-01-24 15:08:54', '2025-01-24 15:03:54'),
(9, '479112', '2025-01-24 15:17:06', '2025-01-24 15:12:06'),
(10, '340105', '2025-01-24 17:04:28', '2025-01-24 16:59:28'),
(11, '187343', '2025-01-24 17:21:51', '2025-01-24 17:16:51'),
(12, '384044', '2025-01-24 17:35:25', '2025-01-24 17:30:25'),
(13, '470011', '2025-01-24 17:41:53', '2025-01-24 17:36:53'),
(14, '650110', '2025-01-24 17:51:47', '2025-01-24 17:46:47'),
(15, '809769', '2025-01-24 17:57:21', '2025-01-24 17:52:21'),
(16, '996120', '2025-01-24 18:03:19', '2025-01-24 17:58:19');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `emails`
--
ALTER TABLE `emails`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `emails`
--
ALTER TABLE `emails`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
