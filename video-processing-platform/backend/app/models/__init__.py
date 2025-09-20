from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    original_filename = Column(String)
    file_path = Column(String)
    duration = Column(Float)
    size = Column(Integer)
    format = Column(String)
    resolution = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)
    
    jobs = relationship("ProcessingJob", back_populates="video")
    quality_versions = relationship("QualityVersion", back_populates="original_video")

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    job_type = Column(String)  
    status = Column(String, default="pending")  
    progress = Column(Integer, default=0)
    result_path = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    video = relationship("Video", back_populates="jobs")

class QualityVersion(Base):
    __tablename__ = "quality_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    original_video_id = Column(Integer, ForeignKey("videos.id"))
    quality = Column(String)  
    file_path = Column(String)
    size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    original_video = relationship("Video", back_populates="quality_versions")

class Overlay(Base):
    __tablename__ = "overlays"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    overlay_type = Column(String)  
    content = Column(Text)  
    position_x = Column(Integer)
    position_y = Column(Integer)
    start_time = Column(Float)
    end_time = Column(Float)
    style_config = Column(JSON)  
    created_at = Column(DateTime, default=datetime.utcnow)