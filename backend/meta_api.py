"""
Meta Ad Library API Client
===========================
Uses the official Facebook Graph API /ads_archive endpoint.

IMPORTANT: The official API only returns data for:
  - EU/EEA countries
  - Brazil (limited)
  - Political/social issue ads (global)
  
For Indian D2C brands, the API may return limited results.
We handle this by:
1. Trying the official API first
2. Falling back to sample data if no results
3. Always seeding with realistic mock data for demo purposes

API Docs: https://developers.facebook.com/docs/marketing-api/reference/ads_archive
"""

import os
import time
import logging
import requests
from datetime import datetime, timedelta
from typing import Optional
import json

logger = logging.getLogger(__name__)

GRAPH_API_BASE = "https://graph.facebook.com/v18.0"

class MetaAdLibraryClient:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.params = {"access_token": self.access_token}
        self.rate_limit_sleep = 1.0  # seconds between requests

    def search_ads(
        self,
        search_terms: str = "",
        page_ids: Optional[list] = None,
        country: str = "IN",
        ad_active_status: str = "ALL",
        media_type: str = "ALL",
        ad_delivery_date_min: Optional[str] = None,
        ad_delivery_date_max: Optional[str] = None,
        limit: int = 25,
        after_cursor: Optional[str] = None
    ) -> dict:
        """
        Search Meta Ad Library via Graph API.
        Returns dict with 'data' list and 'paging' info.
        """
        params = {
            "search_type": "KEYWORD_EXACT_PHRASE" if search_terms else "PAGE",
            "ad_reached_countries": f'["{country}"]',
            "ad_active_status": ad_active_status,
            "media_type": media_type,
            "limit": limit,
            "fields": ",".join([
                "id",
                "ad_creation_time",
                "ad_delivery_start_time",
                "ad_delivery_stop_time",
                "ad_creative_bodies",
                "ad_creative_link_captions",
                "ad_creative_link_descriptions",
                "ad_creative_link_titles",
                "page_id",
                "page_name",
                "spend",
                "impressions",
                "demographic_distribution",
                "region_distribution",
                "ad_snapshot_url",
                "languages",
                "publisher_platforms"
            ])
        }

        if search_terms:
            params["search_terms"] = search_terms

        if page_ids:
            params["search_page_ids"] = json.dumps(page_ids)

        if ad_delivery_date_min:
            params["ad_delivery_date_min"] = ad_delivery_date_min
        if ad_delivery_date_max:
            params["ad_delivery_date_max"] = ad_delivery_date_max

        if after_cursor:
            params["after"] = after_cursor

        try:
            time.sleep(self.rate_limit_sleep)
            resp = self.session.get(
                f"{GRAPH_API_BASE}/ads_archive",
                params=params,
                timeout=30
            )
            resp.raise_for_status()
            result = resp.json()

            if "error" in result:
                logger.error(f"Meta API error: {result['error']}")
                return {"data": [], "paging": {}, "error": result["error"]}

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {"data": [], "paging": {}, "error": str(e)}

    def get_page_id(self, page_name: str) -> Optional[str]:
        """Search for a Facebook page ID by name."""
        try:
            time.sleep(self.rate_limit_sleep)
            resp = self.session.get(
                f"{GRAPH_API_BASE}/pages/search",
                params={"q": page_name, "fields": "id,name,verification_status"},
                timeout=20
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("data"):
                return data["data"][0]["id"]
        except Exception as e:
            logger.error(f"Page search failed for '{page_name}': {e}")
        return None

    def fetch_all_ads_for_competitor(
        self,
        search_term: str,
        country: str = "IN",
        days_back: int = 90,
        max_pages: int = 3
    ) -> list:
        """
        Fetch all ads for a competitor (handles pagination).
        Limits to max_pages to avoid rate limits.
        """
        ads = []
        date_min = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

        result = self.search_ads(
            search_terms=search_term,
            country=country,
            ad_delivery_date_min=date_min,
            limit=25
        )

        ads.extend(result.get("data", []))
        page_count = 1

        while page_count < max_pages:
            paging = result.get("paging", {})
            cursors = paging.get("cursors", {})
            after = cursors.get("after")
            if not after or not paging.get("next"):
                break

            result = self.search_ads(
                search_terms=search_term,
                country=country,
                ad_delivery_date_min=date_min,
                after_cursor=after
            )
            ads.extend(result.get("data", []))
            page_count += 1

        logger.info(f"Fetched {len(ads)} ads for '{search_term}'")
        return ads

    def validate_token(self) -> bool:
        """Check if the access token is valid."""
        try:
            resp = self.session.get(
                f"{GRAPH_API_BASE}/me",
                params={"fields": "id,name"},
                timeout=10
            )
            data = resp.json()
            return "id" in data
        except Exception:
            return False