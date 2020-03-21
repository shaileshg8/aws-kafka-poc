import boto3
import json
import os
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

# Handler method for the lambda function
def handler(event, context):
    result = 'ok'

    # validating event
    validate = validate_event(event)
    if validate != 'ok':
        return validate

    kfk_server = event['kfk_server']
    topic_name = event['topic_name']
    student_id = event['student_id']

    client = boto3.client('dynamodb')
    table_name = os.environ['DYNAMO_DB_NAME']
    
    try:
        # getting item from dynamo db table
        response = client.get_item(
            TableName=table_name,
            Key={
                'id': {'S': student_id}
            }
        )
        result=json.dumps(response, indent=2, cls=DecimalEncoder)

        producer = KafkaProducer(bootstrap_servers=[kfk_server])
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
