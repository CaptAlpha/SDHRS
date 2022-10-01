from flask import Flask,render_template,request,redirect,url_for
import cv2
import subprocess as sp
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hospitalReview.db'
#initil=alize database
DB=SQLAlchemy(app)

#create db model
class City(DB.Model):
    id=DB.Column(DB.Integer,primary_key=True,autoincrement=True)
    name=DB.Column(DB.String(50),nullable=False)

    def __repr__(self):
        return '<City %r>' % self.id

class Hospital(DB.Model):
    id=DB.Column(DB.Integer,primary_key=True,autoincrement=True)
    name=DB.Column(DB.String(50),nullable=False)
    city_id=DB.Column(DB.Integer,DB.ForeignKey('city.id'),nullable=False)
    speciality=DB.Column(DB.String(50),nullable=False,default='General')

    def __repr__(self):
        return '<Hospital %r>' % self.id

class Review(DB.Model):
    id=DB.Column(DB.Integer,primary_key=True,autoincrement=True)
    name=DB.Column(DB.String(50),nullable=False)
    hospital_id=DB.Column(DB.Integer,DB.ForeignKey('hospital.id'),nullable=False)
    review=DB.Column(DB.String(100),nullable=False)
    date_created=DB.Column(DB.VARCHAR(10))
    rating=DB.Column(DB.Numeric,nullable=True,default=4)
    confidence=DB.Column(DB.String(5),nullable=True,default=90.0)

    def __repr__(self):
        return '<Review %r>' % self.id

class User(DB.Model):
    id=DB.Column(DB.Integer,primary_key=True,autoincrement=True)
    name=DB.Column(DB.String(50),nullable=False)
    email=DB.Column(DB.String(50),nullable=False)
    password=DB.Column(DB.String(50),nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

if __name__=='__main__':
    DB.create_all()
    app.run(debug=True)