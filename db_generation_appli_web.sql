CREATE DATABASE IF NOT EXISTS `appli_web` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `appli_web`;

DROP TABLE IF EXISTS `slide`;
CREATE TABLE IF NOT EXISTS `slide` (
  `slide_id` int(11) NOT NULL AUTO_INCREMENT,
  `slide_titre` varchar(100) NOT NULL,
  `slide_auteur` varchar(100) NOT NULL,
  `slide_date` date NOT NULL,
  `slide_description` text NOT NULL,
  `slide_lien` varchar(100) NOT NULL,
  PRIMARY KEY (`slide_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;


TRUNCATE TABLE `slide`;


INSERT INTO `slide` (`slide_id`, `slide_titre`, `slide_auteur`, `slide_date`, `slide_description`, `slide_lien`) VALUES
(1, 'POO', 'Alexandre Dubois', '2017-04-13', 'POO en java', 'http://slides.com/alexandredubois/introduction-a-la-programmation-orientee-objet/'),
(3, 'Réseau', 'Donat Fuzellier', '2017-04-21', 'Cours de réseau', 'https://www.google.fr/'),
(5, 'Java', 'Arnaud De Villedon', '2017-04-21', 'Java 4 ever 3', 'https://www.java.com/fr/'),
(6, 'SQL', 'Sébastien Vita', '2017-04-21', 'Big big big data', 'https://fr.wikipedia.org/wiki/Structured_Query_Language'),
(7, 'Javascript', 'Jean-Baptiste Cordovado', '2017-04-15', 'Cours JS', 'https://openclassrooms.com/courses/dynamisez-vos-sites-web-avec-javascript');

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_pseudo` varchar(100) NOT NULL,
  `user_password` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;



TRUNCATE TABLE `user`;

INSERT INTO `user` (`user_id`, `user_pseudo`, `user_password`) VALUES
(1, 'appli_web', '$2y$10$UO/d399Bms5L4IbY2VGf.OpbeiLN3iGqXXS5SUQDTQ1E5OZ2GOsD2'),
(2, 'root', '$2y$10$YLF32CnZtkKF3yI1.Irg4udJopmpVCAG1N3DmFL1E9kWIowSZYp0K');
