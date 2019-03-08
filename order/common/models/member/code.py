# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy
from application import db


class Code(db.Model):
    __tablename__ = 'code'

    id = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    code = db.Column(db.String(255), nullable=False)
    updatetime = db.Column(db.DateTime, nullable=False)
    creattime = db.Column(db.DateTime, nullable=False)
