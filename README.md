# Podcasti.si
Najvecja zbirka slovenskih podcastov. Stran namenjena odkrivanju podcastov iz nase dezele.

## Contributions
### 🤓 Code
Feel free to open as many PRs as you want. 💪

Za idejo kje pomagati, si lahko [pogledas tudi odpre "taske"](https://github.com/roks0n/podcasti.si/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22). V primeru vprasanj in morebitnih usmeritev poslji msg @roks0n. Vsakega odprtega PRa bom zelo vesel in se maksimalno potrudil, da ga pogledam v roku 24h. :)

### ❓ Manjka podcast?
V primeru da manjka podcast, ga je potrebno rocno vnesti. Lahko posljes request na [te formi](https://rksn.typeform.com/to/EljGwv).

### 💡 Ideas
Ce imas idejo jo lahko dodas pod Github Issue ali pisi @roks0n na Twitter.

#### Navodila za kreiranje ticketa
1. Kreiraj Github Issue
2. Napisi kratek in razumljiv title
3. Napisi strnjen in natancen decription. V kolikor ocenis da bo pomagalo, dodaj se linke do primerov ali attachment (sliko/video).

**Nerazumljivi issue-i bodo izbrisani.**

## Kako pognati podcasti.si lokalno?
Potrebujes Docker in docker-compose

1. run `make dev-bootstrap` - zbuilda project
2. run `make superuser` - kreiraj si super userja, ki ga bos uporabil za dostop do administracije
3. run `make runserver` - pozene stran, ki jo lahko obisces na http://localhost:8000

### Ostalo
V admin panel se logiras na: http://localhost:8000/admin - vpisi username in password, ki si ga izbral pri 2. koraku
Ce si dodal podcaste in jih zelis syncati pozeni: `make sync-podcasts`
