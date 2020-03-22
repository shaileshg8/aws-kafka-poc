import json
import os
import sys
sys.path.insert(0, 'src/vendor')
import boto3
from kafka import KafkaProducer

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# Helper function to validate event
def validate_event(event):
    if 'kfk_server' not in event:
        return 'Error: Missing kfk_server in event'
    if 'topic_name' not in event:
        return 'Error: Missing topic_name in event'
    if 'student_id' not in event:
        return 'Error: Missing student_id in event'
    return 'ok'

# Helper function to validate dynamo db item
# if any of the requried field is missing it will throw error
def validate_response(data):
    if 'id' not in data:
        return 'Error: Missing id in dynamo db table'
    if 'name' not in data:
        return 'Error: Missing name in dynamo db table'
    if 'start_date' not in data:
        return 'Error: Missing start_date in dynamo db table'
    if 'end_date' not in data:
        return 'Error: Missing end_date in dynamo db table'
    if 'amount' not in data:
        return 'Error: Missing amount in dynamo db table'
    if 'state' not in data:
        return 'Error: Missing state in dynamo db table'
    return 'ok'

# helper method to map dynamo db item to final response
# if any more field is require add here
def map_response(data):
    response = {}
    response['id'] = data['id']
    response['name'] = data['name']
    response['start_date'] = data['start_date']
    response['end_date'] = data['end_date']
    response['amount'] = data['amount']
    response['state'] = data['state']
    return response

# Entry Method
# Handler method for the lambda function
def handler(event, context):
    result = 'ok'

    # validating event
    validate = validate_event(event)
    if validate != 'ok':
        return validate

    # Getting values from event passed to lambda
    kfk_server = event['kfk_server']
    topic_name = event['topic_name']
    student_id = event['student_id']

    # Initializing dynamodb client
    client = boto3.client('dynamodb')
    
    #Getting table name from environment variable set in serverless yml
    # To update the dynamo db name you can update config.yml file
    table_name = os.environ['DYNAMO_DB_NAME']

    # if dynamo db name is fed to lambda through event, use this name
    if 'dynamo_db_name' in event:
        table_name = event['dynamo_db_name']
    
    try:
        # getting item from dynamo db table
        response = client.get_item(
            TableName=table_name,
            Key={
                'id': {'S': student_id}
            }
        )

        # validating the dynamo db item if requried data is missing
        validate_item = validate_response(response['Item'])
        if validate_item != 'ok':
            return validate
        
        # map the dynamo db item to final response
        # only required data is added, others are ignored
        mapped_res = map_response(response['Item'])
        result=json.dumps(mapped_res, indent=2, cls=DecimalEncoder)

        # Creating a kafka client that publishes records
        # it needs kfk_server fed to lambda in event
        producer = KafkaProducer(bootstrap_servers=[kfk_server])

        # using producer to send the message to topic_name as provided in event
        send_message = producer.send(topic_name, result)

        try:
            record_metadata = send_message.get(timeout=10)
            print(record_metadata.topic)
            print(record_metadata.partition)
        except Exception as ke:
            # Decide what to do if produce request failed...
            print(ke)
            result = 'Fail'
        finally:
            producer.close()
    except Exception as e:
        print(e)
        result = 'Fail'
    return result;
