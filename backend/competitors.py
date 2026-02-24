"""
Competitor configuration for Mosaic Wellness brands.

JUSTIFICATION:
--------------
BeBodywise (Women's Health & Wellness Supplements):
  - Pilgrim, Mamaearth, Dot & Key, Plum, Minimalist, WOW Skin Science, mCaffeine, Nykaa Beauty
  - Rationale: All target Indian women aged 22-40, sell D2C via website + Amazon/Nykaa,
    use similar channels (Instagram, Facebook), compete in supplements + skincare.

Man Matters (Men's Grooming, Sexual Wellness, Dermatology):
  - The Man Company, Bombay Shaving Company, Beardo, USTRAA, Traya, Vedix, OZiva, BoldFit
  - Rationale: Overlap in men's wellness, hair fall treatments, sexual health products.
    Traya and Vedix directly compete in hair solutions. The Man Company/BSC in grooming.

Little Joys (Kids' Nutrition & Wellness):
  - Mamaearth (baby), Himalaya Wellness, Bey Bee, Chicco India, Horlicks, Complan, Protinex Junior
  - Rationale: All target parents of kids 0-12 in India, sell nutrition supplements/daily care.
    Horlicks/Complan dominate traditional — Little Joys competes on D2C modern positioning.
"""

BRANDS = {
    "bebodywise": {
        "display_name": "Be Bodywise",
        "category": "Women's Health & Wellness",
        "target_audience": "Women, 22-40, urban India",
        "own_page_id": None,  # Add if known
        "competitors": [
            {
                "name": "Pilgrim",
                "page_search_term": "Pilgrim India skincare",
                "category": "Women's Skincare & Wellness",
                "justification": "Direct overlap in women's skincare + hair supplements; same D2C model, Instagram-heavy"
            },
            {
                "name": "Mamaearth",
                "page_search_term": "Mamaearth",
                "category": "Women's Skincare & Wellness",
                "justification": "Largest D2C competitor in India; competes across skincare, hair, supplements"
            },
            {
                "name": "Dot & Key",
                "page_search_term": "Dot and Key skincare",
                "category": "Women's Skincare",
                "justification": "Women's skincare brand; similar audience; acquired by Nykaa"
            },
            {
                "name": "Plum Goodness",
                "page_search_term": "Plum Goodness",
                "category": "Women's Skincare",
                "justification": "Vegan skincare brand targeting same urban Indian women segment"
            },
            {
                "name": "Minimalist",
                "page_search_term": "Minimalist skincare India",
                "category": "Women's Skincare",
                "justification": "Science-backed skincare, strong digital ads, same demographics"
            },
            {
                "name": "WOW Skin Science",
                "page_search_term": "WOW Skin Science",
                "category": "Women's Wellness",
                "justification": "Heavy FB/Insta ad spender; overlaps in hair care + supplements"
            },
            {
                "name": "mCaffeine",
                "page_search_term": "mCaffeine",
                "category": "Women's Skincare",
                "justification": "D2C brand targeting young urban women; aggressive social advertising"
            },
            {
                "name": "OZiva",
                "page_search_term": "OZiva",
                "category": "Women's Nutrition",
                "justification": "Plant-based nutrition and protein for women — direct supplement competitor"
            }
        ]
    },
    "manmatters": {
        "display_name": "Man Matters",
        "category": "Men's Health, Grooming & Wellness",
        "target_audience": "Men, 22-45, urban India",
        "own_page_id": None,
        "competitors": [
            {
                "name": "The Man Company",
                "page_search_term": "The Man Company grooming",
                "category": "Men's Grooming",
                "justification": "Premium men's grooming brand; heavy digital spender; same audience"
            },
            {
                "name": "Bombay Shaving Company",
                "page_search_term": "Bombay Shaving Company",
                "category": "Men's Grooming",
                "justification": "Men's grooming + skincare; expanded to women's line; strong Meta ads"
            },
            {
                "name": "Beardo",
                "page_search_term": "Beardo beard care",
                "category": "Men's Grooming",
                "justification": "Men's beard + grooming brand; acquired by Mamaearth; major Meta advertiser"
            },
            {
                "name": "USTRAA",
                "page_search_term": "USTRAA men grooming",
                "category": "Men's Grooming",
                "justification": "Men's personal care brand; competes in hair, beard, skin categories"
            },
            {
                "name": "Traya Health",
                "page_search_term": "Traya Health hair",
                "category": "Men's Hair Health",
                "justification": "Direct competitor in hair fall solutions for men; doctor-backed claims"
            },
            {
                "name": "Vedix",
                "page_search_term": "Vedix Ayurvedic",
                "category": "Men's Hair & Wellness",
                "justification": "Ayurvedic personalized hair solutions; competes with Man Matters hair products"
            },
            {
                "name": "BoldFit",
                "page_search_term": "BoldFit supplements",
                "category": "Men's Fitness & Nutrition",
                "justification": "Men's fitness supplements; competes in protein + nutrition category"
            },
            {
                "name": "Ustraa by Happily Unmarried",
                "page_search_term": "Happily Unmarried men",
                "category": "Men's Lifestyle",
                "justification": "Men's lifestyle brand; quirky positioning; competes for same digital eyeballs"
            }
        ]
    },
    "littlejoys": {
        "display_name": "Little Joys",
        "category": "Kids' Nutrition & Wellness",
        "target_audience": "Parents with kids aged 0-12, urban India",
        "own_page_id": None,
        "competitors": [
            {
                "name": "Mamaearth Baby",
                "page_search_term": "Mamaearth baby care",
                "category": "Baby & Kids Care",
                "justification": "Mamaearth's baby line — direct competitor; same parent audience; D2C model"
            },
            {
                "name": "Himalaya Baby",
                "page_search_term": "Himalaya Baby Wellness",
                "category": "Baby & Kids Care",
                "justification": "Trusted baby wellness brand; heavy advertising; competes in supplements"
            },
            {
                "name": "Bey Bee",
                "page_search_term": "Bey Bee baby products",
                "category": "Baby Products",
                "justification": "D2C baby care brand; growing Meta ad presence"
            },
            {
                "name": "Chicco India",
                "page_search_term": "Chicco baby products India",
                "category": "Baby Products",
                "justification": "International baby brand active in India; competes for parent audience"
            },
            {
                "name": "Horlicks",
                "page_search_term": "Horlicks kids nutrition",
                "category": "Kids Nutrition",
                "justification": "Dominant kids nutrition brand; Little Joys directly competes with modern positioning"
            },
            {
                "name": "Complan",
                "page_search_term": "Complan growth nutrition",
                "category": "Kids Nutrition",
                "justification": "Height & growth nutrition for kids; direct competitor in 4-12 age group"
            },
            {
                "name": "Pediasure",
                "page_search_term": "PediaSure India kids",
                "category": "Kids Nutrition",
                "justification": "Abbott's kids nutrition brand; competes in premium parent segment"
            },
            {
                "name": "The Moms Co",
                "page_search_term": "The Moms Co baby",
                "category": "Baby & Kids Care",
                "justification": "D2C mom + baby brand; heavy Meta ads; same parent audience"
            }
        ]
    }
}

def get_all_competitors():
    """Returns flat list of all competitors across all brands."""
    all_comps = []
    for brand_key, brand_data in BRANDS.items():
        for comp in brand_data["competitors"]:
            all_comps.append({
                "brand": brand_key,
                "brand_display": brand_data["display_name"],
                **comp
            })
    return all_comps

def get_competitors_for_brand(brand_key: str):
    return BRANDS.get(brand_key, {}).get("competitors", [])