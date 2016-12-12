-- SQL Script to setup database

CREATE DATABASE sample_analysis CHARACTER SET UTF8;
CREATE USER jcura_user@localhost IDENTIFIED BY '123456789';
GRANT ALL PRIVILEGES ON sample_analysis.* TO jcura_user@localhost;
FLUSH PRIVILEGES;
