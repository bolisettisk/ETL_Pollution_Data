
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


--
-- Database: `pollution-db`
--

-- --------------------------------------------------------

--
-- Table structure for table `reading`
--

CREATE TABLE `reading` (
  `MeasurementID` int(11) NOT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Time Offset` time DEFAULT NULL,
  `NOx` decimal(14,8) DEFAULT NULL,
  `NO2` decimal(14,8) DEFAULT NULL,
  `NO` decimal(14,8) DEFAULT NULL,
  `PM10` decimal(14,8) DEFAULT NULL,
  `NVPM10` decimal(14,8) DEFAULT NULL,
  `VPM10` decimal(14,8) DEFAULT NULL,
  `NVPM2.5` decimal(14,8) DEFAULT NULL,
  `PM2.5` decimal(14,8) DEFAULT NULL,
  `VPM2.5` decimal(14,8) DEFAULT NULL,
  `CO` decimal(14,8) DEFAULT NULL,
  `O3` decimal(14,8) DEFAULT NULL,
  `SO2` decimal(14,8) DEFAULT NULL,
  `Temperature` decimal(14,8) DEFAULT NULL,
  `RH` decimal(14,8) DEFAULT NULL,
  `Air Pressure` decimal(14,8) DEFAULT NULL,
  `DateStart` date DEFAULT NULL,
  `TimeStart` time DEFAULT NULL,
  `TimeStart Offset` time DEFAULT NULL,
  `DateEnd` date DEFAULT NULL,
  `TimeEnd` time DEFAULT NULL,
  `TimeEnd Offset` time DEFAULT NULL,
  `Current` varchar(6) DEFAULT NULL,
  `Instrument Type` varchar(128) DEFAULT NULL,
  `SiteID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `schema`
--

CREATE TABLE `schema` (
  `SchemaID` int(11) NOT NULL,
  `Measure` varchar(128) NOT NULL,
  `Description` varchar(512) NOT NULL,
  `Unit` varchar(12) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `site`
--

CREATE TABLE `site` (
  `SiteID` int(11) NOT NULL,
  `Location` varchar(128) NOT NULL,
  `Latitude` decimal(18,16) DEFAULT NULL,
  `Longitude` decimal(19,16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `reading`
--
ALTER TABLE `reading`
  ADD PRIMARY KEY (`MeasurementID`),
  ADD KEY `fk_Reading_Site_idx` (`SiteID`);

--
-- Indexes for table `schema`
--
ALTER TABLE `schema`
  ADD PRIMARY KEY (`SchemaID`);

--
-- Indexes for table `site`
--
ALTER TABLE `site`
  ADD PRIMARY KEY (`SiteID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `reading`
--
ALTER TABLE `reading`
  MODIFY `MeasurementID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `schema`
--
ALTER TABLE `schema`
  MODIFY `SchemaID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reading`
--
ALTER TABLE `reading`
  ADD CONSTRAINT `fk_Reading_Site` FOREIGN KEY (`SiteID`) REFERENCES `site` (`SiteID`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;


