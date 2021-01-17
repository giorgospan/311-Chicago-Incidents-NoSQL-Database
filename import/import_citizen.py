from faker import Faker
from pymongo import MongoClient
from random import randrange, choice
from math import ceil

CITIZENS = 4000
MAX_UPVOTES_PER_CITIZEN = 1000
FACTOR = 0.5  # FACTOR must be greater than 1/3

"""
Create unique upvotes for a citizen
"""


def create_unique_upvotes(num):
    pipeline = [{"$sample": {"size": num}}]
    upvotes = [doc['_id'] for doc in list(db.request.aggregate(pipeline))]
    while len(upvotes) != len(set(upvotes)):
        upvotes = [doc['_id'] for doc in list(db.request.aggregate(pipeline))]
    return upvotes


# Connect to our MongoDB
URI = 'mongodb://localhost:27017'
client = MongoClient(URI)
db = client.chicago_db
db.drop_collection('citizen')
request_count = db.request.count_documents({})
min_upvotes_per_citizen = ceil((FACTOR * request_count) / CITIZENS)

# Init faker
fake = Faker()

# Create unique usernames
usernames = [fake.unique.user_name() for _ in range(CITIZENS)]

# Create 90% distinct phone numbers [useful for query10]
phones = [fake.unique.phone_number() for _ in range(ceil(.9 * CITIZENS))]

# Create citizens
citizens = []
for c in range(CITIZENS):
    username = usernames[c]
    email = fake.email()
    phone = choice(phones)
    upvote_number = randrange(min_upvotes_per_citizen, MAX_UPVOTES_PER_CITIZEN + 1)
    upvote_list = create_unique_upvotes(upvote_number)
    citizens.append({
        'email': email,
        'username': username,
        'phone': phone,
        'upvotes': upvote_list
    })

# Insert citizens into our DB
db.citizen.insert_many(citizens)
