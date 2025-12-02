USE fitbite;

CREATE TABLE preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    p1 VARCHAR(255) NOT NULL,
    p2 VARCHAR(255) NOT NULL,
    p3 VARCHAR(255) NOT NULL,
    p4 VARCHAR(255) NOT NULL,
    p5 VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_respuestas_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
);
