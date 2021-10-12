

ALTER TABLE `item` ADD `item_type` VARCHAR(20) NOT NULL;



ALTER TABLE `item_detail` ADD `dimension_unit` VARCHAR(20) NULL DEFAULT NULL AFTER `description`,
    ADD `dimension_x` decimal(5,2)  NULL DEFAULT NULL AFTER `dimension_unit`,
    ADD `dimension_y` decimal(5,2)  NULL DEFAULT NULL AFTER `dimension_x`,
    ADD `dimension_z` decimal(5,2)  NULL DEFAULT NULL AFTER `dimension_y`,
    ADD `weight_unit` VARCHAR(20) NULL DEFAULT NULL AFTER `dimension_z`,
    ADD `weight` decimal(5,2) NULL DEFAULT NULL AFTER `weight_unit`;

