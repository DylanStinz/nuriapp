USE fitbite;
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(150) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nacimiento DATE,
    genero ENUM('mujer','hombre','personalizado'),
    altura INT,
    actual INT,
    objetivo INT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);