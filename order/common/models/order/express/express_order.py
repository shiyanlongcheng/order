# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class ExpressOrder(db.Model):
    __tablename__ = 'express_order'
    __table_args__ = (
        db.Index('idx_member_id_status', 'order_member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    order_sn = db.Column(db.String(40), nullable=False, unique=True, server_default=db.FetchedValue())
    order_member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    receipt_member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    pay_price = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    pay_sn = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    prepay_id = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue())
    note = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    needplaceid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    needplace = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    needtime = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    express_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_placeid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_place = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    express_code = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    express_sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_weight_id = db.Column(db.Integer)
    express_weight = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=db.FetchedValue())
    comment_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    pay_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    receipt_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    delivery_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    success_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
