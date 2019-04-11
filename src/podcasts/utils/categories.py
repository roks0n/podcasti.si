"""
Games & Hobbies - Igre in hobiji - igre-in-hobiji-podcasti
Society & Culture - Družba in kultura - druzbeni-in-kulturni-podcasti
Business - Posel - poslovni-podcasti
News & Politics - Novice in politika -  novicarski-in-politicni-podcasti
Arts - Umetnost - umetnostni-podcasti
Technology - Tehnologija - tehnoloski-podcasti
Science & Medicine - Znanost in medicina - znanost-in-medicina-podcasti
Kids & Family - Otroci in druzina - otroski-in-druzinski-podcasti
Government & Organizations - Vlade in organizacije - vladni-in-organizacijski-podcasti
Sports & Recreation - Šport in rekreacija - sport-in-rekreacija-podcasti
Education - Izobraževanje - izobrazevalni-podcasti
TV & Film - TV in film - tv-in-filmski-podcasti
Comedy - Komedija - komicni-podcasti
Music - Glasba - glasbeni-podcasti
"""

CATEGORIES_TRANSLATIONS = {
    "Games & Hobbies": "Igre in hobiji",
    "Society & Culture": "Družba in kultura",
    "Business": "Posel",
    "News & Politics": "Novice in politika",
    "Arts": "Umetnost",
    "Technology": "Tehnologija",
    "Science & Medicine": "Znanost in medicina",
    "Kids & Family": "Otroci in družina",
    "Government & Organizations": "Vlade in organizacije",
    "Sports & Recreation": "Šport in rekreacija",
    "Education": "Izobraževanje",
    "TV & Film": "TV in film",
    "Comedy": "Komedija",
    "Music": "Glasba",
}

PODCAST_CATEGORIES_TO_SLUGS = {
    "Games & Hobbies": "igre-in-hobiji-podcasti",
    "Society & Culture": "druzbeni-in-kulturni-podcasti",
    "Business": "poslovni-podcasti",
    "News & Politics": "novicarski-in-politicni-podcasti",
    "Arts": "umetnostni-podcasti",
    "Technology": "tehnoloski-podcasti",
    "Science & Medicine": "znanost-in-medicina-podcasti",
    "Kids & Family": "otroski-in-druzinski-podcasti",
    "Government & Organizations": "vladni-in-organizacijski-podcasti",
    "Sports & Recreation": "sport-in-rekreacija-podcasti",
    "Education": "izobrazevalni-podcasti",
    "TV & Film": "tv-in-filmski-podcasti",
    "Comedy": "komicni-podcasti",
    "Music": "glasbeni-podcasti",
}

EPISODE_CATEGORIES_TO_SLUGS = {
    "Games & Hobbies": "igre-in-hobiji-epizode",
    "Society & Culture": "druzbene-in-kulturne-epizode",
    "Business": "poslovne-epizode",
    "News & Politics": "novicarske-in-politicne-epizode",
    "Arts": "umetnostne-epizode",
    "Technology": "tehnoloske-epizode",
    "Science & Medicine": "znanost-in-medicina-epizode",
    "Kids & Family": "otroske-in-druzinske-epizode",
    "Government & Organizations": "vladne-in-organizacijske-epizode",
    "Sports & Recreation": "sport-in-rekreacija-epizode",
    "Education": "izobrazevalne-epizode",
    "TV & Film": "tv-in-filmske-epizode",
    "Comedy": "komicne-epizode",
    "Music": "glasbene-epizode",
}

PODCAST_SLUGS_TO_CATEGORIES = {
    slug: category for category, slug in PODCAST_CATEGORIES_TO_SLUGS.items()
}

EPISODE_SLUGS_TO_CATEGORIES = {
    slug: category for category, slug in EPISODE_CATEGORIES_TO_SLUGS.items()
}
