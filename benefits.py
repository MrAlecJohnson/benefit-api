#!flask/bin/python
from flask import Flask

app = Flask(__name__)

benefits = [
    {
        'id': 1,
        'benefit': u'Universal Credit',
        'abbrev': u'UC',
        'current': '2018-19'
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/')
def index():
    return "Flask test"

if __name__ == '__main__':
    app.run(debug=True)
