CREATE TABLE `stock_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `stock_id` varchar(45) NOT NULL COMMENT '股票代码',
  `symbol` varchar(45) NOT NULL COMMENT '股票代码，带 SZ/SH前缀',
  `stock_name` varchar(128) NOT NULL COMMENT '股票名称',
  `region` int NOT NULL COMMENT '地区：0 中国，1 美国',
  `open_dt` int NOT NULL COMMENT '上市时间',
  `currency` varchar(45) NOT NULL COMMENT '货币单位',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `stock_id` (`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3