from django.core.management.base import BaseCommand

from podcasts.models import Podcast
from podcasts.utils.logger import get_log

log = get_log(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        podcasts = ['Tandem', 'Časnik Finance, poslovni dnevnik', 'Vagabundi', 'Spetek', 'Mali podcast', 'Številke', 'IMEnitno', 'Metamorfoza', 'Petkova centrifuga', 'Življenje in jaz', 'Cosmo podcast', 'Digital Mafia', 'IN MEDIA RES', 'Večer', 'Filozofija gre v svet', 'Filip Pesek Live', 'Kofirajd', 'Neustavljiv', 'Torpedo', 'Kampanja', 'SOS odmevi', 'Metadekleta', 'Zakulisje', 'O.B.O.D.', 'Student.si', 'AIDEA', 'POINT OUT Weekly', 'Fejmiči', 'Koronavirus podkast', 'Dvokorak', '#Ofsajd', 'Ta hitri', 'Avanture, Miha Ahačič podcast', 'Sopotnik', '3rd and 36: NFL podcast z Rokom Grilcem', 'Tajno društvo OFC', 'Opazovalnica', 'Glave', 'Bojana in Luka - Družinski podcast', 'Pot v raj', 'Filmstart', 'Suspenzor', 'Toplovod', 'Membranje', 'Vroči mikrofon', 'Mladina', 'Od genov do zvezd', 'Apparatus pogovori', 'InternetWeek.SI', 'Dober poskus', 'Marigor', 'Podjetniške Skrivnosti', 'Apgrejd', 'Pod Črto', 'Odbita do bita', 'Frekvenca X', 'Fotkas', 'SBS Slovenian', 'Popkulturni pogovori', 'Na potezi', 'Jezikanje', 'Forum 69', 'Bitni pogovori', 'Lahko noč, otroci!', 'Tranzistorij', 'Evropska četrt', 'LD;GD', 'Žoga je okrogla', 'GO4GOAL', 'Kunapipi', 'Nehvaležni skeptiki', 'Metin čaj', 'Parallel Passion', 'Nebuloze', 'Intelekta', 'Kje pa vas čevelj žuli', 'ARSO Podcast', 'Podrobnosti', 'Lahkonočnice', 'Do mikrofona v #vblatu', 'Reneseansa - Casual Friday Podcast', 'Državljan D', 'Knedl Fura', 'A res, tega ne veš?', 'Znanost dobrega počutja', 'Radio Ga Ga', 'Latrina', 'Strašno hudi', 'Radio Ritem', 'Iskreni', 'BIMpogovori', 'Futurist', 'Bedarije', 'Direktorjeva perspektiva', 'Lovim ravnotežje', 'Tehno klistir', 'FilmFlow', 'Na svoji strani', 'Idrijske Novice Studio', 'Zgodbe', 'Zapisi iz močvirja', 'Malinca Lifestyle', 'ODPRTO, podkast o prostoru', 'Znanost na cesti', 'Klepet ob Kavi', 'Sportinfo', 'Govori molk', 'Od srede do srede', 'Avtomat', 'Meta PHoDcast', 'TourismFromZero', 'Opravičujemo se za vse nevšečnosti', 'Globalna vas', 'samopostrezna.com', 'Garaža, festival mobilnosti', 'Teniški Podcast', 'Gravitacija', "Klemen Bec's Podcast", 'Glass Balloons', 'Fotr Fotru', 'Nasveti učiteljice Nine', 'Možgani na dlani: nevron pred mikrofon', 'Gospoda', 'Ljudska pamet', 'Špilferderber']
        for name in podcasts:
            Podcast.objects.create(name=name)
