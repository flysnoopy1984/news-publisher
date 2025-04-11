/*
 Navicat Premium Dump SQL

 Source Server         : 卡卡110
 Source Server Type    : MySQL
 Source Server Version : 80039 (8.0.39)
 Source Host           : 110.40.137.44:3306
 Source Schema         : aiinfo

 Target Server Type    : MySQL
 Target Server Version : 80039 (8.0.39)
 File Encoding         : 65001

 Date: 11/04/2025 16:27:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for news_infos
-- ----------------------------
DROP TABLE IF EXISTS `news_infos`;
CREATE TABLE `news_infos`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `newsId` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `createDateTime` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
