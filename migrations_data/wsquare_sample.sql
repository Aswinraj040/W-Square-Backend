-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: wsquare
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `USER_NAME` varchar(100) NOT NULL,
  `EMAIL` varchar(255) DEFAULT NULL,
  `PASSWORD` varchar(255) DEFAULT NULL,
  `CREATE` tinyint(1) DEFAULT NULL,
  `UPDATE` tinyint(1) DEFAULT NULL,
  `READ` tinyint(1) DEFAULT NULL,
  `DELETE` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`USER_NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('admin','admin@gmail.com','scrypt:32768:8:1$qzOJX8Wb4IcB0MBh$531e2f880f16b8a41841688ee06c94b6ffa9299626bfd0519b19e4d6ddbe3844b79b8ef2b32e4d59780ac69f85522fbb45c11d0e21890ca2c931ce08a0047f1a',1,1,1,1);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `claim`
--

DROP TABLE IF EXISTS `claim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim` (
  `Vehicle_number` varchar(100) DEFAULT NULL,
  `Client_Name` varchar(100) DEFAULT NULL,
  `Insurance_company` varchar(100) DEFAULT NULL,
  `claim_number` varchar(100) NOT NULL,
  `accident_date` date DEFAULT NULL,
  `Surveyor_name` varchar(100) DEFAULT NULL,
  `surveyor_contact` varchar(100) DEFAULT NULL,
  `Garage_location` varchar(255) DEFAULT NULL,
  `remarks` json DEFAULT NULL,
  `garage_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`claim_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `claim`
--

LOCK TABLES `claim` WRITE;
/*!40000 ALTER TABLE `claim` DISABLE KEYS */;
INSERT INTO `claim` VALUES ('TN02CD3456','User2','VIC','895641','2025-06-04','Balaji C','985641237','User area','[\"The vehicle side mirror damaged.\", \"The front suspension is locked.\"]','Star Garage'),('TN01AB1234','User1','ICICI Lombard','CLM10001','2025-06-02','Ravi Kumar','9876543210','Kodambakkam','[\"Front bumper damaged\", \"Left indicator broken\"]','Dr Garage'),('TN02CD9012','User2','VIC','CLM10002','2025-06-04','Balaji C','985641237','User area','[\"Side mirror damaged\", \"Front suspension locked\"]',NULL),('TN02CD7890','User2','Bajaj Allianz','CLM10003','2025-06-05','Arun M','9898989890','Velachery','[\"Windscreen cracked\", \"AC not working\"]',NULL),('TN03EF1234','User3','HDFC Ergo','CLM10004','2025-06-06','Suresh M','9786452310','T Nagar','[\"Battery shorted\", \"Dashboard lights on\"]',NULL),('TN04GH3456','User4','Tata AIG','CLM10005','2025-06-07','Prakash N','9898989898','Ambattur','[\"Cargo door dented\", \"Rear lights broken\"]',NULL),('TN04GH9012','User4','Reliance General','CLM10006','2025-06-08','Naveen Rao','9812345678','Perambur','[\"Fuel tank leak\", \"Scratches on right panel\"]',NULL);
/*!40000 ALTER TABLE `claim` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `USER_NAME` varchar(100) NOT NULL,
  `NAME` varchar(255) DEFAULT NULL,
  `EMAIL` varchar(255) DEFAULT NULL,
  `PASSWORD` varchar(255) DEFAULT NULL,
  `PHONE` varchar(255) DEFAULT NULL,
  `ADDRESS` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`USER_NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES ('User1','User One','user1@gmail.com','scrypt:32768:8:1$arPkyTVkuj6sIDKG$01b074aaa129eedb3ecd5346b215126e3b4d6e4b28813dfa951beea373ad8be24346be2545376b28f8268072a35e519e8ad16cba4caf50f25ca8f3c2ad2d5b3f','9876543210','No. 12/5, User street, Userpakkam, Chennai - 600001'),('User2','User Two','user2@gmail.com','scrypt:32768:8:1$iLNExyoQB7XRs2rv$8f80002b6f3a73d121c049695c981f4a5f4882c012a7e7d5ec3803b89f54ce9bed9ea1782836b02cbd499bdb2f50422198840a33052de1677b4187ac7dd66450','9874561230','No. 12/5, User street, Userpakkam, Chennai - 600002'),('User3','User Three','user3@gmail.com','scrypt:32768:8:1$mDmhNKsg7h0TvSlH$d12e65c4dc3421e52982e777737b00a4ed5e472d428309f0ad3a2e58d8140b54116133f34cbd572d603aa6125790f5b2fc8aac38bd561ef32b5d9ce67e8d0ba8','1234567890','No. 12/5, User street, Userpakkam, Chennai - 600003'),('User4','User Four','user4@gmail.com','scrypt:32768:8:1$9U9FZFBtVej2oLxy$63ac839e17277aa14560518c085b9569d09e1cf3e1dadf31f6580aa860f7866e6dca7760ea8e0d35b5b150ed3930e10e4d3a759580c4229a8af8b5f3d60f2839','7896541230','No. 12/5, User street, Userpakkam, Chennai - 600004'),('User5','User Five','user5@gmail.com','scrypt:32768:8:1$dh530xaJFKEzztx6$dada3144b4ac8c043230ef47597403d24b9b2f7aa6b8655e766b01e17a2d076274f907b94538cdcf649ab378fa4293e4090b385dc6a3de1d55d110c23da8964f','9632587410','No. 12/5, User street, Userpakkam, Chennai - 600005');
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle` (
  `VehicleNumber` varchar(100) NOT NULL,
  `UserName` varchar(100) DEFAULT NULL,
  `RegNo` varchar(100) DEFAULT NULL,
  `Type` varchar(100) DEFAULT NULL,
  `InsuranceExpiryDate` date DEFAULT NULL,
  `Fuel` varchar(50) DEFAULT NULL,
  `ChassisNumber` varchar(100) DEFAULT NULL,
  `EngineNumber` varchar(100) DEFAULT NULL,
  `InsuranceNumber` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`VehicleNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle`
--

LOCK TABLES `vehicle` WRITE;
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
INSERT INTO `vehicle` VALUES ('TN01AB1234','User1','TN01AB1234','Staff','2025-06-08','Petrol','MA3FZC32S00712345','K12MN1234567','INS20240600123'),('TN01AB5678','User1','TN01AB5678','Bike','2025-08-10','Petrol','MA3FZC32S00767890','K12MN9876543','INS20240800124'),('TN02CD3456','User2','TN02CD3456','PCV','2026-02-20','Diesel','MH34WXZ5500678901','D13A98765432','INS20260200568'),('TN02CD7890','User2','TN02CD7890','EIB','2026-04-05','CNG','MH34WXZ5500765432','D13A54321678','INS20260400569'),('TN02CD9012','User2','TN02CD9012','Goods','2025-12-15','Diesel','MH34WXZ5500123456','D13A12345678','INS20241200567'),('TN03EF1234','User3','TN03EF1234','Misc - D','2026-01-20','Electric','KA59EVT987654321','EVX45678901','INS20260100012'),('TN03EF5678','User3','TN03EF5678','Staff','2026-03-10','Petrol','KA59EVT987612345','EVX12345678','INS20260300013'),('TN04GH3456','User4','TN04GH3456','Goods','2025-11-25','Diesel','DL10CN9087123456','CNX12345678','INS20251100988'),('TN04GH9012','User4','TN04GH9012','Bike','2025-09-30','CNG','DL10CN9087654321','CNX98765432','INS20250900987'),('TN05IJ1234','User5','TN05IJ1234','Staff','2025-10-15','Petrol','GJ01ABCD123456789','EN1234567890','INS20251000789'),('TN05IJ5678','User5','TN05IJ5678','PCV','2026-01-20','Diesel','GJ01ABCD987654321','EN0987654321','INS20260100790');
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-12 16:28:29
