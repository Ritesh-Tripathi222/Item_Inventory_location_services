ALTER TABLE location_contact_info ADD FOREIGN KEY (location_id) REFERENCES location(id);
ALTER TABLE location_receiving_info ADD FOREIGN KEY (location_id) REFERENCES location(id);
ALTER TABLE location_shipping_info ADD FOREIGN KEY (location_id) REFERENCES location(id);


ALTER TABLE location ADD UNIQUE (ref_location_id);


UPDATE service_levels SET name = 'standard' WHERE (`id` = '1');
UPDATE service_levels SET name = 'expedited' WHERE (`id` = '2');
