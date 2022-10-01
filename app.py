from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import pandas as pd
import cohere
import json
from algosdk.v2client import algod
from algosdk import account, mnemonic, kmd
from algosdk.future import transaction
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
from cohere.classify import Example
from db import DB, City, Hospital, Review, User
from models.NLP.wordcloud1 import generate_wordcloud

co = cohere.Client('xprvLYyVPF4XKxRqRUb1ADD9TiQ8ATDCKN6kuqVk')

app=Flask(__name__)
DB.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hospitalReview.db'

VERIFICATION_TOKEN = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hosp=request.form['hospitalName']
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
        #get the wordcloud
        generate_wordcloud(reviewList)

        print(reviewList)
        # join the reviews by \n
        reviewString='||'.join(reviewList)
        #redirect to transaction route
        return redirect(url_for('addReview', hospitalName=hospitalName, cityName=cityName, speciality=speciality,reviewList=reviewString))

    return render_template('index.html')

@app.route('/addReview', methods=['GET', 'POST'])
def addReview():
    if request.method=='POST':
        return redirect(url_for('txn'))
    return render_template('index2.html', hospitalName=request.args.get('hospitalName'), cityName=request.args.get('cityName'), speciality=request.args.get('speciality'), reviewList=request.args.get('reviewList'))
    

@app.route('/transaction', methods=['GET', 'POST'])
def txn():
    if request.method == 'POST':
        review = request.form['review']
        pp = request.form['pp']
        hospitalName = request.form['hospitalName']

        algod_address = "https://testnet-algorand.api.purestake.io/ps2"
        algod_token = ""
        headers = {
            "X-API-Key": "LznYKjBylk53uEV5UDlN57lolkR64tnr1VHwsM19",
        }

        # my_wallet
        my_address = 'QZ4JHEU6QEXZCB52W7ABKLOXNSH6PBOSFNU4VVJNYNCIRVAP6UWLB3IQMU'
        my_passphrase = 'cargo blush ocean cluster divert spider bunker gain excite shop jeans romance buzz loan potato stick people receive cross cheese unfair alter wild ability drop'
        
        # Client Wallet 
        client_pp = pp
        client_address = mnemonic.to_public_key(client_pp)
        print("Client address: {}".format(client_address))
        client_SK = mnemonic.to_private_key(client_pp)
        print("Client private key: {}".format(client_SK))

        # Initialize an algod client
        algod_client = algod.AlgodClient(algod_token, algod_address, headers)

        # Get the relevant params from the algod    
        params = algod_client.suggested_params()
        params.flat_fee = True
        params.fee = 1000
        send_amount = 10000

        txn = transaction.PaymentTxn(client_address, params, my_address, send_amount)
        signed_txn = txn.sign(client_SK)
        
        txid = algod_client.send_transaction(signed_txn)
        if(txid):
            print("Transaction sent, transaction ID: {}".format(txid))
            txnStr = str('Transaction Successful with TransactionID: {}'.format(txid))
            VERIFICATION_TOKEN = txid
        else:
            print("Transaction Failed")
            txnStr = str('Transaction Failed')
        return redirect(url_for('success', result=txnStr, VERIFICATION_TOKEN=VERIFICATION_TOKEN, hospitalName=hospitalName, review=review))
        
    return render_template('transaction.html')

print(VERIFICATION_TOKEN)
#Successful transaction page
@app.route('/success', methods=['GET', 'POST'])
def success():
    VERIFICATION_TOKEN = request.args.get('VERIFICATION_TOKEN')
    hospitalName = request.args.get('hospitalName')
    review = request.args.get('review')
    if(VERIFICATION_TOKEN):
        #check genuinity of the review
        response = co.classify(inputs=[review], model='996de6b6-76c2-411b-97b7-aa58f15e75ad-ft')
        prediction=response.classifications[0].prediction
        confidence=response.classifications[0].confidence[int(prediction)].confidence
        genuinity='genuine' if int(prediction)==0 else 'fake'
        #write the review to the database if it is genuine
        if genuinity=='genuine':
            #get id from hospital name
            hospital=Hospital.query.filter_by(name=hospitalName).first()
            id=hospital.id
            newReview=Review(name='Anonymous',review=review,hospital_id=id,date_created='01/10/22')
            DB.session.add(newReview)
            DB.session.commit()
        return render_template('success.html', txnid=VERIFICATION_TOKEN,result=genuinity)
    return render_template('success.html', result=VERIFICATION_TOKEN)


if __name__ == '__main__':
    app.run(debug=True)

