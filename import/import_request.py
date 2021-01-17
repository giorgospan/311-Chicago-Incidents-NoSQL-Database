from pymongo import MongoClient
import pandas as pd
import os

# Connect to our MongoDB
URI = 'mongodb://localhost:27017'
client = MongoClient(URI)
db = client.chicago_db
db.drop_collection('request')


def insert(filename):
    # Read csv into a df
    df = pd.read_csv(INPUT_DIR + filename)

    print("=" * len(filename))
    print(filename)
    print("=" * len(filename))
    print()

    new_column_names = {

        # Common
        'Street Address': 'street_address',
        'Creation Date': 'creation_date',
        'Completion Date': 'completion_date',
        'Status': 'status',
        'Service Request Number': 'request_number',
        'Zip Code': 'zip_code',
        'Zip Codes': 'zip_codes',
        'Ward': 'ward',
        'Wards': 'wards',
        'Location': 'location',
        'Historical Wards 2003-2015': 'historical_wards',
        'Community Area': 'community_area',
        'Community Areas': 'community_areas',
        'Census Tracts': 'census_tracts',
        'Police District': 'police_district',
        'Type Of Service Request': 'request_type',
        'Latitude': 'latitude',
        'Longitude': 'longitude',
        'X Coordinate': 'x_coordinate',
        'Y Coordinate': 'y_coordinate',

        # RequestType-specific
        'Current Activity': 'current_activity',
        'Most Recent Action': 'most_recent_action',
        'Zip': 'zip_code',
        'Ssa': 'ssa',
        'License Plate': 'license_plate',
        'Vehicle Color': 'vehicle_color',
        'Vehicle Make/Model': 'vehicle_model',
        'How Many Days Has The Vehicle Been Reported As Parked?': 'days_parked',
        'Number Of Black Carts Delivered': 'num_of_black_carts',
        'What Type Of Surface Is The Graffiti On?': 'graffiti_surface',
        'Where Is The Graffiti Located?': 'graffiti_location',
        'Number Of Potholes Filled On Block': 'potholes_filled',
        'Number Of Premises Baited': 'premises_baited',
        'Number Of Premises With Garbage': 'premises_with_garbage',
        'Number Of Premises With Rats': 'premises_with_rats',
        'What Is The Nature Of This Code Violation?': 'nature',
        'If Yes, Where Is The Debris Located?': 'debris_location',
        'Location Of Trees': 'tree_location'

    }

    # Remove duplicate rows
    df = df[~df.duplicated()]

    # Rename column names to match column names in our DB
    df.columns = map(str.title, df.columns)
    df.rename(columns=new_column_names, inplace=True)

    # Drop location column [redundant]
    df.drop(columns=['location'], inplace=True)

    # Convert date strings to timestamps
    df['creation_date'] = pd.to_datetime(df['creation_date'], format='%Y-%m-%dT%H:%M:%S')
    df['completion_date'] = pd.to_datetime(df['completion_date'], format='%Y-%m-%dT%H:%M:%S')

    # Applies only on './data/311-service-requests-street-lights-one-out.csv'
    df['request_type'] = df['request_type'].str.replace('Street Light Out', 'Street Light - 1/Out')

    # Applies only on './data/311-service-requests-pot-holes-reported.csv'
    df['request_type'] = df['request_type'].str.replace('Pot Hole in Street', 'Pothole in Street')

    # Filter license plates
    if 'license_plate' in df.columns:
        df['license_plate'] = df[df['license_plate'].str.len() < 10]['license_plate']

    # Drop rows that contain NaN Coordinates
    df.dropna(subset=['longitude', 'latitude'], inplace=True)

    # Create GeoJSON objects from long,lat
    df['location'] = [{'type': 'Point', 'coordinates': [long, lat]} for long, lat in zip(df.longitude, df.latitude)]
    df.drop(columns=['longitude', 'latitude'], inplace=True)

    # Convert zipcode to string
    mask = df['zip_code'].notna()
    df['zip_code'] = df[df['zip_code'].notna()]['zip_code'].astype(int).apply(str)
    if 'zip_codes' in df.columns:
        mask = df['zip_codes'].notna()
        df['zip_codes'] = df[df['zip_codes'].notna()]['zip_codes'].astype(int).apply(str)

    # Exclude empty fields
    out = [dict((k, v) for k, v in zip(df.columns, row) if v is not None and v == v) for row in df.values]

    # Insert into our collection
    db.request.insert_many(out)


INPUT_DIR = './data/'
input_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.csv')]
input_files.remove('311-service-requests-vacant-and-abandoned-buildings-reported.csv')

# Insert each csv file in our request collection
for f in input_files:
    insert(f)
