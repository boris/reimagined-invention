-- MySQL dump 10.13  Distrib 8.0.30, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: reimagined_invention
-- ------------------------------------------------------
-- Server version	5.7.37

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
-- Current Database: `reimagined_invention`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `reimagined_invention` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `reimagined_invention`;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('88d6278ad594');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `country` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `author`
--

LOCK TABLES `author` WRITE;
/*!40000 ALTER TABLE `author` DISABLE KEYS */;
INSERT INTO `author` VALUES (1,'Ampuero, Fernanda','Ecuador'),(2,'Aira, César','Chile'),(3,'Almada, Selva','Argentina'),(4,'Baricco, Alessandro','Italia'),(5,'Bronte, Emily','Reino Unido');
/*!40000 ALTER TABLE `author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `pages` int(11) DEFAULT NULL,
  `read` tinyint(1) DEFAULT NULL,
  `shared` tinyint(1) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `id_user` int(11) NOT NULL,
  `id_author` int(11) NOT NULL,
  `id_editorial` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_author` (`id_author`),
  KEY `id_editorial` (`id_editorial`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `book_ibfk_1` FOREIGN KEY (`id_author`) REFERENCES `author` (`id`),
  CONSTRAINT `book_ibfk_2` FOREIGN KEY (`id_editorial`) REFERENCES `editorial` (`id`),
  CONSTRAINT `book_ibfk_3` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES (1,'Pelea de Gallos','Cuentos',2018,115,1,0,5,1,1,27),(2,'Congreso de literatura','Novela',1997,0,0,0,3,1,2,28),(3,'Chicas muertas','Crónica',2014,0,1,1,5,1,3,28),(4,'Homero Iliada','Novela',2004,187,1,0,3,1,4,29),(5,'Cumbres Borrascosas','Novela ',1847,414,1,0,4,1,5,30),(9,'El viento que arrasa','Novela',2012,142,1,0,2,1,3,31);
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_tags`
--

DROP TABLE IF EXISTS `books_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books_tags` (
  `id_tag` int(11) NOT NULL,
  `id_book` int(11) NOT NULL,
  PRIMARY KEY (`id_tag`,`id_book`),
  KEY `id_book` (`id_book`),
  CONSTRAINT `books_tags_ibfk_1` FOREIGN KEY (`id_book`) REFERENCES `book` (`id`),
  CONSTRAINT `books_tags_ibfk_2` FOREIGN KEY (`id_tag`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_tags`
--

LOCK TABLES `books_tags` WRITE;
/*!40000 ALTER TABLE `books_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `books_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `editorial`
--

DROP TABLE IF EXISTS `editorial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `editorial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `editorial`
--

LOCK TABLES `editorial` WRITE;
/*!40000 ALTER TABLE `editorial` DISABLE KEYS */;
INSERT INTO `editorial` VALUES (1,'ááéé'),(2,'asdf'),(3,'asdfááééhola'),(4,'asdfááééhola'),(5,'asdfááééhola'),(6,'Ã¡Ã¡Ã©Ã©Ã­Ã­'),(7,'asdfááééhola'),(8,'asdfááééholaöö'),(9,'123123'),(10,'áéíóú'),(11,'123123'),(12,'123123áé'),(13,'123123áé'),(14,'_á'),(15,'_á'),(16,'_á'),(17,'asdf'),(18,'asdfggg'),(19,'asdfgggÃ¡Ã©Ã«'),(20,'asdf_áéë'),(21,'asdfgggÃ¡Ã©Ã«123'),(22,'asdf_áéë111'),(23,'asdf_áéë111'),(24,'asdf_áéë111'),(25,'asdasd'),(26,'óóó'),(27,'Páginas de Espuma'),(28,'Random House Mondadori'),(29,'Anagrama'),(30,'Austral'),(31,'Montacerdos');
/*!40000 ALTER TABLE `editorial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password_hash` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'test@ri.dev','Test User','sha256$pOoumEYU5p6ELJKb$e8d480a5b3b6c51b732a2a475e9ed0cdff22f1dfd716d9f6ea9116fc8144b8af');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-03 20:28:16
