# Projet P2I-2 2023 : <br/> GET BETTER AT PIANO !

(Un gant pour ~~pour les gouverner tous~~ apprendre à jouer au piano)*

## Description du projet

Notre projet de Parcours d'Initiation à l'Ingénierie est un gant équipé de capteur permettant de s'améliorer au piano.

<div align="center">
    <img src=Images/gant.png width=400>
</div> &nbsp;

Le concept est realtivement simple : Nous avons une ✨*magnifique*✨  application faisant défiler les touches sur lesquelles l'on doit appuyer tout au long du morceau. 

Pendant ce temps le gant et le micro vont enregistrer de nombreuses informations (fréquence, pression sur les doigts, accélération de la main, fréquence cardiaque, etc) qui sont envoyées à l'application. 

<div align="center">
    <img src=Images/play_mode.gif width=400>
</div> &nbsp;

À la fin du morceau, les données du micro et du gant sont mises en commun pour déterminer notamment quelles touches sont pressées, à quel moment et avec quel doigt. 
On fait alors 3 choses : l'envoi des données à la base de données, une comparaison avec les note de références qui défilaient pour déterminer le nombre de fausses notes, et enfin, on passe les données à un arbre de décision préalablement entrainé pour nous donner une estimation du niveau sur la performance réalisée.

Et la dernière fonctionnalitée mais non des moindres : un mode replay de la performance. Dans ce mode, les touches jouées *(en couleur et avec une couleur différente pour chaque doigt)* vont défiler en même temps que les touches de référence *(contours noires)* pour pouvoir comparer visuellement et voir où sont les erreurs.

<div align="center">
    <img src=Images/replay_mode.gif width=400>
</div> &nbsp;

## Détails techniques

### Application Python

L'application est réalisée en python avec  [tkinter](https://docs.python.org/3/library/tkinter.html) comme interface graphique.

#### Libraries utilisées

- [tkinter](https://docs.python.org/3/library/tkinter.html) : Interface graphique

- [matplotlib](https://matplotlib.org/) : Graphiques de retour sur la performance

- [mysql-connector-python](https://github.com/mysql/mysql-connector-python) : Communication avec la base de données

- [pyserial](https://github.com/pyserial/pyserial) : Communication avec les cartes Arduino

- [pandas](https://pandas.pydata.org/) : Dataframes

- [scikit-learn](https://github.com/scikit-learn/scikit-learn) : Arbre de Décision et KNN

### Cartes Arduino

Ce projet utilise 3 cartes Arduino : 1 [Arduino Uno](https://store.arduino.cc/products/arduino-uno-rev3-smd) et 2 [Arduino MKR WAN 1310](https://store.arduino.cc/products/arduino-mkr-wan-1310). Elle est connectée par liason série à l'ordinateur et notre application

La carte UNO est utilisée uniquement pour le micro afin de pouvoir faire de l'analyse fréquencielle plus rapidement que sur une MKR WAN (voir [Analyse fréquencielle du signal du micro](#analyse-fréquencielle-du-signal-du-micro)).

<div align="center">
    <img src=Images/micro.png width=400>
</div> &nbsp;

La première carte MKR WAN est celle du gant. Elle est en charge de récupérer toute les données des capteurs puis de les envoyer par communication [LoRa](https://fr.wikipedia.org/wiki/LoRaWAN#Modulation_LoRa) à la seconde MKR WAN qui va finalement les transmettre par liaison série à notre application.

#### Libraries utilisées

- [RadioLib](https://github.com/jgromes/RadioLib) : Communication LoRa

- [Seeed Arduino LSM6DS3](https://github.com/Seeed-Studio/Seeed_Arduino_LSM6DS3) : Accéléromètre 6 axes

- [Fixed16FFT](https://github.com/Klafyvel/AVR-FFT) : Transformation de Fourier pour  [l'analyse fréquencielle du micro](#analyse-fréquencielle-du-signal-du-micro)

### Capteurs de pression

Pour chaque capteur de pression ([Flexiforce©](https://www.gotronic.fr/art-capteurs-de-force-flexiforce-0-45kg-12138.htm)), le signal est traité par un circuit conditionneur réalisé par nos soins utilisant un [AOP](https://fr.wikipedia.org/wiki/Amplificateur_op%C3%A9rationnel).

C'est à cela que servent tout les composants sur la [breadboard](#description-du-projet).

### Analyse fréquencielle du signal du micro

Pour passer du signal de volume sonore du micro à connaître quelle touche du piano est préssée, on réalise une analyse fréquencielle du signal avec une [FFT](https://fr.wikipedia.org/wiki/Transformation_de_Fourier_rapide) pour déterminer les fréquences de plus grandes amplitudes et donc celles principales.

Le passage de la fréquence à la note jouée se fait dans l'application python lorsqu'elle reçoit les données.

La [librairie de FFT utilisée](https://github.com/polo-diemunsch/projet-p2i/blob/main/Arduino/Micro/Fixed16FFT.h) est celle implémentée par [Klafyvel](https://github.com/Klafyvel/AVR-FFT) et que j'ai légèrement modifié pour correspondre à notre cas d'utilisation. En effet, on ne cherche pas seulement la fréquence principale mais les 5 de plus grandes amplitudes pour pouvoir détecter l'appui de plusieurs touches en même temps.

Malgré toutes les optimisations implémentées dans la library, sur une carte MKR WAN effectuer une FFT de 512 valeurs chacune codée sur 16 bits prennait 50 à 100 ms et donc beaucoup trop long pour notre utilisation (certaines notes durent moins de 100 ms).
On a donc utilisé une carte UNO spécialement pour le micro car elle pouvait faire la FFT entre 12 et 16 ms, ce qui était suffisant pour notre application.

## Disclaimer

Le gant a été démonté à la fin du semestre et la base de données sera supprimée. Ce repo sert donc de compte rendu et peut être une inspiration mais le projet en lui même n'est maintenant plus utilisable en tant que tel.

## Auteurs

- **[Polo](https://github.com/polo-diemunsch)**
- **[Arthur](https://github.com/JostDoit)**
- **[Armand](https://github.com/armandp2t)**
- **[Arno](https://github.com/avenaille)**
- **[Marc-Antoine](https://github.com/marcoandchill)**
- **[Elouan](https://github.com/ElouanBul)**
