# aws-kafka-topic
```
This is a sample project to demonstrate: to read data from dynamo db table and send the data over to kafka topic.
This project uses python, boto3 and kafka-python
pip install boto3
pip install kafka-python

Before installation please verify your aws credentials
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
```

# Setting up Dynamo Db Table
```
Go to your AWS Management Console in your web browser
Navigate to Dynamo Db service, and create a table.
Update the config.yml, with the name you provided or you can feed the lambda the dynamo db name (eg. event/kafkaTopic.json)
{
    "dynamo_db_name": "aws-kafka-topic-table",
    "kfk_server": "localhost:9092",
    "topic_name": "myTopic",
    "student_id": "44"
}


Manually insert data with Partition Key , 'id'
Example Sample data:
{
  "amount": 1200,
  "end_date": "2020-03-22T04:36:10.418Z",
  "id": "44",
  "name": "test",
  "start_date": "2020-03-22T04:36:10.418Z",
  "state": "monthly"
}

If any of the data is missing in the dynamo db table, lambda will throw error

```

# Apache Kafka
```
Get the kafka server name and feed the lambda the server name and topic
eg: event/kafkaTopic.json
Sample:
{
    "dynamo_db_name": "aws-kafka-topic-table",
    "kfk_server": "localhost:9092",
    "topic_name": "myTopic",
    "student_id": "44"
}
```

# Response
```
Lamda will send a message to a kafka topic
Sample Response data sedn to kafka topic:
{
  "amount": 1200,
  "end_date": "2020-03-22T04:36:10.418Z",
  "id": "44",
  "name": "test",
  "start_date": "2020-03-22T04:36:10.418Z",
  "state": "monthly"
}
```

# Installation
```
clone the project, cd to project directory
npm i
```

# Deployment
```
npm run prepare
npm run deploy
```

# Invocation
```
npm run invoke
```

# Remove
```
npm run remove
```
