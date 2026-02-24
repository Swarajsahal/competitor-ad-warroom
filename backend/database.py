"""
Database layer — SQLite via SQLAlchemy.
Stores ads, analysis runs, and weekly briefs.
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Boolean,
    Text, DateTime, Index, text
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session

logger = logging.getLogger(__name__)

DB_PATH = os.environ.get("DB_PATH", "warroom.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class AdRecord(Base):
    __tablename__ = "ads"

    id = Column(String, primary_key=True)
    page_name = Column(String, index=True)
    page_id = Column(String)
    brand_key = Column(String, index=True)   # bebodywise / manmatters / littlejoys
    competitor_name = Column(String, index=True)

    ad_body = Column(Text)
    ad_title = Column(Text)
    ad_description = Column(Text)

    media_type = Column(String, index=True)   # IMAGE / VIDEO / CAROUSEL
    publisher_platforms = Column(Text)         # JSON list
    languages = Column(Text)                   # JSON list

    ad_creation_time = Column(DateTime)
    ad_delivery_start_time = Column(DateTime)
    ad_delivery_stop_time = Column(DateTime, nullable=True)

    spend_lower = Column(Integer, nullable=True)
    spend_upper = Column(Integer, nullable=True)
    impressions_lower = Column(Integer, nullable=True)
    impressions_upper = Column(Integer, nullable=True)

    ad_snapshot_url = Column(String, nullable=True)

    # Enriched fields
    theme = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    run_days = Column(Integer, default=0)
    is_top_performer = Column(Boolean, default=False)
    is_sample = Column(Boolean, default=False)

    # AI analysis
    ai_theme = Column(String, nullable=True)
    ai_sentiment = Column(String, nullable=True)
    ai_cta_type = Column(String, nullable=True)
    ai_angle = Column(String, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_brand_competitor", "brand_key", "competitor_name"),
        Index("ix_brand_media", "brand_key", "media_type"),
    )


class WeeklyBrief(Base):
    __tablename__ = "weekly_briefs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_key = Column(String, index=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
    week_start = Column(DateTime)
    week_end = Column(DateTime)
    brief_text = Column(Text)
    insights_json = Column(Text)   # JSON list of insight objects
    ad_count = Column(Integer)


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_type = Column(String)   # "fetch", "analyze", "brief"
    brand_key = Column(String, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, default="running")   # running / success / failed
    message = Column(Text, nullable=True)
    ads_processed = Column(Integer, default=0)


def init_db():
    Base.metadata.create_all(engine)
    logger.info("Database initialized")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---- CRUD helpers ----

def upsert_ad(db: Session, ad_data: dict) -> AdRecord:
    """Insert or update an ad record."""
    existing = db.query(AdRecord).filter_by(id=ad_data["id"]).first()
    if existing:
        for k, v in ad_data.items():
            if hasattr(existing, k):
                setattr(existing, k, v)
        db.commit()
        return existing

    record = AdRecord(**{k: v for k, v in ad_data.items() if hasattr(AdRecord, k)})
    db.add(record)
    db.commit()
    return record


def get_ads(
    db: Session,
    brand_key: Optional[str] = None,
    competitor_name: Optional[str] = None,
    media_type: Optional[str] = None,
    theme: Optional[str] = None,
    is_active: Optional[bool] = None,
    days_back: Optional[int] = None,
    limit: int = 200
) -> List[AdRecord]:
    q = db.query(AdRecord)
    if brand_key:
        q = q.filter(AdRecord.brand_key == brand_key)
    if competitor_name:
        q = q.filter(AdRecord.competitor_name == competitor_name)
    if media_type:
        q = q.filter(AdRecord.media_type == media_type)
    if theme:
        q = q.filter(AdRecord.theme == theme)
    if is_active is not None:
        q = q.filter(AdRecord.is_active == is_active)
    if days_back:
        cutoff = datetime.utcnow().timestamp() - (days_back * 86400)
        q = q.filter(AdRecord.ad_delivery_start_time >= datetime.utcfromtimestamp(cutoff))
    return q.order_by(AdRecord.ad_delivery_start_time.desc()).limit(limit).all()


def get_stats(db: Session, brand_key: Optional[str] = None) -> dict:
    """Return aggregate stats for dashboard."""
    q = db.query(AdRecord)
    if brand_key:
        q = q.filter(AdRecord.brand_key == brand_key)

    total = q.count()
    active = q.filter(AdRecord.is_active == True).count()
    top_performers = q.filter(AdRecord.is_top_performer == True).count()

    # Media type breakdown
    media_counts = {}
    for mt in ["IMAGE", "VIDEO", "CAROUSEL"]:
        cnt = q.filter(AdRecord.media_type == mt).count()
        media_counts[mt] = cnt

    # Theme breakdown
    theme_counts = {}
    from sqlalchemy import func
    for row in db.query(AdRecord.theme, func.count(AdRecord.id)).filter(
        AdRecord.brand_key == brand_key if brand_key else True
    ).group_by(AdRecord.theme).all():
        if row[0]:
            theme_counts[row[0]] = row[1]

    # Competitor breakdown
    comp_counts = {}
    for row in db.query(AdRecord.competitor_name, func.count(AdRecord.id)).filter(
        AdRecord.brand_key == brand_key if brand_key else True
    ).group_by(AdRecord.competitor_name).all():
        if row[0]:
            comp_counts[row[0]] = row[1]

    return {
        "total_ads": total,
        "active_ads": active,
        "top_performers": top_performers,
        "media_breakdown": media_counts,
        "theme_breakdown": theme_counts,
        "competitor_breakdown": comp_counts,
    }


def save_weekly_brief(db: Session, brief_data: dict) -> WeeklyBrief:
    brief = WeeklyBrief(**brief_data)
    db.add(brief)
    db.commit()
    return brief


def get_latest_brief(db: Session, brand_key: str) -> Optional[WeeklyBrief]:
    return db.query(WeeklyBrief).filter_by(brand_key=brand_key)\
        .order_by(WeeklyBrief.generated_at.desc()).first()


def save_run(db: Session, run_data: dict) -> AnalysisRun:
    run = AnalysisRun(**run_data)
    db.add(run)
    db.commit()
    return run