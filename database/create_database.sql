-- 空服务器建表语句 只执行一次

CREATE DATABASE IF NOT EXISTS `spider_data`;

USE `spider_data`;

CREATE TABLE IF NOT EXISTS `s_paocao` (
  `card_no` bigint(20) NOT NULL COMMENT '一卡通号',
  `count_paocao` int(11) DEFAULT NULL COMMENT '跑操次数',
  `create_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`card_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;