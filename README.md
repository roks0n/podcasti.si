# Podcasti.si
Najvecja zbirka slovenskih podcastov. Stran namenjena odkrivanju podcastov iz nase dezele.

## Contributions
### 🤓 Code
Feel free to open as many PRs as you want. 💪

Obstaja tudi [public todo lista](https://trello.com/b/uiI85sUB/podcastisi). Ce ti je kak task vsec, se [joinaj](https://trello.com/invite/b/uiI85sUB/4bc0d20f964b10b8ba70a84975fbee55/podcastisi) in assignaj na task. V primeru vprasanj in morebitnih usmeritev poslji msg @roks0n. Vsakega odprtega PRa bom zelo vesel in se maksimalno potrudil, da ga pogledam v roku 24h. :)

### ❓ Manjka podcast?
V primeru da manjka podcast, ga je potrebno rocno vnesti. Lahko posljes request na [te formi](https://rksn.typeform.com/to/EljGwv).

### 💡 Ideas
Ce imas idejo jo lahko dodas na [Trello](https://trello.com/b/uiI85sUB/podcastisi), vendar se moras prijaviti v team s [tem linkom](https://trello.com/invite/b/uiI85sUB/4bc0d20f964b10b8ba70a84975fbee55/podcastisi).
Spudbujamo tudi **glasovanje na ideje**, kar bo olajsalo prioritizacijo taskov.

#### Navodila za kreiranje ticketa
1. Prijavi se v Trello (v kolikor se nisi, se moras registrirati)
2. Joinaj board s [tem linkom](https://trello.com/invite/b/uiI85sUB/4bc0d20f964b10b8ba70a84975fbee55/podcastisi)
3. Idejo/feature request dodaj pod stolpec "Feature requests/Ideas"
4. Napisi kratek in razumljiv title
5. Napisi strnjen in natancen decription. V kolikor ocenis da bo pomagalo, dodaj se linke do primerov ali attachment (sliko/video).

**Nerazumljivi ticketi bodo izbrisani.**

## Kako pognati podcasti.si lokalno?
Potrebujes Docker in docker-compose

1. run `make dev-bootstrap` - zbuilda project
2. run `make superuser` - kreiraj si super userja, ki ga bos uporabil za dostop do administracije
3. run `make runserver` - pozene stran, ki jo lahko obisces na http://localhost:8000

### Ostalo
V admin panel se logiras na: http://localhost:8000/admin - vpisi username in password, ki si ga izbral pri 2. koraku
Ce si dodal podcaste in jih zelis syncati pozeni: `make sync-podcasts`
