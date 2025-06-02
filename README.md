# DnD-Group-finder

## Sovelluksen toiminnot
* Sovelluksessa käyttäjät pystyvät etsiä pelejä tai pelaajia peleihinsä.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen peliryhmän. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään peliryhmiä.
* Käyttäjä näkee sovellukseen lisätyt peliryhmät. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät peliryhmät.
* Käyttäjä pystyy etsimään tietokohteita hakutermeillä. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä peliryhmiä.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä heidän tekemänsä pelit.
* Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun (esim. pelikokemuksen määrä, pelin taso) ja maksimi pelaaja määrän.
* Käyttäjä pystyy ilmoittautumaan muiden vetämiin peliryhmiin pelaajaksi jos niissä on tilaa. Ilmoituksessa näytetään, ketkä pelaajat ovat ilmoittautuneet ja muita olennaisia tietoja kyseisestä peliryhmästä.
* Käyttäjä pystyy poistamaan ilmoittautumisen jos se on hänen tekemä peli tai jos se on oma ilmoittautuminen.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
