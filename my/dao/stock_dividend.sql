CREATE TABLE `stock_dividend` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `stock_id` varchar(45) NOT NULL COMMENT '股票代码',
  `stock_code` varchar(45) NOT NULL COMMENT '股票代码',
  `year` int NOT NULL COMMENT '分红年份 yyyy 格式',
  `dividend_dt` int DEFAULT NULL COMMENT '分红具体日期 yyyyMMdd 格式',
  `dividend_info` varchar(1024) NOT NULL COMMENT '分红具体信息',
  `dividend_type` tinyint(4) NOT NULL COMMENT '派息类型 0不发钱，1发钱',
  `dividend_per_share` decimal(10,4) DEFAULT NULL COMMENT '每股分红金额',
  `price` decimal(10,4) DEFAULT NULL COMMENT '分红当天股价',
  `dividend_rate` decimal(10,4) DEFAULT NULL COMMENT '股息率',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `stock_dt` (`stock_code`,`year`)
) ENGINE=InnoDB