# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    Balance = db.Column(db.Integer, nullable=False)
    verif = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    _identity = db.Column(' identity', db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False,
                          server_default=db.FetchedValue())
    name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    schoolcode = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    weChatNum = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
