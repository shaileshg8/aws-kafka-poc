#aws-kafka-topic
```
This is a sample project to demonstrate: to read data from dynamo db table and send the data over to kafka topic.
This project uses python, boto3 and kafka-python
pip install boto3
pip install kafka-python

Before installation please verify your aws credentials
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

Go to your AWS Management Console in your web browser
Navigate to Dynamo Db service, and create a table called 'aws-kafka-topic-table'
Manually insert data with Partition Key , 'id'
```

#Installation
```
clone the project, cd to project directory
npm i
```
#Deployment
```
npm run deploy
```

#Invocation
```
npm run invoke
```

#Remove
```
npm run remove
```