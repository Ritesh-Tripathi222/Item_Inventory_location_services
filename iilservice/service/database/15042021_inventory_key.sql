
ALTER TABLE inventory ADD FOREIGN KEY (item_id) REFERENCES item(id);
ALTER TABLE inventory ADD FOREIGN KEY (location_id) REFERENCES location(id);

ALTER TABLE inventory_attribute_info ADD FOREIGN KEY (inventory_id) REFERENCES inventory(id);
ALTER TABLE inventory_attribute_info ADD FOREIGN KEY (inventory_attribute_id) REFERENCES inventory_attribute_settings(id);
