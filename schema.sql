DROP DATABASE IF EXISTS __DBNAME__;

CREATE DATABASE __DBNAME__;

USE __DBNAME__;


CREATE TABLE IF NOT EXISTS empresa (
    `id` int AUTO_INCREMENT PRIMARY KEY,
    `name` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS user (
    `id` int AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `username` varchar(255) NOT NULL UNIQUE,
    `email` varchar(255) NOT NULL UNIQUE,
    `telephone` varchar(255) UNIQUE,
    `password` varchar(255) NOT NULL,
    `permission_level` int DEFAULT 0,
    `role` varchar(255) NOT NULL,
    `enterprise_id` int REFERENCES empresa(`id`),
    PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS imovel (
    `id` int AUTO_INCREMENT,
    `enterprise_id` int NOT NULL REFERENCES empresa(`id`),
    `valor_aluguel` float,
    `valor_venda` float,
    `taxa_adm_mensal` float,
    `taxa_locacao` float,
    `cep` varchar(255) NOT NULL,
    `endereco` varchar(255) NOT NULL,
    `numero` int, -- pode ser NUL caso não haja número
    `complemento` varchar(255),
    `bairro` varchar(255) NOT NULL,
    `cidade` varchar(255) NOT NULL,
    `estado` varchar(255) NOT NULL,
    `tipo` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS morador (
    `id` int AUTO_INCREMENT,
    `nome` varchar(255) NOT NULL,
    `cpf` varchar(11) NOT NULL,
    `telefone` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `imovel_id` int NOT NULL REFERENCES imovel(`id`),
    `enterprise_id` int NOT NULL REFERENCES empresa(`id`),
    `prazo_tolerancia` int NOT NULL,
    `prazo_medidas_legais` int NOT NULL,
    `data_inicio` date NOT NULL,
    `data_termino` date NOT NULL,
    `data_pagamento` date NOT NULL, -- sentido de "proxima data de pagamento"
    `status` tinyint NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS pagamento (
    `id` int AUTO_INCREMENT,
    `morador_id` int NOT NULL REFERENCES morador(`id`),
    `valor_pago` float NOT NULL,
    `data_pagamento` date NOT NULL,
    `is_delayed` tinyint NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS feature (
    `id` int AUTO_INCREMENT,
    `category` varchar(255) NOT NULL,
    `min_perm_level` int NOT NULL,
    `description` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    `import_url` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);