-- MySQL dump 10.13  Distrib 5.6.30, for Linux (x86_64)
--
-- Host: localhost    Database: live
-- ------------------------------------------------------
-- Server version	5.6.30

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
-- Table structure for table `live`
--

DROP TABLE IF EXISTS `live`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live` (
  `liveid` varchar(233) NOT NULL DEFAULT '',
  `state` int(11) DEFAULT NULL,
  `snapshot` varchar(233) DEFAULT NULL,
  `title` varchar(233) DEFAULT NULL,
  `publish_url` varchar(233) DEFAULT NULL,
  `playback_hls_url` varchar(233) DEFAULT NULL,
  `rtmp_live_url` varchar(233) DEFAULT NULL,
  `persons` int(11) DEFAULT NULL,
  `supports` int(11) DEFAULT NULL,
  `tojson` varchar(1024) DEFAULT NULL,
  `hls_live_url` varchar(255) DEFAULT NULL,
  `startime` datetime DEFAULT NULL,
  PRIMARY KEY (`liveid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `live`
--

LOCK TABLES `live` WRITE;
/*!40000 ALTER TABLE `live` DISABLE KEYS */;
INSERT INTO `live` VALUES ('z1.mycs.1465523282',0,'http://img.blog.csdn.net/20131204093907625','[]','rtmp://pili-publish.qiniu.mycs.cn/mycs/1465523282?key=b37f9e20-9e6d-41fb-89d6-cf3ada83065f','','rtmp://pili-live-rtmp.qiniu.mycs.cn/mycs/1465523282',0,0,'{\"publishSecurity\": \"static\", \"hub\": \"mycs\", \"title\": \"1465523282\", \"publishKey\": \"b37f9e20-9e6d-41fb-89d6-cf3ada83065f\", \"disabled\": false, \"disabledTill\": 0, \"hosts\": {\"live\": {\"snapshot\": \"10000eb.live1-snapshot.z1.pili.qiniucdn.com\", \"http\": \"pili-live-hls.qiniu.mycs.cn\", \"hdl\": \"pili-live-hdl.qiniu.mycs.cn\", \"hls\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"playback\": {\"http\": \"10000eb.playback1.z1.pili.qiniucdn.com\", \"hls\": \"10000eb.playback1.z1.pili.qiniucdn.com\"}, \"play\": {\"http\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"publish\": {\"rtmp\": \"pili-publish.qiniu.mycs.cn\"}}, \"updatedAt\": \"2016-06-10T01:48:02.504Z\", \"id\": \"z1.mycs.1465523282\", \"createdAt\": \"2016-06-10T01:48:02.504Z\"}','http://pili-live-hls.qiniu.mycs.cn/mycs/1465523282.m3u8',NULL),('z1.mycs.1466059427',0,'http://img.blog.csdn.net/20131204093907625','[u\']','rtmp://pili-publish.qiniu.mycs.cn/mycs/1466059427?key=b37f9e20-9e6d-41fb-89d6-cf3ada83065f','','rtmp://pili-live-rtmp.qiniu.mycs.cn/mycs/1466059427',0,0,'{\"publishSecurity\": \"static\", \"hub\": \"mycs\", \"title\": \"1466059427\", \"publishKey\": \"b37f9e20-9e6d-41fb-89d6-cf3ada83065f\", \"disabled\": false, \"disabledTill\": 0, \"hosts\": {\"live\": {\"snapshot\": \"10000eb.live1-snapshot.z1.pili.qiniucdn.com\", \"http\": \"pili-live-hls.qiniu.mycs.cn\", \"hdl\": \"pili-live-hdl.qiniu.mycs.cn\", \"hls\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"playback\": {\"http\": \"10000eb.playback1.z1.pili.qiniucdn.com\", \"hls\": \"10000eb.playback1.z1.pili.qiniucdn.com\"}, \"play\": {\"http\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"publish\": {\"rtmp\": \"pili-publish.qiniu.mycs.cn\"}}, \"updatedAt\": \"2016-06-16T06:43:47.367Z\", \"id\": \"z1.mycs.1466059427\", \"createdAt\": \"2016-06-16T06:43:47.367Z\"}','http://pili-live-hls.qiniu.mycs.cn/mycs/1466059427.m3u8',NULL),('z1.mycs.1466141846',2,'http://pili-static.qiniu.mycs.cn/snapshots/z1.mycs.1466141846/snapshot.jpg','流程测试','rtmp://pili-publish.qiniu.mycs.cn/mycs/1466141846?key=b37f9e20-9e6d-41fb-89d6-cf3ada83065f','http://pili-static.qiniu.mycs.cn/recordings/z1.mycs.1466141846/1466142731.m3u8','rtmp://pili-live-rtmp.qiniu.mycs.cn/mycs/1466141846',0,0,'{\"publishSecurity\": \"static\", \"hub\": \"mycs\", \"title\": \"1466141846\", \"publishKey\": \"b37f9e20-9e6d-41fb-89d6-cf3ada83065f\", \"disabled\": false, \"disabledTill\": 0, \"hosts\": {\"live\": {\"snapshot\": \"10000eb.live1-snapshot.z1.pili.qiniucdn.com\", \"http\": \"pili-live-hls.qiniu.mycs.cn\", \"hdl\": \"pili-live-hdl.qiniu.mycs.cn\", \"hls\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"playback\": {\"http\": \"10000eb.playback1.z1.pili.qiniucdn.com\", \"hls\": \"10000eb.playback1.z1.pili.qiniucdn.com\"}, \"play\": {\"http\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"publish\": {\"rtmp\": \"pili-publish.qiniu.mycs.cn\"}}, \"updatedAt\": \"2016-06-17T05:37:26.901Z\", \"id\": \"z1.mycs.1466141846\", \"createdAt\": \"2016-06-17T05:37:26.901Z\"}','http://pili-live-hls.qiniu.mycs.cn/mycs/1466141846.m3u8',NULL),('z1.mycs.1466142683',2,'http://pili-static.qiniu.mycs.cn/snapshots/z1.mycs.1466142683/snapshot.jpg','直播流程再次测试','rtmp://pili-publish.qiniu.mycs.cn/mycs/1466142683?key=b37f9e20-9e6d-41fb-89d6-cf3ada83065f','http://pili-static.qiniu.mycs.cn/recordings/z1.mycs.1466142683/1466146052.m3u8','rtmp://pili-live-rtmp.qiniu.mycs.cn/mycs/1466142683',0,0,'{\"publishSecurity\": \"static\", \"hub\": \"mycs\", \"title\": \"1466142683\", \"publishKey\": \"b37f9e20-9e6d-41fb-89d6-cf3ada83065f\", \"disabled\": false, \"disabledTill\": 0, \"hosts\": {\"live\": {\"snapshot\": \"10000eb.live1-snapshot.z1.pili.qiniucdn.com\", \"http\": \"pili-live-hls.qiniu.mycs.cn\", \"hdl\": \"pili-live-hdl.qiniu.mycs.cn\", \"hls\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"playback\": {\"http\": \"10000eb.playback1.z1.pili.qiniucdn.com\", \"hls\": \"10000eb.playback1.z1.pili.qiniucdn.com\"}, \"play\": {\"http\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"publish\": {\"rtmp\": \"pili-publish.qiniu.mycs.cn\"}}, \"updatedAt\": \"2016-06-17T05:51:23.354Z\", \"id\": \"z1.mycs.1466142683\", \"createdAt\": \"2016-06-17T05:51:23.354Z\"}','http://pili-live-hls.qiniu.mycs.cn/mycs/1466142683.m3u8',NULL),('z1.mycs.1466246029',0,'http://img.blog.csdn.net/20131204093907625','','rtmp://pili-publish.qiniu.mycs.cn/mycs/1466246029?key=b37f9e20-9e6d-41fb-89d6-cf3ada83065f','','rtmp://pili-live-rtmp.qiniu.mycs.cn/mycs/1466246029',0,0,'{\"publishSecurity\": \"static\", \"hub\": \"mycs\", \"title\": \"1466246029\", \"publishKey\": \"b37f9e20-9e6d-41fb-89d6-cf3ada83065f\", \"disabled\": false, \"disabledTill\": 0, \"hosts\": {\"live\": {\"snapshot\": \"10000eb.live1-snapshot.z1.pili.qiniucdn.com\", \"http\": \"pili-live-hls.qiniu.mycs.cn\", \"hdl\": \"pili-live-hdl.qiniu.mycs.cn\", \"hls\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"playback\": {\"http\": \"10000eb.playback1.z1.pili.qiniucdn.com\", \"hls\": \"10000eb.playback1.z1.pili.qiniucdn.com\"}, \"play\": {\"http\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"publish\": {\"rtmp\": \"pili-publish.qiniu.mycs.cn\"}}, \"updatedAt\": \"2016-06-18T10:33:49.113Z\", \"id\": \"z1.mycs.1466246029\", \"createdAt\": \"2016-06-18T10:33:49.113Z\"}','http://pili-live-hls.qiniu.mycs.cn/mycs/1466246029.m3u8',NULL),('z1.mycs.tgp',0,'http://pili-static.qiniu.mycs.cn/snapshots/z1.mycs.xiechc/snapshot.jpg','直播中','rtmp://pili-publish.qiniu.mycs.cn/mycs/xiechc?key=b37f9e20-9e6d-41fb-89d6-cf3ada83065f','http://pili-static.qiniu.mycs.cn/recordings/z1.mycs.xiechc/1465785810.m3u8','rtmp://pili-live-rtmp.qiniu.mycs.cn/mycs/xiechc',300,361,NULL,'hls.qiniu.mycs.cn/mycs/xiechc.m3u8',NULL),('z1.mycs.xiechc',1,'http://pili-static.qiniu.mycs.cn/snapshots/z1.mycs.xiechc/snapshot.jpg','直播测试','rtmp://pili-publish.qiniu.mycs.cn/mycs/1465279101?key=b37f9e20-9e6d-41fb-89d6-cf3ada83065f','','rtmp://pili-live-rtmp.qiniu.mycs.cn/mycs/1465279101',0,3,'{\"publishSecurity\": \"static\", \"hub\": \"mycs\", \"title\": \"1465279101\", \"publishKey\": \"b37f9e20-9e6d-41fb-89d6-cf3ada83065f\", \"disabled\": false, \"disabledTill\": 0, \"hosts\": {\"live\": {\"snapshot\": \"10000eb.live1-snapshot.z1.pili.qiniucdn.com\", \"http\": \"pili-live-hls.qiniu.mycs.cn\", \"hdl\": \"pili-live-hdl.qiniu.mycs.cn\", \"hls\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"playback\": {\"http\": \"10000eb.playback1.z1.pili.qiniucdn.com\", \"hls\": \"10000eb.playback1.z1.pili.qiniucdn.com\"}, \"play\": {\"http\": \"pili-live-hls.qiniu.mycs.cn\", \"rtmp\": \"pili-live-rtmp.qiniu.mycs.cn\"}, \"publish\": {\"rtmp\": \"pili-publish.qiniu.mycs.cn\"}}, \"updatedAt\": \"2016-06-07T05:58:21.27Z\", \"id\": \"z1.mycs.1465279101\", \"createdAt\": \"2016-06-07T05:58:21.27Z\"}','http://pili-live-hls.qiniu.mycs.cn/mycs/1465279101.m3u8',NULL);
/*!40000 ALTER TABLE `live` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `owner`
--

DROP TABLE IF EXISTS `owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `owner` (
  `ownerid` mediumint(9) DEFAULT NULL,
  `liveid` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`liveid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `owner`
--

LOCK TABLES `owner` WRITE;
/*!40000 ALTER TABLE `owner` DISABLE KEYS */;
INSERT INTO `owner` VALUES (1234,'z1.mycs.1465523282'),(1234,'z1.mycs.1466059427'),(1234,'z1.mycs.1466141846'),(1234,'z1.mycs.1466142683'),(1234,'z1.mycs.1466246029'),(1234,'z1.mycs.tgp'),(1234,'z1.mycs.xiechc');
/*!40000 ALTER TABLE `owner` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-06-22  9:46:55
