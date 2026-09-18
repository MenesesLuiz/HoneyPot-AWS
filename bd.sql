CREATE DATABASE IF NOT EXISTS honeypot;
USE honeypot;

CREATE TABLE IF NOT EXISTS registro_ataques (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(45) NOT NULL,
    usuario VARCHAR(50) NOT NULL,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_registro_ataques_data_hora (data_hora),
    INDEX idx_registro_ataques_ip (ip)
);
