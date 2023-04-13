DROP DATABASE IF EXISTS __DBNAME__;

CREATE DATABASE __DBNAME__;

USE __DBNAME__;

CREATE TABLE IF NOT EXISTS users (
    `id` int AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `username` varchar(255) NOT NULL UNIQUE,
    `email` varchar(255) NOT NULL UNIQUE,
    `telephone` varchar(255) UNIQUE,
    `password` varchar(255) NOT NULL,
    `permission_level` int DEFAULT 0,
    `role` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);
