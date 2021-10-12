ALTER TABLE item_detail ADD FOREIGN KEY (item_id) REFERENCES item(id);
ALTER TABLE item_selling_info ADD FOREIGN KEY (item_id) REFERENCES item(id);
ALTER TABLE item_purchase_info ADD FOREIGN KEY (item_id) REFERENCES item(id);


ALTER TABLE item ADD UNIQUE (sku);
