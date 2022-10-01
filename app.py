from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import pandas as pd
import cohere
from cohere.classify import Example
from db import DB, City, Hospital, Review, User

co = cohere.Client('xprvLYyVPF4XKxRqRUb1ADD9TiQ8ATDCKN6kuqVk')

app=Flask(__name__)
DB.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hospitalReview.db'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hosp=request.form['hospitalName']
        print(hosp)
        #get hospital city,speciality,reviews from the database
        hospital=Hospital.query.filter_by(name=hosp).first()
        city=City.query.filter_by(id=hospital.city_id).first()
        reviews=Review.query.filter_by(hospital_id=hospital.id).all()
        #get the reviews and put them in a list
        reviewList=[]
        for review in reviews:
            reviewList.append(review.review)
        #get the hospital name and city
        hospitalName=hospital.name
        cityName=city.name
        #get the speciality
        speciality=hospital.speciality
        
        return render_template('details.html',hospitalName=hospitalName,cityName=cityName,speciality=speciality,reviewList=reviewList)

    return render_template('index.html')


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        review = request.form['review']
        response = co.classify(inputs=[review], model='996de6b6-76c2-411b-97b7-aa58f15e75ad-ft')
        prediction=response.classifications[0].prediction
        confidence=response.classifications[0].confidence[int(prediction)].confidence
        genuinity='genuine' if int(prediction)==0 else 'fake'
        return render_template('index.html', result='Your review is {:0.2f}% {}'.format(confidence*100, genuinity))

    return render_template('index.html')

@app.route('/addReview', methods=['GET', 'POST'])
def addReview():
    if request.method == 'POST':
        review = request.form['review']
        hospitalName = request.form['hospitalName']
        hospital=Hospital.query.filter_by(name=hospitalName).first()
        review=Review(review=review,hospital_id=hospital.id)
        DB.session.add(review)
        DB.session.commit()
        return redirect(url_for('index'))
    return render_template('addReview.html')

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        pk = request.form['pk']
        sk = request.form['sk']
        pp = request.form['pp']
        print(pk,sk,pp)
        print('*************************************************')


    return render_template('transaction.html')

if __name__ == '__main__':
    app.run(debug=True)

