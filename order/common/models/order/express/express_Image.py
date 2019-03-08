# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class ExpressImage(db.Model):
    __tablename__ = 'express_Image'

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    eporder_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    eporder_sn = db.Column(db.String(40), nullable=False, server_default=db.FetchedValue())
    imagename = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    imageurl = db.Column(db.String(255, 'utf8_general_ci'), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
