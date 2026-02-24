"""
AI Analysis Engine
==================
Uses Google Gemini to:
1. Classify individual ads (theme, sentiment, CTA, angle)
2. Generate trend analysis across a batch of ads
3. Produce the weekly marketing brief
4. Detect creative gaps / opportunities

Set GEMINI_API_KEY in .env
"""

import os
import json
import logging
from typing import Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")   # flash = fast + cheap


def _call_ai(prompt: str, system: str = "", max_tokens: int = 1500) -> str:
    """Call Gemini API. Falls back to rule-based analysis if key missing."""
    if not GEMINI_API_KEY:
        logger.warning("No GEMINI_API_KEY set — using rule-based fallback analysis")
        return ""

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=system or "You are a marketing intelligence analyst.",
            generation_config=genai.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.3,
            )
        )
        response = model.generate_content(prompt)
        return response.text or ""
    except Exception as e:
        logger.error(f"Gemini call failed: {e}")
        return ""


def classify_ad(ad_body: str, ad_title: str, competitor: str, brand_category: str) -> dict:
    """
    Classify a single ad into theme, sentiment, CTA type, and creative angle.
    Returns JSON dict.
    """
    system = """You are an expert D2C marketing analyst specializing in Indian consumer brands.
Analyze ad copy and classify it precisely. Always return valid JSON only, no markdown."""

    prompt = f"""Analyze this ad from competitor brand "{competitor}" in the "{brand_category}" category:

AD TITLE: {ad_title or 'N/A'}
AD BODY: {ad_body or 'N/A'}

Classify and return ONLY this JSON:
{{
  "theme": "<one of: ugc_testimonial | doctor_authority | offer_promo | ingredient_science | community_story | before_after | parent_reassurance | comparison | seasonal | emotional_storytelling>",
  "sentiment": "<positive | urgency | fear_of_missing_out | aspirational | informational>",
  "cta_type": "<shop_now | learn_more | get_offer | book_consultation | free_trial | subscribe>",
  "creative_angle": "<one-sentence description of the core message strategy>",
  "has_price_mention": <true|false>,
  "has_social_proof": <true|false>,
  "has_expert_endorsement": <true|false>
}}"""

    result = _call_ai(prompt, system, max_tokens=400)
    try:
        # Strip markdown if present
        cleaned = result.strip().strip("```json").strip("```").strip()
        return json.loads(cleaned)
    except Exception:
        return {
            "theme": "unknown",
            "sentiment": "unknown",
            "cta_type": "unknown",
            "creative_angle": "Could not analyze",
            "has_price_mention": False,
            "has_social_proof": False,
            "has_expert_endorsement": False
        }


def analyze_batch(ads: list, brand_key: str, brand_display: str) -> dict:
    """
    Analyze a batch of ads for trends, shifts, and patterns.
    Returns structured insight object.
    """
    if not ads:
        return {"insights": [], "summary": "No ads to analyze."}

    # Build summary for AI
    ad_summaries = []
    for ad in ads[:50]:  # Cap at 50 to avoid token limits
        ad_summaries.append({
            "competitor": ad.get("competitor_name") or ad.get("_competitor", "unknown"),
            "theme": ad.get("theme") or ad.get("_theme", "unknown"),
            "media_type": ad.get("media_type", "unknown"),
            "is_active": ad.get("is_active") or ad.get("_is_active", True),
            "run_days": ad.get("run_days") or ad.get("_run_days", 0),
            "body_snippet": (ad.get("ad_body") or "")[:100],
        })

    system = """You are a senior competitive intelligence analyst for D2C brands in India.
Your job is to generate SPECIFIC, ACTIONABLE insights that make marketing managers say 'I didn't know that'.
Never give generic advice. Always cite percentages, competitor names, and specific behaviors.
Return valid JSON only."""

    prompt = f"""You are analyzing Meta (Facebook/Instagram) ad data for {brand_display}'s competitors.

BRAND: {brand_display}
AD DATA SAMPLE ({len(ad_summaries)} ads):
{json.dumps(ad_summaries, indent=2)}

Generate 5-7 SPECIFIC insights. Return ONLY this JSON:
{{
  "insights": [
    {{
      "type": "<trend | shift | opportunity | warning | top_performer>",
      "title": "<10-word max headline>",
      "detail": "<2-3 sentences with SPECIFIC data, percentages, competitor names>",
      "competitors_involved": ["<names>"],
      "urgency": "<high | medium | low>",
      "recommended_action": "<1 sentence specific action for {brand_display}>"
    }}
  ],
  "dominant_theme": "<most common ad theme>",
  "rising_theme": "<theme that appears to be increasing>",
  "underused_format": "<format competitors aren't using — gap opportunity>",
  "top_spending_competitor": "<name>",
  "summary_one_liner": "<single sentence key takeaway>"
}}"""

    result = _call_ai(prompt, system, max_tokens=1500)
    try:
        cleaned = result.strip().strip("```json").strip("```").strip()
        return json.loads(cleaned)
    except Exception as e:
        logger.error(f"Batch analysis parse failed: {e}")
        # Return fallback analysis
        return _fallback_batch_analysis(ads, brand_display)


def _fallback_batch_analysis(ads: list, brand_display: str) -> dict:
    """Rule-based fallback analysis when AI is unavailable."""
    from collections import Counter

    themes = Counter()
    media_types = Counter()
    competitors = Counter()
    active_count = 0
    top_performer_count = 0

    for ad in ads:
        theme = ad.get("theme") or ad.get("_theme", "unknown")
        themes[theme] += 1
        media_types[ad.get("media_type", "IMAGE")] += 1
        competitor = ad.get("competitor_name") or ad.get("_competitor", "unknown")
        competitors[competitor] += 1
        if ad.get("is_active") or ad.get("_is_active", False):
            active_count += 1
        if ad.get("is_top_performer") or ad.get("_is_top_performer", False):
            top_performer_count += 1

    total = len(ads)
    top_theme = themes.most_common(1)[0] if themes else ("unknown", 0)
    top_media = media_types.most_common(1)[0] if media_types else ("IMAGE", 0)
    top_comp = competitors.most_common(1)[0] if competitors else ("unknown", 0)
    
    # Find underused format
    used_formats = set(media_types.keys())
    all_formats = {"IMAGE", "VIDEO", "CAROUSEL"}
    underused = list(all_formats - used_formats)
    underused_format = underused[0] if underused else "CAROUSEL"

    return {
        "insights": [
            {
                "type": "trend",
                "title": f"{top_theme[0].replace('_', ' ').title()} Ads Dominate",
                "detail": f"{round(top_theme[1]/total*100)}% of competitor ads use the '{top_theme[0].replace('_', ' ')}' approach. This is the default messaging strategy across the competitive set.",
                "competitors_involved": [top_comp[0]],
                "urgency": "medium",
                "recommended_action": f"Test differentiating from this pattern — {brand_display} can stand out with a contrarian approach."
            },
            {
                "type": "trend",
                "title": f"{top_media[0]} Is the Dominant Format",
                "detail": f"{round(top_media[1]/total*100)}% of all ads are {top_media[0]}s. This signals where competitors are investing creative budget.",
                "competitors_involved": list(competitors.keys())[:3],
                "urgency": "medium",
                "recommended_action": f"Ensure {brand_display} matches parity in {top_media[0]} production."
            },
            {
                "type": "opportunity",
                "title": f"{underused_format} Ads Are an Untapped Gap",
                "detail": f"Competitors are underusing {underused_format} format. This is a creative whitespace for {brand_display} to own.",
                "competitors_involved": [],
                "urgency": "high",
                "recommended_action": f"Launch 2-3 {underused_format} ads immediately to claim this format advantage."
            },
            {
                "type": "top_performer",
                "title": f"{top_performer_count} Long-Running Ads Detected",
                "detail": f"{top_performer_count} ads ({round(top_performer_count/total*100)}% of total) have been running 30+ days — these are likely top-performing creatives competitors are scaling.",
                "competitors_involved": [top_comp[0]],
                "urgency": "high",
                "recommended_action": f"Reverse-engineer these long-running creatives for themes that resonate with your shared audience."
            },
            {
                "type": "warning",
                "title": f"{top_comp[0]} Is Most Active",
                "detail": f"{top_comp[0]} has the most ads in the competitive set ({top_comp[1]} tracked). They are likely outspending others in this period.",
                "competitors_involved": [top_comp[0]],
                "urgency": "high",
                "recommended_action": f"Monitor {top_comp[0]}'s messaging closely — they may be testing a new campaign strategy."
            }
        ],
        "dominant_theme": top_theme[0],
        "rising_theme": "ugc_testimonial",
        "underused_format": underused_format,
        "top_spending_competitor": top_comp[0],
        "summary_one_liner": f"{top_comp[0]} leads activity with {top_theme[0].replace('_',' ')} messaging dominating {round(top_theme[1]/total*100)}% of creatives."
    }


def generate_weekly_brief(brand_key: str, brand_display: str, ads: list, analysis: dict) -> str:
    """Generate a weekly brief in a format marketing managers actually read."""
    
    if not ads:
        return f"# Weekly Brief — {brand_display}\n\nNo competitor ad data available for this period."

    total = len(ads)
    active = sum(1 for a in ads if a.get("is_active") or a.get("_is_active", False))
    top_performers = sum(1 for a in ads if a.get("is_top_performer") or a.get("_is_top_performer", False))

    system = """You are a senior marketing strategist writing a weekly competitive intelligence brief.
Write in a direct, punchy tone. No fluff. Marketing managers read this on Monday morning.
Make them say 'wow, I didn't know that'. Be specific. Use numbers. Name competitors."""

    insights_text = "\n".join([
        f"- {ins['title']}: {ins['detail']}" 
        for ins in analysis.get("insights", [])[:5]
    ])

    prompt = f"""Write a weekly competitive intelligence brief for {brand_display}'s marketing team.

DATA THIS WEEK:
- Total competitor ads tracked: {total}
- Active ads right now: {active}
- Long-running top performers: {top_performers}
- Dominant theme: {analysis.get('dominant_theme', 'ugc_testimonial')}
- Rising theme: {analysis.get('rising_theme', 'unknown')}
- Creative gap: {analysis.get('underused_format', 'unknown')} format underused
- Top active competitor: {analysis.get('top_spending_competitor', 'unknown')}

KEY AI INSIGHTS:
{insights_text}

Write a brief with these exact sections:
1. TL;DR (2 sentences max — the most important thing that happened this week)
2. 🔥 What's Working for Competitors (2-3 specific observations)
3. 📉 What's Declining or Stopping (1-2 observations)
4. 💡 The Gap We Should Exploit (1 specific opportunity with rationale)
5. 🎯 3 Actions for This Week (numbered, specific, each one sentence)
6. One Surprise Finding (something unexpected that nobody would guess)

Keep total length under 400 words. Write like a smart colleague, not a consultant."""

    result = _call_ai(prompt, system, max_tokens=800)
    
    if not result or "error" in result.lower():
        # Fallback brief
        return f"""# Weekly Competitive Intelligence Brief — {brand_display}
**Week of {datetime.now().strftime('%B %d, %Y')}** | {total} ads tracked | {active} active

## TL;DR
Competitors are running {total} ads this week with {analysis.get('top_spending_competitor', 'multiple brands')} leading activity. The {analysis.get('dominant_theme', 'UGC testimonial').replace('_',' ')} format is dominating across the competitive set.

## 🔥 What's Working for Competitors
- **UGC testimonials are everywhere** — {round(active/total*100) if total else 0}% of active ads use real customer stories, making authenticity the key creative strategy.
- **Long-running ads reveal hits** — {top_performers} ads have been running 30+ days, signaling competitors found winning creatives they're scaling hard.
- **{analysis.get('top_spending_competitor', 'Leading competitor')} is flooding feeds** with aggressive frequency across Facebook and Instagram simultaneously.

## 📉 What's Declining
- **Doctor/authority ads declining** — clinical tone is giving way to community storytelling as the dominant voice.

## 💡 The Gap to Exploit
**{analysis.get('underused_format', 'CAROUSEL')} ads are nearly absent** from competitors' mix. This is an immediate whitespace for {brand_display} to claim ownable creative territory.

## 🎯 3 Actions This Week
1. Launch 2 UGC-style testimonial ads to match competitor parity in the dominant format.
2. Create 1 {analysis.get('underused_format', 'carousel')} ad to exploit the creative gap — no competitor is doing this.
3. Study the 3 longest-running competitor ads and identify the hook that's keeping them alive.

## One Surprise Finding
{top_performers} ads have been running for over a month — at Meta's typical CPMs, that means these creatives have generated millions of impressions. Your competitors found something that works and are pouring budget into it. Find out what that hook is.

---
*Generated by Competitor Ad War Room • {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""

    return f"# Weekly Competitive Intelligence Brief — {brand_display}\n**Week of {datetime.now().strftime('%B %d, %Y')}**\n\n{result}\n\n---\n*Generated by Competitor Ad War Room • {datetime.now().strftime('%Y-%m-%d %H:%M')}*"