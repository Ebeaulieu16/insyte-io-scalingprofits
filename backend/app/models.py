from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.database import Base

class VideoMetrics(Base):
    __tablename__ = "video_metrics"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    avg_watch_time = Column(Float, default=0.0)  # in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    clicks = relationship("ClickEvent", back_populates="video")

class ClickEvent(Base):
    __tablename__ = "click_events"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("video_metrics.id"))
    ip_address = Column(String)
    user_agent = Column(String)
    referrer = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    video = relationship("VideoMetrics", back_populates="clicks")
    booking = relationship("BookingEvent", back_populates="click", uselist=False)

class BookingEvent(Base):
    __tablename__ = "booking_events"

    id = Column(Integer, primary_key=True, index=True)
    click_id = Column(Integer, ForeignKey("click_events.id"))
    email = Column(String)
    name = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    click = relationship("ClickEvent", back_populates="booking")
    sale = relationship("SaleEvent", back_populates="booking", uselist=False)

class SaleEvent(Base):
    __tablename__ = "sale_events"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("booking_events.id"))
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship
    booking = relationship("BookingEvent", back_populates="sale")

class Link(Base):
    __tablename__ = "links"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    destination_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow) 