-- MySQL dump 10.13  Distrib 5.7.32, for Linux (x86_64)
--
-- Host: localhost    Database: solar_panel
-- ------------------------------------------------------
-- Server version	5.7.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_catagory`
--

DROP TABLE IF EXISTS `account_catagory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_catagory` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` text,
  `addedon` date DEFAULT NULL,
  `type` text,
  `super_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_catagory`
--

LOCK TABLES `account_catagory` WRITE;
/*!40000 ALTER TABLE `account_catagory` DISABLE KEYS */;
INSERT INTO `account_catagory` VALUES (1,'TRAVEL','2020-11-18','expense',5),(2,'FOOD','2020-11-18','expense',5),(3,'FUEL','2020-11-18','expense',5);
/*!40000 ALTER TABLE `account_catagory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` text,
  `admin` bigint(20) DEFAULT NULL,
  `description` text,
  `account_cat` bigint(20) DEFAULT NULL,
  `date_added` date DEFAULT NULL,
  `status` text,
  `edited_on` date DEFAULT NULL,
  `approved_by` text,
  `attachment` text,
  `remarks` text,
  `admin_id` bigint(20) NOT NULL,
  `amount` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,'madurai to tirupuvanam',1,'plant visit',1,'2020-11-18','Submitted',NULL,NULL,'null','',5,500);
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` text,
  `addedon` date DEFAULT NULL,
  `username` char(128) DEFAULT NULL,
  `password` char(128) DEFAULT NULL,
  `location` text,
  `status` text,
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `address` text,
  `lat_lon` text,
  `super_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'TIRUPUVANAM PLANT','2020-11-18','admin@tpt.com','20960bf59e4a48ff7acf23e05912f2b41a90e56c675dc6d0bd85ee769f8d3113f34a0f1d74804e5c145e76ec0cd83e02b1470d531f251ab7ab8f61f5bd2ee364','Madurai','active','2020-11-18 10:08:19','','',5),(2,'testadmin','2020-11-18','testadmin@gmail.com','252f3ed9284cc2ca19d4866b57cdd7b43816034f4a4f07cb1ec3e8b59f584ee233796e3ce6a0f4ec7ef0b73460c8e7483096d9761329f1b37556bea36f19561b','madurai','active','2020-11-18 13:03:28','madurai','22',4),(3,'admin2','2020-11-19','admin2@gmail.com','fd978b82af281deaff5d1fe609c3235c2e39b5e19d4326875ef7f135382f60b5da1423acfb37ddf3ad58071a9384aa0989efe926785a30ef7818b3c6b189f5fb','mdu','active','2020-11-19 04:38:15','mdu','22',4),(4,'test','2020-11-20','testadmin','f2b08a609eefe6c83e34d9fc348932cff7d877c2ccb52cb3f17dd2ee4139d63917397a24fd4f6a9f2f1d891ec97184329a44dec95adc78c50ed82d1e72af89bd','madurai','active','2020-11-20 13:04:55','test','123',4),(5,'j','2020-11-20','testadmin2','f2b08a609eefe6c83e34d9fc348932cff7d877c2ccb52cb3f17dd2ee4139d63917397a24fd4f6a9f2f1d891ec97184329a44dec95adc78c50ed82d1e72af89bd','w','active','2020-11-20 13:04:55','w','',4),(6,'kani','2020-11-20','kani1@gmail.com','9d1e86a66f780e37c7aee3a4e967337e6585cf0cfebd9cb4113aba96c638307fce8b363d382bed2861a9efeebaddd018564c3e6966fa18bc5553a0ae12acb846','mdu','active','2020-11-20 13:08:21','mdu','11',4),(7,'admin','2020-11-22','admin1','8b41b3fe80ea3d95a271e23e9016b20c22e35d5b9e24f353ffeb9b69baa4747a5c1955c8bd699e8f937c8eecc770f134d1f70e1a6e583e7105aff634b746f373','mdu','active','2020-11-22 03:27:11','mdu','11',4);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_group`
--

DROP TABLE IF EXISTS `admin_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_group` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` text,
  `addedon` date DEFAULT NULL,
  `username` char(128) DEFAULT NULL,
  `password` char(128) DEFAULT NULL,
  `status` text,
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `super_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_group`
--

LOCK TABLES `admin_group` WRITE;
/*!40000 ALTER TABLE `admin_group` DISABLE KEYS */;
INSERT INTO `admin_group` VALUES (1,'Velammal Educational Trust','2020-11-18','admin@vet.com','sol123','active','2020-11-18 07:06:32',5),(2,'grpadmin','2020-11-18','grpadmin@gmail.com','grpadmin','active','2020-11-18 13:03:28',4);
/*!40000 ALTER TABLE `admin_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alloted_admin`
--

DROP TABLE IF EXISTS `alloted_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alloted_admin` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `addedon` date DEFAULT NULL,
  `admin_id` bigint(20) DEFAULT NULL,
  `admin_grp_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alloted_admin`
--

LOCK TABLES `alloted_admin` WRITE;
/*!40000 ALTER TABLE `alloted_admin` DISABLE KEYS */;
INSERT INTO `alloted_admin` VALUES (1,'2020-11-18',1,1),(2,'2020-11-18',2,2),(3,'2020-11-19',3,2),(4,'2020-11-20',4,2),(5,'2020-11-20',5,2),(6,'2020-11-20',6,2),(7,'2020-11-22',7,2);
/*!40000 ALTER TABLE `alloted_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alloted_to`
--

DROP TABLE IF EXISTS `alloted_to`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alloted_to` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `support_id` bigint(20) NOT NULL,
  `account_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `support_id` (`support_id`),
  CONSTRAINT `alloted_to_ibfk_1` FOREIGN KEY (`support_id`) REFERENCES `support` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alloted_to`
--

LOCK TABLES `alloted_to` WRITE;
/*!40000 ALTER TABLE `alloted_to` DISABLE KEYS */;
INSERT INTO `alloted_to` VALUES (1,1,1),(2,2,3);
/*!40000 ALTER TABLE `alloted_to` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `controller`
--

DROP TABLE IF EXISTS `controller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controller` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` text,
  `username` char(128) DEFAULT NULL,
  `password` char(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controller`
--

LOCK TABLES `controller` WRITE;
/*!40000 ALTER TABLE `controller` DISABLE KEYS */;
INSERT INTO `controller` VALUES (1,'controller','controller','2471245b44ddb58348c26a55bc5ccd5edea29a662b98bb5e58747ae4e4b2187e27be9e582ca2f3234eb829d37517fe981d0583300f16a823149267a7e9d0b433');
/*!40000 ALTER TABLE `controller` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `energy_meter`
--

DROP TABLE IF EXISTS `energy_meter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `energy_meter` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `EM_id` text,
  `addedon` date DEFAULT NULL,
  `capacity` text,
  `admin` bigint(20) DEFAULT NULL,
  `status` text,
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` bigint(20) NOT NULL,
  `groupadmin` bigint(20) NOT NULL,
  `equipment_id` int(5) NOT NULL,
  `slave_id` int(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `energy_meter`
--

LOCK TABLES `energy_meter` WRITE;
/*!40000 ALTER TABLE `energy_meter` DISABLE KEYS */;
INSERT INTO `energy_meter` VALUES (1,'EMR 1','2020-11-18','22KV',2,1,'active','2020-11-18 11:27:50',5,1,2,91);
/*!40000 ALTER TABLE `energy_meter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gateway`
--

DROP TABLE IF EXISTS `gateway`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gateway` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `Meter_id` text,
  `addedon` date DEFAULT NULL,
  `capacity` text,
  `admin` bigint(20) DEFAULT NULL,
  `status` text,
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` bigint(20) NOT NULL,
  `groupadmin` bigint(20) NOT NULL,
  `api_key` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gateway`
--

LOCK TABLES `gateway` WRITE;
/*!40000 ALTER TABLE `gateway` DISABLE KEYS */;
INSERT INTO `gateway` VALUES (1,'testcap','2020-11-19','12',3,'active','2020-11-19 04:50:55',4,2,'1244sdsc'),(2,'test','2020-11-19','12',1,'active','2020-11-19 04:52:00',5,1,'c8DrAnUs');
/*!40000 ALTER TABLE `gateway` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inverter`
--

DROP TABLE IF EXISTS `inverter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inverter` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` text,
  `addedon` date DEFAULT NULL,
  `capacity` text,
  `install_date` date DEFAULT NULL,
  `admin` bigint(20) DEFAULT NULL,
  `status` text,
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` bigint(20) NOT NULL,
  `groupadmin` bigint(20) NOT NULL,
  `equipment_id` int(5) DEFAULT NULL,
  `slave_id` int(5) DEFAULT NULL,
  `energy_meter_id` bigint(20) NOT NULL
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inverter`
--

LOCK TABLES `inverter` WRITE;
/*!40000 ALTER TABLE `inverter` DISABLE KEYS */;
INSERT INTO `inverter` VALUES (1,'test','2020-11-18','test','2020-11-18',1,'active','2020-11-18 11:21:11',5,1,12,13),(2,'INVERTER ABB_1','2020-11-18','1.8MW','2020-11-18',1,'active','2020-11-18 11:24:25',5,1,1,81),(3,'INVERTER ABB_2','2020-11-18','1.8MW','2020-11-18',1,'active','2020-11-18 11:24:25',5,1,1,82),(4,'inverter','2020-11-22','12','2020-11-01',7,'active','2020-11-22 03:27:11',4,2,12,12,0);
/*!40000 ALTER TABLE `inverter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rolls`
--

DROP TABLE IF EXISTS `rolls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rolls` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `roll_name` char(128) DEFAULT NULL,
  `status` text,
  `accounts_approver` text,
  `super_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `roll_name` (`roll_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rolls`
--

LOCK TABLES `rolls` WRITE;
/*!40000 ALTER TABLE `rolls` DISABLE KEYS */;
/*!40000 ALTER TABLE `rolls` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smb`
--

DROP TABLE IF EXISTS `smb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smb` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `smb_id` text,
  `addedon` date DEFAULT NULL,
  `capacity` text,
  `inverter` bigint(20) DEFAULT NULL,
  `admin` bigint(20) DEFAULT NULL,
  `status` text,
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` bigint(20) NOT NULL,
  `groupadmin` bigint(20) NOT NULL,
  `equipment_id` int(5) NOT NULL,
  `slave_id` int(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smb`
--

LOCK TABLES `smb` WRITE;
/*!40000 ALTER TABLE `smb` DISABLE KEYS */;
INSERT INTO `smb` VALUES (1,'SMB 1','2020-11-18','1500V DC',2,1,'active','2020-11-18 11:24:25',5,1,9,1),(2,'SMB 2','2020-11-18','1500V DC',2,1,'active','2020-11-18 11:24:25',5,1,9,2);
/*!40000 ALTER TABLE `smb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solar_panel_data`
--

DROP TABLE IF EXISTS `solar_panel_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solar_panel_data` (
  `my_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `api_key` text NOT NULL,
  `S_NO` bigint(20) NOT NULL,
  `IP` varchar(20) NOT NULL,
  `DID` varchar(20) NOT NULL,
  `EID` double NOT NULL,
  `ID` bigint(20) NOT NULL,
  `FC` double NOT NULL,
  `ADDRESS` text NOT NULL,
  `QUANTITY` double NOT NULL,
  `TIME_STAMP` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `FIELD0` double NOT NULL,
  `FIELD1` double NOT NULL,
  `FIELD2` double NOT NULL,
  `FIELD3` double NOT NULL,
  `FIELD4` double NOT NULL,
  `FIELD5` double NOT NULL,
  `FIELD6` double NOT NULL,
  `FIELD7` double NOT NULL,
  `FIELD8` double NOT NULL,
  `FIELD9` double NOT NULL,
  `FIELD10` double NOT NULL,
  `FIELD11` double NOT NULL,
  `FIELD12` double NOT NULL,
  `FIELD13` double NOT NULL,
  `FIELD14` double NOT NULL,
  `FIELD15` double NOT NULL,
  `FIELD16` double NOT NULL,
  `FIELD17` double NOT NULL,
  `FIELD18` double NOT NULL,
  `FIELD19` double NOT NULL,
  `FIELD20` double NOT NULL,
  `FIELD21` double NOT NULL,
  `FIELD22` double NOT NULL,
  `FIELD23` double NOT NULL,
  `FIELD24` double NOT NULL,
  `FIELD25` double NOT NULL,
  `FIELD26` double NOT NULL,
  `FIELD27` double NOT NULL,
  `FIELD28` double NOT NULL,
  `FIELD29` double NOT NULL,
  `FIELD30` double NOT NULL,
  `FIELD31` double NOT NULL,
  `FIELD32` double NOT NULL,
  `FIELD33` double NOT NULL,
  `FIELD34` double NOT NULL,
  `FIELD35` double NOT NULL,
  `FIELD36` double NOT NULL,
  `FIELD37` double NOT NULL,
  `FIELD38` double NOT NULL,
  `FIELD39` double NOT NULL,
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`my_id`)
) ENGINE=InnoDB AUTO_INCREMENT=175069 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;



DROP TABLE IF EXISTS `super_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `super_admin` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` text,
  `addedon` date DEFAULT NULL,
  `username` char(128) DEFAULT NULL,
  `password` char(128) DEFAULT NULL,
  `location` text,
  `status` text,
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `super_admin`
--

LOCK TABLES `super_admin` WRITE;
/*!40000 ALTER TABLE `super_admin` DISABLE KEYS */;
INSERT INTO `super_admin` VALUES (4,'admin','2020-09-30','admin','f2b08a609eefe6c83e34d9fc348932cff7d877c2ccb52cb3f17dd2ee4139d63917397a24fd4f6a9f2f1d891ec97184329a44dec95adc78c50ed82d1e72af89bd','','Active','2020-10-01 06:47:27'),(5,'Grand Solar Private Ltd.','2020-11-18','admin@gspl.com','20960bf59e4a48ff7acf23e05912f2b41a90e56c675dc6d0bd85ee769f8d3113f34a0f1d74804e5c145e76ec0cd83e02b1470d531f251ab7ab8f61f5bd2ee364','','active','2020-11-18 07:02:52'),(6,'GRAND SOLAR 2','2020-11-18','admin@gspl2.com','20960bf59e4a48ff7acf23e05912f2b41a90e56c675dc6d0bd85ee769f8d3113f34a0f1d74804e5c145e76ec0cd83e02b1470d531f251ab7ab8f61f5bd2ee364','chennai','active','2020-11-18 11:55:04');
/*!40000 ALTER TABLE `super_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `support`
--

DROP TABLE IF EXISTS `support`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `support` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `admin` bigint(20) DEFAULT NULL,
  `name` text,
  `title` text,
  `description` text,
  `status` text,
  `allotted_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `completed_on` date DEFAULT NULL,
  `remarks` text,
  `periority` text,
  `due_date` date DEFAULT NULL,
  `admin_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `support`
--

LOCK TABLES `support` WRITE;
/*!40000 ALTER TABLE `support` DISABLE KEYS */;
INSERT INTO `support` VALUES (1,1,'1','SMB 17 NOT WORKING','TEST','Open','2020-11-18 12:25:29','2020-11-18','TEST','High','2020-11-20',5),(2,2,'2','testsub','testdes','Open','2020-11-18 13:11:10','2020-11-18','testsub','High','2020-11-19',4);
/*!40000 ALTER TABLE `support` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_admin_allote`
--

DROP TABLE IF EXISTS `user_admin_allote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_admin_allote` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `addedon` date DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `admin_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_admin_allote`
--

LOCK TABLES `user_admin_allote` WRITE;
/*!40000 ALTER TABLE `user_admin_allote` DISABLE KEYS */;
INSERT INTO `user_admin_allote` VALUES (1,'2020-11-18',1,1),(2,'2020-11-18',2,1),(3,'2020-11-18',3,2);
/*!40000 ALTER TABLE `user_admin_allote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` text,
  `addedon` date DEFAULT NULL,
  `username` char(128) DEFAULT NULL,
  `password` char(128) DEFAULT NULL,
  `view` text,
  `edit` text,
  `approve` text,
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `super_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'NAGENDRAN','2020-11-18','NAGA@GSPL.COM','sol123','Yes','No','No','2020-11-18 12:15:45',5),(2,'RAMESH','2020-11-18','ramesh@gspl.com','sol123','Yes','Yes','Yes','2020-11-18 12:15:45',5),(3,'testuser','2020-11-18','testuser','user','Yes','Yes','Yes','2020-11-18 13:10:27',4);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `w_w`
--

DROP TABLE IF EXISTS `w_w`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `w_w` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `w_w` text,
  `addedon` date DEFAULT NULL,
  `capacity` text,
  `admin` bigint(20) DEFAULT NULL,
  `status` text,
  `lastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` bigint(20) NOT NULL,
  `groupadmin` bigint(20) NOT NULL,
  `equipment_id` int(5) NOT NULL,
  `slave_id` int(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `w_w`
--

LOCK TABLES `w_w` WRITE;
/*!40000 ALTER TABLE `w_w` DISABLE KEYS */;
INSERT INTO `w_w` VALUES (1,'WMS','2020-11-18','NA',1,'active','2020-11-18 10:18:16',5,1,3,60);
/*!40000 ALTER TABLE `w_w` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-23  5:57:58
