import boto3
import pandas as pd
import json

# Initialize the S3 client
s3 = boto3.client('s3')

# Function to list objects and get metadata from S3
def list_s3_objects_with_time(bucket_name):
    objects = s3.list_objects_v2(Bucket=bucket_name)
    object_info = []
    
    for obj in objects.get('Contents', []):
        key = obj['Key']
        last_modified = obj['LastModified']
        object_info.append({'Key': key, 'LastModified': last_modified})
    
    return object_info

# Function to read the object data from S3
def read_s3_object(bucket_name, object_key):
    obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    return obj['Body'].read()

# Parse JSON data
def parse_object_data(data):
    return json.loads(data)

# Function to fetch data from S3 and save it locally
def fetch_and_save_data(bucket_name, local_file):
    object_info_list = list_s3_objects_with_time(bucket_name)
    data_list = []
    
    for obj_info in object_info_list:
        key = obj_info['Key']
        last_modified = obj_info['LastModified']
        
        # Read the data from the object
        raw_data = read_s3_object(bucket_name, key)
        
        # Parse the JSON data
        parsed_data = parse_object_data(raw_data)
        
        # Add the timestamp (LastModified) to the parsed data
        parsed_data['timestamp'] = last_modified
        
        # Add to the list
        data_list.append(parsed_data)
    
    # Save data to a local CSV file
    if data_list:
        df = pd.DataFrame(data_list)
        df.to_csv(local_file, index=False)
        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no data is fetched

# Call this function once to fetch data from S3 and store it locally
bucket_name = 'soil-bucket-aws-iot'
local_file = 'soil_data.csv'
fetch_and_save_data(bucket_name, local_file)
