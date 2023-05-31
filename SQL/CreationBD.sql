
DROP TABLE IF EXISTS MesureBPM;
DROP TABLE IF EXISTS MesureAccelero;
DROP TABLE IF EXISTS MesureTouche;
DROP TABLE IF EXISTS Performance;
DROP TABLE IF EXISTS Musicien;
DROP TABLE IF EXISTS ToucheRef;
DROP TABLE IF EXISTS Morceau;

CREATE TABLE Morceau (
  idMorceau INT(10) AUTO_INCREMENT,
  titre VARCHAR(100) NOT NULL,
  bpmMorceau INT(3),
  PRIMARY KEY (idMorceau)
);

CREATE TABLE ToucheRef (
  idTouche INT(10) AUTO_INCREMENT,
  idMorceau INT(10) NOT NULL,
  note INT(2) NOT NULL,
  tpsPresse DECIMAL(5, 3) NOT NULL,
  tpsDepuisDebut DECIMAL(5, 3) NOT NULL,
  PRIMARY KEY (idTouche),
  FOREIGN KEY (idMorceau) REFERENCES Morceau(idMorceau)
);

CREATE TABLE Musicien (
  idMusicien INT(10) AUTO_INCREMENT,
  nom VARCHAR(100) NOT NULL,
  niveau VARCHAR(100),
  PRIMARY KEY (idMusicien)
);

CREATE TABLE Performance (
  idPerf INT(10) AUTO_INCREMENT,
  idMusicien INT(10) NOT NULL,
  idMorceau INT(10) NOT NULL,
  datePerf DATETIME NOT NULL,
  nbFaussesNotes INT(10),
  nbNotesTotal INT(10),
  bpmMoy INT(3),
  niveauEstime VARCHAR(100),
  PRIMARY KEY (idPerf),
  FOREIGN KEY (idMusicien) REFERENCES Musicien(idMusicien),
  FOREIGN KEY (idMorceau) REFERENCES Morceau(idMorceau)
);

CREATE TABLE MesureTouche (
  idMesureTouche INT(10) AUTO_INCREMENT,
  idPerf INT(10) NOT NULL,
  note INT(2) NOT NULL,
  doigt INT(1) NOT NULL,
  tpsPresse DECIMAL(5, 3) NOT NULL,
  tpsDepuisDebut DECIMAL(5, 3) NOT NULL,
  PRIMARY KEY (idMesureTouche),
  FOREIGN KEY (idPerf) REFERENCES Performance(idPerf)
);

CREATE TABLE MesureAccelero (
  idMesureAccelero INT(10) AUTO_INCREMENT,
  idPerf INT(10) NOT NULL,
  valeurX INT(6) NOT NULL,
  valeurY INT(6) NOT NULL,
  tpsDepuisDebut DECIMAL(5, 3) NOT NULL,
  PRIMARY KEY (idMesureAccelero),
  FOREIGN KEY (idPerf) REFERENCES Performance(idPerf)
);

CREATE TABLE MesureBPM (
  idMesureBPM INT(10) AUTO_INCREMENT,
  idPerf INT(10) NOT NULL,
  valeur INT(3) NOT NULL,
  tpsDepuisDebut DECIMAL(5, 3) NOT NULL,
  PRIMARY KEY (idMesureBPM),
  FOREIGN KEY (idPerf) REFERENCES Performance(idPerf)
);
