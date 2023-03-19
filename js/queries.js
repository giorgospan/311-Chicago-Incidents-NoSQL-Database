//Query1
db.request.aggregate([
    {'$match': {'creation_date': {'$gte': ISODate('2014-01-01T20:20:00'), '$lt': ISODate('2014-09-01T20:20:00')}}},
    {'$group': {'_id': '$request_type', 'total_requests': {'$sum': 1}}},
    {'$sort': {'total_requests': -1}},
    {'$project': {'_id': 0, 'type': '$_id', 'total_requests': 1}}
])

//Query2
db.request.aggregate([
    {'$match': {'$and': [{'creation_date': {'$gte': ISODate('2014-01-01T20:20:00'), '$lt': ISODate('2014-09-01T20:20:00')}}, {'request_type': 'Tree Trim'}]}},
    {'$group': {'_id': {'$dateToString':{'format':'%d-%m-%Y',date:'$creation_date'}} , 'total_requests': {'$sum': 1}}},
    {'$project': {'_id': 0, 'day': '$_id', 'total_requests': 1}}
])

//Query3
db.request.aggregate([
    {'$match':{'creation_date':ISODate('2014-01-01')}},
    {
        '$group': 
        {
            '_id': 
            {
                'zip_code':'$zip_code',
                'type':'$request_type'
            }, 
            'requests_per_zip_type': {'$sum': 1}
        }
    },
    {'$project': {'_id': 0, 'zip_code': '$_id.zip_code', 'type':'$_id.type', 'requests_per_zip_type': 1}},
    {'$sort':{'zip_code':-1,'requests_per_zip_type':-1}},
    {'$group':
        {
            '_id': '$zip_code',
            'counts': {
                '$push': {
                    'requests_per_zip_type': '$requests_per_zip_type',
                    'type': '$type'
                }
            }
        }
    },
    {'$project':{'_id':0,'zip_code':'$_id','counts':{ '$slice':['$counts',3]}}}
])

//Query4
db.request.aggregate([

    {'$match':{'request_type':'Tree Debris','ward':{'$exists':true}}},
    {'$group': {'_id': '$ward', 'total_requests': {'$sum': 1}}},
    {'$sort':{'total_requests':1}},
    {'$limit':3},
    {'$project':{'_id':0,'ward':'$_id','total_requests':1}}
])


//Query5
db.request.aggregate([

    {'$match': {'creation_date': {'$gte': ISODate('2014-01-01T20:20:00'), '$lt': ISODate('2014-09-01T20:20:00')}}},
    {'$project':
        {
            'diff':{
                '$divide':[
                {'$subtract':['$completion_date','$creation_date']},
                1000 * 60 * 60 * 24
                ]
            },
            'request_type':1,
        }
    },
    {'$group':{'_id':'$request_type', 'avg_days':{'$avg':'$diff'}}},
    {'$project':{'_id':0,'request_type':'$_id','avg_days':{'$floor':'$avg_days'}}}
])

//Query6
db.request.aggregate([

    {'$match':
        {
            'location': { '$geoWithin': { '$box':  [ [ -87.67273, 41.846234 ], [ -87.628981, 41.893898 ] ]} }, 
            'creation_date':ISODate('2014-01-01')
        }
    },
    {'$group': {'_id': '$request_type', 'total_requests': {'$sum': 1}}},
    {'$sort':{'total_requests':-1}},
    {'$limit':1},
    {'$project':{'_id':0,'request_type':'$_id','total_requests':1}}
])

//Query7
db.request.aggregate([

    {'$match':{'creation_date':ISODate('2014-01-01')}},
    {'$project':{'_id':1}},
    {'$lookup':
        {
            'from': 'citizen',
            'localField': '_id',
            'foreignField': 'upvotes',
            'as': 'upvotes'
        }
    },
    {'$project': {'upvotes': {'$size': '$upvotes'}, '_id': 0, 'request_id': '$_id'} },
    {'$sort': {'votes': -1 }},
    {'$limit': 50}
])

//Query8
db.citizen.aggregate([

    {'$project':{'username':1,'totalupvotes':{'$size':'$upvotes'}}},
    {'$sort':{'totalupvotes':-1}},
    {'$limit':50}
])

//Query9
db.citizen.aggregate([
    {
        '$lookup' :
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
    {'$sort': {'totalwards': -1 } },
    {'$limit': 50}
])

//Query10
db.citizen.aggregate([

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
    } , {
        '$match': {
            'total': {
                '$gte': 2
            }
        }
    }, {
        '$unwind': '$upvotes'
    }, {
        '$unwind': '$upvotes'
    }, {
        '$group': {
            '_id': '$upvotes'
        }
    },
])


//Query11
db.citizen.aggregate([
    {'$match': {'username': 'dcole'}},
    {
        '$lookup' :
        {
            'from': 'request',
            'localField': 'upvotes',
            'foreignField': '_id',
            'as': 'upvotes'
        }
    },
    {'$unwind': '$upvotes'},
    {'$group':{'_id':'$upvotes.ward'}},
    {'$project':{'_id':0,'ward':'$_id'}}
])