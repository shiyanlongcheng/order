# coding: utf-8
from sqlalchemy import Column, DateTime, Index, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class MemberAddres(db.Model):
    __tablename__ = 'member_address'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    nickname = db.Column(db.String(20, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    weChatNum = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    province_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    city_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    area_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    hide_address = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    address = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, primary_key=True, nullable=False, server_default=db.FetchedValue())
    is_default = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
