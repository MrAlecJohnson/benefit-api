#!flask/bin/python
from flask import Flask
import datetime

app = Flask(__name__)

benefits = [
    {
        'ben_id': 1,
        'name': 'Universal Credit',
        'abbrev': 'UC'
    }
]

rates = [
    {
        'rate_id': 1,
        'benefit': 1,
        'element': 'housing element' # what if I wanted to capitalise?
        'date': datetime(2018,4,1)
    }
]

@app.route('/benefits/api/v1/rates', methods=['GET'])
def get_tasks():
    return jsonify({'rates': rates})


if __name__ == '__main__':
    app.run(debug=True)
