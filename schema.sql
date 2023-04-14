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

CREATE TABLE IF NOT EXISTS moradias (
    `id` int AUTO_INCREMENT,
    `client_id` int NOT NULL REFERENCES users(`id`),
    `value` int NOT NULL,
    `address` varchar(255) NOT NULL,
    `type` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS inquilinos (
    `id` int REFERENCES users(`id`),
    `name` varchar(255) NOT NULL,
    `telephone` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `moradia_id` int NOT NULL REFERENCES moradias(`id`),
    `taxa_juros` float NOT NULL DEFAULT 0.2,
    `data_vencimento` date NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS pagamentos (
    `id` int AUTO_INCREMENT,
    `inquilino_id` int NOT NULL REFERENCES inquilinos(`id`),
    `value` int NOT NULL,
    `data_vencimento` date NOT NULL,
    `data_pagamento` date,
    PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS features (
    `id` int AUTO_INCREMENT,
    `category` varchar(255) NOT NULL,
    `min_perm_level` int NOT NULL,
    `description` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    `import_url` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);