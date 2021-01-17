from bson import ObjectId
from bson.json_util import dumps
from flask import Blueprint, request
from datetime import datetime
from ..extensions import mongo
from ..utils.utils import *

api = Blueprint('api', __name__)

"""
Find the total requests per type that were created within a specified time range and sort
them in a descending order.
"""


@api.route('/query1')
def query1():
    fr = datetime.strptime(request.args.get('fr'), DATETIME_FORMAT)
    to = datetime.strptime(request.args.get('to'), DATETIME_FORMAT)

    result = mongo.db.request.aggregate([
        {'$match': {'creation_date': {'$gte': fr, '$lt': to}}},
        {'$group': {'_id': '$request_type', 'total_requests': {'$sum': 1}}},
        {'$sort': {'total_requests': -1}},
        {'$project': {'_id': 0, 'type': '$_id', 'total_requests': 1}}

    ])
    return dumps(result)


"""
Find the number of total requests per day for a specified request type and time range.
"""


@api.route('/query2')
def query2():
    fr = datetime.strptime(request.args.get('fr'), DATETIME_FORMAT)
    to = datetime.strptime(request.args.get('to'), DATETIME_FORMAT)
    given_type = request.args.get('type')

    result = mongo.db.request.aggregate([
        {'$match': {'$and': [{'creation_date': {'$gte': fr, '$lt': to}}, {'request_type': given_type}]}},
        {
            '$group':
                {
                    '_id': {'$dateToString': {'format': '%d-%m-%Y', 'date': '$creation_date'}},
                    'total_requests': {'$sum': 1}
                }
        },
        {'$project': {'_id': 0, 'day': '$_id', 'total_requests': 1}}
    ])
    return dumps(result)


"""
Find the three most common service requests per zipcode for a specified day.
"""


@api.route('/query3')
def query3():
    day = datetime.strptime(request.args.get('day'), DATE_FORMAT)

    result = mongo.db.request.aggregate([
        {'$match': {'creation_date': day}},
        {
            '$group':
                {
                    '_id':
                        {
                            'zip_code': '$zip_code',
                            'type': '$request_type'
                        },
                    'requests_per_zip_type': {'$sum': 1}
                }
        },
        {'$project': {'_id': 0, 'zip_code': '$_id.zip_code', 'type': '$_id.type', 'requests_per_zip_type': 1}},
        {'$sort': {'zip_code': -1, 'requests_per_zip_type': -1}},
        {
            '$group':
                {
                    '_id': '$zip_code',
                    'types': {
                        '$push': {
                            'requests_per_zip_type': '$requests_per_zip_type',
                            'type': '$type'
                        }
                    }
                }
        },
        {'$project': {'_id': 0, 'zip_code': '$_id', 'types': {'$slice': ['$types', 3]}}}
    ])
    return dumps(result)


"""
Find the three least common wards with regards to a given service request type.
"""


@api.route('/query4')
def query4():
    given_type = request.args.get('type')

    results = mongo.db.request.aggregate([
        {'$match': {'request_type': given_type, 'ward': {'$exists': True}}},
        {'$group': {'_id': '$ward', 'total_requests': {'$sum': 1}}},
        {'$sort': {'total_requests': 1}},
        {'$limit': 3},
        {'$project': {'_id': 0, 'ward': '$_id', 'total_requests': 1}}
    ])

    return dumps(results)


"""
Find the average completion time per service request for a specified date range.
"""


@api.route('/query5')
def query5():
    fr = datetime.strptime(request.args.get('fr'), DATETIME_FORMAT)
    to = datetime.strptime(request.args.get('to'), DATETIME_FORMAT)
    results = mongo.db.request.aggregate([

        {'$match': {'creation_date': {'$gte': fr, '$lt': to}}},
        {
            '$project':
                {
                    'diff': {
                        '$divide': [
                            {'$subtract': ['$completion_date', '$creation_date']},
                            1000 * 60 * 60 * 24
                        ]
                    },
                    'request_type': 1,
                }
        },
        {'$group': {'_id': '$request_type', 'avg_days': {'$avg': '$diff'}}},
        {'$project': {'_id': 0, 'request_type': '$_id', 'avg_days': {'$floor': '$avg_days'}}}
    ])

    return dumps(results)


"""
Find the most common service request in a specified bounding box for a specified day. You
are encouraged to use GeoJSON objects and Geospatial Query Operators.
"""


@api.route('/query6')
def query6():
    xmin = float(request.args.get('xmin'))
    ymin = float(request.args.get('ymin'))
    xmax = float(request.args.get('xmax'))
    ymax = float(request.args.get('ymax'))
    day = datetime.strptime(request.args.get('day'), DATE_FORMAT)

    results = mongo.db.request.aggregate([

        {
            '$match':
                {
                    'location': {'$geoWithin': {'$box': [[xmin, ymin], [xmax, ymax]]}},
                    'creation_date': day
                }
        },
        {'$group': {'_id': '$request_type', 'total_requests': {'$sum': 1}}},
        {'$sort': {'total_requests': -1}},
        {'$limit': 1},
        {'$project': {'_id': 0, 'request_type': '$_id', 'total_requests': 1}}
    ])

    return dumps(results)


"""
Find the fifty most upvoted service requests for a specified day.
"""


@api.route('/query7')
def query7():
    day = datetime.strptime(request.args.get('day'), DATE_FORMAT)
    results = mongo.db.request.aggregate([

        {'$match': {'creation_date': day}},
        {'$project': {'_id': 1}},
        {
            '$lookup':
                {
                    'from': 'citizen',
                    'localField': '_id',
                    'foreignField': 'upvotes',
                    'as': 'upvotes'
                }
        },
        {'$project': {'upvotes': {'$size': '$upvotes'}, '_id': 0, 'request_id': '$_id'}},
        {'$sort': {'votes': -1}},
        {'$limit': 50}
    ])

    return dumps(results)


"""
Find the fifty most active citizens, with regard to the total number of upvotes.
"""


@api.route('/query8')
def query8():
    results = mongo.db.citizen.aggregate([

        {'$project': {'username': 1, 'totalupvotes': {'$size': '$upvotes'}}},
        {'$sort': {'totalupvotes': -1}},
        {'$limit': 50}
    ])

    return dumps(results)


"""
Find the top fifty citizens, with regard to the total number of wards for which they have
upvoted an incidents.
"""


@api.route('/query9')
def query9():
    results = mongo.db.citizen.aggregate([
        {
            '$lookup':
                {
                    'from': 'request',
                    'localField': 'upvotes',
                    'foreignField': '_id',
                    'as': 'upvotes'
                }
        },
        {'$unwind': '$upvotes'},
        {
            '$group':
                {
                    "_id": "$_id",
                    'distinct_wards': {'$addToSet': '$upvotes.ward'}
                }
        },
        {'$project': {'totalwards': {'$size': '$distinct_wards'}}},
        {'$sort': {'totalwards': -1}},
        {'$limit': 50}
    ])

    return dumps(results)


"""
Find all incident ids for which the same telephone number has been used for more than one
names.
"""


@api.route('/query10')
def query10():
    results = mongo.db.citizen.aggregate([

        {
            '$group': {
                '_id': '$phone',
                'upvotes': {
                    '$push': '$upvotes'
                },
                'total': {
                    '$sum': 1
                }
            }
        },
        {
            '$match': {
                'total': {
                    '$gte': 2
                }
            }
        },
        {
            '$unwind': '$upvotes'
        },
        {
            '$unwind': '$upvotes'
        },
        {
            '$group': {
                '_id': '$upvotes'
            }
        }
    ])

    return dumps(results)


"""
Find all the wards in which a given name has casted a vote for an incident taking place in it.
"""


@api.route('/query11')
def query11():

    username = request.args.get('username')

    results = mongo.db.citizen.aggregate([
        {'$match': {'username': username}},
        {
            '$lookup':
                {
                    'from': 'request',
                    'localField': 'upvotes',
                    'foreignField': '_id',
                    'as': 'upvotes'
                }
        },
        {'$unwind': '$upvotes'},
        {'$group': {'_id': '$upvotes.ward'}},
        {'$project': {'_id': 0, 'ward': '$_id'}}
    ])

    return dumps(results)


"""
Insert a new incident
"""


@api.route('/insert-incident', methods=['POST'])
def insert_incident():
    data = request.get_json()

    error_message = is_valid(data)
    if error_message:
        return '<h1>Insertion Failed<h1>' + error_message

    data['creation_date'] = datetime.strptime(data['creation_date'], DATETIME_FORMAT)
    data['completion_date'] = datetime.strptime(data['completion_date'], DATETIME_FORMAT)
    mongo.db.request.insert(data)
    return '<h1> Successful insert </h1>'


"""
Cast an upvote. 
In case the same user casts a vote for the same incident a second time, the vote should be rejected.
"""


@api.route('/insert-upvote', methods=['POST'])
def insert_upvote():
    data = request.get_json()

    res = mongo.db.citizen.update_one(
        {"_id": ObjectId(data['citizen_id'])},
        {'$addToSet': {"upvotes": ObjectId(data['incident_id'])}}
    )

    if res.modified_count == 1:
        return '<h1> Successful upvote </h1>'
    else:
        return '<h1> Upvote already exists </h1>'
