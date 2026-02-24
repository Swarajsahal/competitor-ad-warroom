"""
Sample data seeder for the Competitor Ad War Room.
This provides realistic mock data when the Meta API returns no results
(e.g., for Indian brands due to API geographic limitations).
"""

import random
from datetime import datetime, timedelta

# ---- Realistic ad copy templates per category ----
AD_TEMPLATES = {
    "bebodywise_competitors": [
        {
            "theme": "ugc_testimonial",
            "bodies": [
                "I tried {product} for 3 months and honestly? My skin transformed 🌟 No filters needed anymore! #RealResults",
                "From acne-prone to glass skin in 60 days 😍 {product} changed everything. Link in bio!",
                "My mom asked me what I changed in my routine — I said {product} and nothing else 💕",
            ],
            "titles": ["{brand}: Real Women, Real Results", "Science-Backed Skincare That Actually Works"]
        },
        {
            "theme": "doctor_authority",
            "bodies": [
                "Recommended by 10,000+ dermatologists across India. {product} — because your skin deserves science.",
                "Dermatologist formulated. Clinically tested. {brand} — skincare you can trust.",
                "Dr. Priya Sharma: 'This is the only serum I recommend to all my patients for hyperpigmentation.'",
            ],
            "titles": ["Clinically Proven Results", "Trusted by India's Top Dermatologists"]
        },
        {
            "theme": "offer_promo",
            "bodies": [
                "🔥 FLAT 30% OFF on your first order! Use code GLOW30. Limited time only.",
                "Buy 2, Get 1 FREE on all {brand} bestsellers. Shop now before it's gone!",
                "₹499 starter kit — includes our top 3 sellers. Free shipping. 30-day return guarantee.",
            ],
            "titles": ["Limited Time Offer", "Today Only: 30% Off Sitewide"]
        },
        {
            "theme": "ingredient_science",
            "bodies": [
                "Niacinamide 10% + Zinc 1% — the gold standard combo for oily, acne-prone skin. Now in India.",
                "2% Salicylic Acid. No SLS. No Parabens. Just science that works. That's {brand}.",
                "Our Vitamin C serum has 15% L-Ascorbic Acid — 3x more potent than the leading brand.",
            ],
            "titles": ["The Science of Beautiful Skin", "Ingredient Transparency Starts Here"]
        },
        {
            "theme": "community_story",
            "bodies": [
                "1 million+ women in India have made the switch. Join the {brand} revolution 💪",
                "Our community of glowing women is growing every day. What's their secret? {product} 🌸",
                "From Bengaluru to Bhopal — women everywhere are choosing {brand}. Here's why.",
            ],
            "titles": ["Join 1M+ Women", "India's Most-Loved Skincare Brand"]
        }
    ],
    "manmatters_competitors": [
        {
            "theme": "ugc_testimonial",
            "bodies": [
                "I was losing 200+ strands a day. After 6 months on {product}, my barber noticed the difference 💪 #HairGrowth",
                "Honest review: {brand} actually worked for my hair fall. I was skeptical but the results speak for themselves.",
                "My confidence is back. {product} changed my hair and honestly my entire morning routine.",
            ],
            "titles": ["{brand}: Real Men, Real Results", "Hair Loss Fixed? Here's How."]
        },
        {
            "theme": "doctor_authority",
            "bodies": [
                "Board-certified dermatologists + a custom formula = {product}. Because hair fall deserves real treatment.",
                "Dr. Rahul Verma explains why {brand}'s 3-step system outperforms everything else on the market.",
                "Science says: DHT is the #1 cause of male pattern baldness. {brand} blocks it at the root.",
            ],
            "titles": ["Doctor-Backed Hair Solutions", "Science of Hair Regrowth"]
        },
        {
            "theme": "offer_promo",
            "bodies": [
                "🔥 Hair Kit + Free Consultation — just ₹999. 10,000 men already took this step.",
                "Festive Sale: 40% off our complete grooming range. Use GROOM40.",
                "First order? Get ₹500 off + FREE doctor consultation. Limited slots.",
            ],
            "titles": ["Flat 40% Off — Today Only", "Start Your Hair Regrowth Journey"]
        },
        {
            "theme": "before_after",
            "bodies": [
                "Arjun's before/after at 90 days 📸 This is what consistency with {product} looks like.",
                "3 months. 90 photos. 1 incredible result. {brand} hair regrowth kit — results that show.",
                "Watch the transformation 👇 From thinning to thick — this is {product} working.",
            ],
            "titles": ["90 Days. Real Results.", "Before vs After: Judge for Yourself"]
        },
        {
            "theme": "community_story",
            "bodies": [
                "500,000 men trust {brand} for their daily grooming. You should too.",
                "India's leading men's wellness platform — built by men, for men. That's {brand}.",
                "When 1 in 3 Indian men has hair loss, someone had to build a real solution. That's us.",
            ],
            "titles": ["5L+ Men Trust Us", "India's #1 Men's Wellness Brand"]
        }
    ],
    "littlejoys_competitors": [
        {
            "theme": "parent_reassurance",
            "bodies": [
                "As a mom, I only give my kids the safest. {product} — zero sugar, all nutrients, zero compromise.",
                "Priya's son went from picky eater to finishing his plate 😊 The secret? {product} daily.",
                "3 kids, 1 solution. {brand} kids' nutrition — because every child deserves the best start.",
            ],
            "titles": ["{brand}: Trusted by 1M+ Indian Moms", "Nutrition Without Compromise"]
        },
        {
            "theme": "pediatrician_authority",
            "bodies": [
                "Recommended by pediatricians across India. {product} — clinically proven for growing kids.",
                "Dr. Anjali Mehta, Pediatrician: '{brand} is what I give my own children every morning.'",
                "Formulated with ICMR guidelines for Indian children's nutritional needs. {brand}.",
            ],
            "titles": ["Pediatrician Recommended", "Built on Child Nutrition Science"]
        },
        {
            "theme": "offer_promo",
            "bodies": [
                "Back to school special: 25% off on {brand} nutrition packs. Free shipping above ₹500!",
                "Subscribe & Save: Get {product} every month + save ₹200 + free nutritionist consult.",
                "Summer pack: 3 months of {product} at 30% off. Keep your kids healthy all season.",
            ],
            "titles": ["Back to School Sale!", "Subscribe & Save 25%"]
        },
        {
            "theme": "ingredient_science",
            "bodies": [
                "DHA for brain. Calcium for bones. Iron for energy. All in one {product} serving for your child.",
                "No artificial colors. No preservatives. No palm oil. Just clean nutrition your kids will actually eat.",
                "Indian kids need 40% more iron than WHO guidelines. {brand} is built for Indian children.",
            ],
            "titles": ["Science-Backed Kids Nutrition", "Clean Label. Real Nutrition."]
        },
        {
            "theme": "ugc_testimonial",
            "bodies": [
                "My 7-year-old asks for {product} every morning now 🙌 That's how I know it works. Thank you {brand}!",
                "From skinny to strong in 4 months — {product} + regular meals changed everything for my son.",
                "Rahul's pediatrician was shocked at his growth. We've been on {brand} for 6 months.",
            ],
            "titles": ["Real Kids. Real Growth.", "Parents Are Raving About This"]
        }
    ]
}

MEDIA_TYPES = ["IMAGE", "VIDEO", "CAROUSEL"]
MEDIA_WEIGHTS = [0.40, 0.35, 0.25]  # realistic distribution

PLATFORMS = ["facebook", "instagram", "messenger", "audience_network"]

SPEND_RANGES = [
    {"lower_bound": "100", "upper_bound": "499"},
    {"lower_bound": "500", "upper_bound": "999"},
    {"lower_bound": "1000", "upper_bound": "4999"},
    {"lower_bound": "5000", "upper_bound": "9999"},
    {"lower_bound": "10000", "upper_bound": "49999"},
    {"lower_bound": "50000", "upper_bound": "99999"},
]

IMPRESSION_RANGES = [
    {"lower_bound": "1000", "upper_bound": "4999"},
    {"lower_bound": "5000", "upper_bound": "9999"},
    {"lower_bound": "10000", "upper_bound": "49999"},
    {"lower_bound": "50000", "upper_bound": "99999"},
    {"lower_bound": "100000", "upper_bound": "499999"},
    {"lower_bound": "500000", "upper_bound": "999999"},
]


def generate_sample_ads(
    competitor_name: str,
    brand_key: str,
    count: int = 15,
    days_range: int = 90
) -> list:
    """Generate realistic mock ads for a competitor."""
    
    # Select correct template pool
    if brand_key == "bebodywise":
        templates = AD_TEMPLATES["bebodywise_competitors"]
    elif brand_key == "manmatters":
        templates = AD_TEMPLATES["manmatters_competitors"]
    else:
        templates = AD_TEMPLATES["littlejoys_competitors"]

    product_names = {
        # Bebodywise competitors
        "Pilgrim": ["Vitamin C Serum", "SPF 50 Sunscreen", "AHA BHA Peel"],
        "Mamaearth": ["Onion Hair Oil", "Ubtan Face Pack", "Vitamin C Face Wash"],
        "Dot & Key": ["Waterlight Gel Moisturizer", "Vitamin C + E Serum", "Retinol Night Cream"],
        "Plum Goodness": ["Green Tea Mattifying Moisturizer", "E-Luminence Face Wash", "Grape Seed & Sea Buckthorn Oil"],
        "Minimalist": ["10% Niacinamide + Zinc", "2% Salicylic Acid", "Alpha Arbutin 2%"],
        "WOW Skin Science": ["Apple Cider Vinegar Shampoo", "Vitamin C Face Serum", "Onion Black Seed Hair Oil"],
        "mCaffeine": ["Coffee Body Scrub", "Caffeine Under Eye Cream", "Coffee Face Wash"],
        "OZiva": ["Protein & Herbs Women", "Plant-Based Biotin", "Holistic Nutrition Shake"],
        # Man Matters competitors
        "The Man Company": ["Beard Growth Kit", "Anti-Acne Face Wash", "Daily Sunscreen SPF 50"],
        "Bombay Shaving Company": ["Charcoal Face Wash", "After Shave Balm", "Hair Serum for Men"],
        "Beardo": ["Beard Growth Serum", "Activated Charcoal Peel Mask", "Anti Hair Fall Shampoo"],
        "USTRAA": ["Hair Growth Vitalizer", "Activated Charcoal Face Scrub", "Sport Deodorant"],
        "Traya Health": ["Hair Ras", "Hair Vitamins", "Scalp Oil Treatment Kit"],
        "Vedix": ["Customized Hair Oil", "Herbal Shampoo Kit", "Vedix Hair Regrowth Kit"],
        "BoldFit": ["Whey Protein Gold", "Pre-Workout", "Multivitamin for Men"],
        # Little Joys competitors
        "Mamaearth Baby": ["Gentle Cleansing Baby Shampoo", "Soothing Baby Lotion", "Baby Massage Oil"],
        "Himalaya Baby": ["Himalaya Baby Cream", "Gentle Baby Shampoo", "Baby Body Lotion"],
        "Bey Bee": ["Organic Baby Powder", "Natural Baby Wipes", "Baby Rash Cream"],
        "Chicco India": ["Natural Feeling Bottle", "Baby Snack Melties", "Baby Oatmeal Cereal"],
        "Horlicks": ["Horlicks Junior", "Mother's Horlicks", "Horlicks Protein+"],
        "Complan": ["Complan NutriGro", "Complan Chocolate", "Complan Power of 2"],
        "Pediasure": ["PediaSure Vanilla", "PediaSure Chocolate", "PediaSure 5+ Immunity"],
        "The Moms Co": ["Natural Baby Lotion", "Stretch Marks Oil", "Baby Body Butter"],
    }.get(competitor_name, ["Premium Product", "Best Seller", "New Launch"])

    ads = []
    now = datetime.now()

    for i in range(count):
        template = random.choice(templates)
        product = random.choice(product_names)
        
        body_template = random.choice(template["bodies"])
        title_template = random.choice(template["titles"])
        
        body = body_template.replace("{brand}", competitor_name).replace("{product}", product)
        title = title_template.replace("{brand}", competitor_name).replace("{product}", product)

        media_type = random.choices(MEDIA_TYPES, weights=MEDIA_WEIGHTS)[0]
        
        days_ago_start = random.randint(1, days_range)
        start_date = now - timedelta(days=days_ago_start)
        
        # Some ads are still running (30% chance stopped)
        is_active = random.random() > 0.3
        stop_date = None if is_active else start_date + timedelta(days=random.randint(7, 45))

        # Longer-running ads = more likely top performers
        run_days = (now - start_date).days if is_active else (stop_date - start_date).days
        is_top_performer = run_days > 30

        num_platforms = random.randint(1, 3)
        platforms = random.sample(PLATFORMS, num_platforms)

        ad = {
            "id": f"sample_{competitor_name.lower().replace(' ', '_')}_{i}_{int(now.timestamp())}",
            "page_name": competitor_name,
            "page_id": f"page_{competitor_name.lower().replace(' ', '_')}",
            "ad_creation_time": start_date.strftime("%Y-%m-%dT%H:%M:%S+0000"),
            "ad_delivery_start_time": start_date.strftime("%Y-%m-%dT%H:%M:%S+0000"),
            "ad_delivery_stop_time": stop_date.strftime("%Y-%m-%dT%H:%M:%S+0000") if stop_date else None,
            "ad_creative_bodies": [body],
            "ad_creative_link_titles": [title],
            "ad_creative_link_descriptions": [f"Shop {product} by {competitor_name} — Free shipping on orders above ₹499"],
            "media_type": media_type,
            "publisher_platforms": platforms,
            "spend": random.choice(SPEND_RANGES),
            "impressions": random.choice(IMPRESSION_RANGES),
            "languages": ["en"],
            "ad_snapshot_url": f"https://www.facebook.com/ads/archive/render_ad/?id=sample_{i}",
            # Enriched fields
            "_is_sample": True,
            "_theme": template["theme"],
            "_is_active": is_active,
            "_run_days": run_days,
            "_is_top_performer": is_top_performer,
            "_brand_key": brand_key,
            "_competitor": competitor_name,
            "_product": product,
        }
        ads.append(ad)

    return ads


def seed_all_sample_data(competitors_config: dict) -> list:
    """Seed sample data for all competitors across all brands."""
    all_ads = []
    for brand_key, brand_data in competitors_config.items():
        for comp in brand_data["competitors"]:
            count = random.randint(10, 20)
            ads = generate_sample_ads(comp["name"], brand_key, count=count)
            all_ads.extend(ads)
    return all_ads