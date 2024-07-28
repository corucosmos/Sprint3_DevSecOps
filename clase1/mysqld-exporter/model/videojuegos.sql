CREATE TABLE videojuegos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    genero VARCHAR(100),
    plataforma VARCHAR(100),
    precio DECIMAL(10,2)
);

INSERT INTO videojuegos (nombre, genero, plataforma, precio) VALUES
('FIFA 21', 'Deportes', 'PlayStation 4', 69.99),
('The Legend of Zelda: Breath of the Wild', 'Aventuras', 'Nintendo Switch', 59.99),
('Animal Crossing: New Horizons', 'Simulación', 'Nintendo Switch', 49.99),
('Cyberpunk 2077', 'RPG', 'PC', 59.99),
('Super Mario 3D All-Stars', 'Plataformas', 'Nintendo Switch', 59.99),
('The Last of Us Part II', 'Aventuras', 'PlayStation 4', 69.99);
