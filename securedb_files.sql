-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: securep.c7x8rgc7mug5.us-east-2.rds.amazonaws.com    Database: securedb
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `files` (
  `fid` int NOT NULL AUTO_INCREMENT,
  `gid` int NOT NULL,
  `timestamp` date NOT NULL,
  `fileurl` varchar(255) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `keys` varchar(500) NOT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
INSERT INTO `files` VALUES (1,2,'2022-11-24','https://98shashi1.s3.amazonaws.com/test.txt','test.txt',''),(2,2,'2022-11-24','https://98shashi1.s3.amazonaws.com/shahsi.txt','shahsi.txt',''),(3,2,'2022-11-24','https://98shashi1.s3.amazonaws.com/shahsi.txt','shahsi.txt',''),(4,2,'2022-11-24','https://98shashi1.s3.amazonaws.com/s3.txt','s3.txt',''),(5,2,'2022-11-24','https://98shashi1.s3.amazonaws.com/ss.txt','ss.txt','XIONu2GmMEmAu9lIbIPHMyXdsAh7PtPX9Kiav7UORdo='),(6,2,'2022-11-24','https://98shashi1.s3.amazonaws.com/ss.txt','ss.txt','Osc8eCl1-RDPCcVcNdflU6U4jvJX6j_-AR-ZM1zzsL8='),(7,2,'2022-11-24','https://98shashi1.s3.amazonaws.com/ss.txt','ss.txt','zbjjVpbj--YV_Nni1em44DXZKzQ9sZhxnbC0SJ06iv0='),(8,2,'2022-11-24','https://98shashi1.s3.amazonaws.com/test8.txt','test8.txt','dzHV6vlFZbg4ZWklaYIEhL1ZxZazKS5dlPmg9gjCuhM='),(9,2,'2022-11-24','https://98shashi1.s3.amazonaws.com/temp.txt','temp.txt','aM8qEDBH1YdKmuPq19kFB2EJr9sSAc92e9xZMSeqqhk='),(10,2,'2022-11-24','https://98shashi1.s3.amazonaws.com/temp2.txt','temp2.txt','-_T94OLXQsID_AqddKsArmKXWY035PenmiTehrvBZK0='),(11,1,'2022-11-25','https://98shashi1.s3.amazonaws.com/test.txt','test.txt','pJohY71uoTyuPg5jbgYmK4ro9cygiEPVtoGmxz0AxAA=');
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-25 19:56:13
