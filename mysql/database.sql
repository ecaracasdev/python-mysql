CREATE DATABASE chanelworks;

USE chanelworks;

CREATE TABLE developer (
  id int PRIMARY KEY,
  fullname varchar(50),
  active bool
);

CREATE TABLE license (
  id int PRIMARY KEY,
  software varchar(50)
);

CREATE TABLE asset (
  id int PRIMARY KEY,
  brand varchar(50),
  model varchar(50),
  type enum('laptop', 'keyboard', 'mouse', 'headset', 'monitor')
);

CREATE TABLE developer_licenses (
  developer_id int REFERENCES developer(id),
  license_id int REFERENCES license(id),
  PRIMARY KEY (developer_id, license_id)
);

CREATE TABLE developer_assets (
  developer_id int REFERENCES developer(id),
  asset_id int REFERENCES asset(id),
  PRIMARY KEY (developer_id, asset_id)
);

CREATE TABLE user (
  id int PRIMARY KEY,
  username varchar(50) UNIQUE,
  password varchar(100),
  fullname varchar(50)
);


INSERT INTO developer (id, fullname, active)
VALUES (1, 'John Doe', true),
       (2, 'Jane Smith', false);

INSERT INTO license (id, software)
VALUES (1, 'Visual Studio Code'),
       (2, 'PyCharm');

INSERT INTO asset (id, brand, model, type)
VALUES (1, 'HP', 'Elitebook', 'laptop'),
       (2, 'Logitech', 'K120', 'keyboard');

INSERT INTO developer_licenses (developer_id, license_id)
VALUES (1, 1),
       (2, 2);

INSERT INTO developer_assets (developer_id, asset_id)
VALUES (1, 1),
       (2, 2);

INSERT INTO user (id, username, password, fullname)
VALUES (1, 'admin', 'pbkdf2:sha256:260000$EGWshHJk$0a5e6cd3836e7e036f664fb92afca8f84623d4d2cb71bc9524f804178398ce69', 'Admin');