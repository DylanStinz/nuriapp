-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.4.7 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.13.0.7147
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para fitbite
CREATE DATABASE IF NOT EXISTS `fitbite` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `fitbite`;

-- Volcando estructura para tabla fitbite.preguntas
CREATE TABLE IF NOT EXISTS `preguntas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `p1` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `p2` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `p3` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `p4` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `p5` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_respuestas_usuario` (`usuario_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fitbite.preguntas: 1 rows
DELETE FROM `preguntas`;
/*!40000 ALTER TABLE `preguntas` DISABLE KEYS */;
INSERT INTO `preguntas` (`id`, `usuario_id`, `p1`, `p2`, `p3`, `p4`, `p5`) VALUES
	(1, 1, 'Pregunta1: Perder peso', 'Pregunta 2: Para mejorar mi salud en general', 'Pregunta 3: Sentirme bien con mi cuerpo', 'Pregunta 4: Ninguno', 'Pregunta 5: Ninguno');
/*!40000 ALTER TABLE `preguntas` ENABLE KEYS */;

-- Volcando estructura para tabla fitbite.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `correo` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `nacimiento` date DEFAULT NULL,
  `genero` enum('mujer','hombre','personalizado') COLLATE utf8mb4_general_ci DEFAULT NULL,
  `altura` int DEFAULT NULL,
  `actual` int DEFAULT NULL,
  `objetivo` int DEFAULT NULL,
  `creado_en` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla fitbite.usuarios: 1 rows
DELETE FROM `usuarios`;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `correo`, `password_hash`, `nacimiento`, `genero`, `altura`, `actual`, `objetivo`, `creado_en`) VALUES
	(1, 'Tilin', 'Alvarez', '123@gmail.com', 'scrypt:32768:8:1$JT2Ts0vnLIjsjs48$b5812c896d95b5335bc9529ea2d254b4c0d1a0c383255695b5de6df2327ce9e0a9f43dff9ddb7421afc1b6b4dd04a07b5d62f470d73fdf36ff5537477a66a5f9', '2025-12-06', 'hombre', 180, 80, 75, '2025-12-01 22:02:02');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
