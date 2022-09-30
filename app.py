from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from flask import send_file
import os
import pandas as pd
import cohere
from cohere.classify import Example

co = cohere.Client('xprvLYyVPF4XKxRqRUb1ADD9TiQ8ATDCKN6kuqVk')

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        review = request.form['review']
        response = co.classify(inputs=[review], model='996de6b6-76c2-411b-97b7-aa58f15e75ad-ft')
        prediction=response.classifications[0].prediction
        confidence=response.classifications[0].confidence[int(prediction)].confidence
        genuinity='genuine' if int(prediction)==0 else 'fake'
        return render_template('index.html', result='Your review is {:0.2f}% {}'.format(confidence*100, genuinity))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

