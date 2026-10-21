-- Opcional: a API já cria a tabela sozinha. Use no MySQL Workbench se quiser dados de teste.
CREATE TABLE IF NOT EXISTS produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);

INSERT INTO produto (descricao, preco) VALUES
('Teclado Logitech K120', 89.90),
('Mouse Microsoft Basic', 54.50),
('Monitor Samsung 24"', 899.99),
('SSD Kingston 480GB', 450.00),
('Cabo HDMI 2m', 39.90);
