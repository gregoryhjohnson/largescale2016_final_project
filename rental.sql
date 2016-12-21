DROP DATABASE IF EXISTS `rental_app`;
CREATE DATABASE `rental_app`
    DEFAULT CHARACTER SET utf8
    DEFAULT COLLATE utf8_general_ci;

USE 'mysql';
GRANT ALL PRIVILEGES ON rental_app.* TO 'appserver'@'localhost' IDENTIFIED BY 'foobarzoot'

WITH GRANT OPTION;
FLUSH PRIVILEGES;
