# Task

Process a Wiktionary dump to extract synonym relations for a random language (not English, Ukrainian or Russian :). 
You can find the latest dumps at https://dumps.wikimedia.org/backup-index.html. The task requires application of 
XML SAX parsing.

# Solution

Here you can find code for downloading and processing German Wiktionary file. 
Class xml.etree.ElementTree in iterative mode is used for XML processing.

0. Please, install requirements.txt
0. Run in folder AcquisitionAndAnalysis following command:

```python 01-Wiktionary/get_german_synonims.py```

# Results

Downloaded, unpacked files and synonyms list can be found in directory 

```01-Wiktionary/data```

Archive with collected sets of synonyms also can be found in the file 

```01-Wiktionary/dewiktionary-20190301-pages-articles-multistream.syn.txt.zip```

A little statistics about found synonyms (output of the running program):

```
Found terms with synonyms: 42056
The longest set has length 157
['Matte', 'Allgemeine', 'Alma', 'Amüsiermädchen', 'Amüsiermatratze', 'Anschaffefrau', 
'Bein', 'Berufsamüsiererin', 'Berufsmäßige', 'Beserl', 'Bettmaid', 'Biene', 'Bolzen', 
'Briefkasten', 'Bruchbiene', 'Brunzwinkel', 'Bumsmädchen', 'Dämchen', 
'Dame/Dame vom Dienst/Dame des öffentlichen Dienstes/Dame fürs Geld/ Dame des ältesten Gewerbes/Dame des ältesten Gewerbes der Welt/Dame des leichten Gewerbes/Dame minderen Gewichts/Dame der zehnten Muse/Dame mit dem unaussprechlichen Namen/Dame der ältesten Zunft der Welt/Dame von der flotten Zunft/Dame von der leichten Zunft/horizontale Dame/käufliche Dame/leichte Dame/öffentliche Dame/professionelle Dame/schräge Dame/vorübergehende Dame/eindeutig zweideutige Dame', 
'Dienerin des horizontalen Gewerbes/Dienerin der Liebe/Dienerin der käuflichen Liebe', 
'Diensleistungsdame', 'Dienstmädchen/Dienst-Mädchen', 'Donna', 'Dosenverkäuferin', 
'Dulle', 'Ekelkörper', 'horizontal Erwerbstätige', 'Fahrrad', 'Fetze', 'Fliege', 
'Flinte', 'F-Loch', 'Flöte', 'Frau auf Zeit', 'Fraulein/Fräulein', 'Freudenfrau', 
'Freudenmädchen', 'Freundin gegen bar/Freundin für Geld', 'Fuchtel', 'Futt', 'Gammel', 
'Gänsefüßchen-Dame', 'Geige', 'Geigenspielerin', 'Geldkatze', 'Gemse', 'Genussdame', 
'Geschlechtskatze', 'Gesellschaftsdame', 'Gunstgewerblerin', 'hwG-Frau', 'Hackbraten', 
'Halbschwergewicht', 'Halbweltlerin', 'Hatsche', 'Haut', 'Hoppemädchen', 
'Horizontalgewerblerin', 'Horizontalhostess', 'Hostess', 'Hübschlerin', 'Huhn', 
'Hüpferl', 'Intimsportlerin', 'Juchhe-Dame', 'Kalle', 'Kätzchen', 'Katze', 'Kauffrau', 
'Kletterhanne', 'Kletterjule', 'Kobelmädchen', 'Kuh', 'Leihdame', 'Leihkörper', 
'Leisten', 'Lustmatratze', 'Mädchen für alle', 'Mädchen vom Dienst/M.v.D.', 
'Mädchen der Liebe', 'Mädchen von der leichtesten Tugend', 'allgemeingültiges Mädchen', 
'halbseidenes Mädchen', 'horizontales Mädchen', 'leichtes Mädchen', 'Matratze', 'Metze', 
'Mietsche', 'Mieze', 'Miss Gunst', 'Modell', 'Möse', 'Motte', 'Muschi', 'Nachthyäne', 
'Nachtmensch', 'Nagel', 'Nähmaschine', 'Nelke', 'Nickel', 'Nymphe', 'Öffentliche', 
'Omnibus', 'P. P.', 'Pflaumenhandlung', 'Pimperliese', 'Pimpernelle', 'Presslusthammer', 
'Pritsche', 'Professionelle', 'Profi/Profi-Katze', 'Rabe', 'Ratte', 'Reitpferd', 
'Samenräuber', 'Schickse', 'Schinken', 'Schlampe/Schlampen', 'Schlapfen', 'Schleuse', 
'Schlitten', 'Schnalle', 'Schöne der Nacht', 'barmherzige Schwester/mitleidige Schwester', 
'Sexgewerblerin', 'Sexmaschine', 'Sexualdemokratin', 'Sexualhelferin', 'Solchene', 
'Spritzbüchse', 'Spritze', 'Staude', 'Steckdose', 'Stück', 'Stundenfrau', 'Stute', 
'Sumpfblüte', 'Tebe', 'Tilla/Tille', 'Töle', 'Truhe', 'Tülle', 'Tülpchen', 'Unke', 
'Uschi', 'Vergnügungsspenderin', 'öffentliches Verkehrsmittel', 'Viertelstundenlöhnerin', 
'Volksempfängerin', 'Vorführdame', 'Wachtel', 'Wanze', 'sündige Ware', 'Zahn', 
'professionelle Zeitvertreiberin', 'Zibbe', 'Zusel']
```