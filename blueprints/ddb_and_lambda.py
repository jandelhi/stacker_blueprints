from troposphere import (
    Base64, GetAtt, FindInMap, Join, Output, Ref, Parameter, Template, constants
)
from troposphere.dynamodb import (
    Table, KeySchema, AttributeDefinition, ProvisionedThroughput, StreamSpecification
)
from troposphere.awslambda import (
  Function, Code, MEMORY_VALUES, Environment
)
from troposphere.iam import ( 
  Role, Policy
)
from stacker.blueprints.base import Blueprint

class ddb_and_lambda(Blueprint):  
  def create_lambda_role(self):
    t = self.template
    self.LambdaExecutionRole = t.add_resource(Role(
    "ddbElasticsearchBridge",
    Path="/",
    Policies=[Policy(
        PolicyName="root",
        PolicyDocument={
            "Version": "2012-10-17",
            "Statement": [{
                "Action": ["es:ESHttpPost"],
                "Resource": ES DOMAIN HERE + "/*",
                "Effect": "Allow"
            },
            {
              "Action": [
                  "dynamodb:DescribeStream",
                  "dynamodb:GetRecords",
                  "dynamodb:GetShardIterator",
                  "dynamodb:ListStreams"],
              "Effect": "Allow",
              "Resource": GetAtt(self.dynamoTable, "StreamArn")
            }]
        })],
    AssumeRolePolicyDocument={
        "Version": "2012-10-17",
        "Statement": [{
            "Action": ["sts:AssumeRole"],
            "Effect": "Allow",
            "Principal": {
                "Service": ["lambda.amazonaws.com"]
            }
        }]
      },
    ))  

  def create_dynamo_table(self):
    t = self.template
    self.dynamoTable = t.add_resource(Table(
        "moviesDBTable",
        AttributeDefinitions=[
            AttributeDefinition(
                AttributeName="id",
                AttributeType="S"
            )
        ],
        KeySchema=[
            KeySchema(
                AttributeName="id",
                KeyType="HASH"
            )
        ],
        ProvisionedThroughput=ProvisionedThroughput(
            ReadCapacityUnits=5,
            WriteCapacityUnits=5
        ),
        StreamSpecification=StreamSpecification(
            StreamViewType="NEW_IMAGE"
        )
    ))
    t.add_output(Output(
        "TableName",
        Value=Ref(self.dynamoTable),
        Description="Table name of my new sample table"
    ))
    t.add_output(Output(
      "StreamArn",
      Value=GetAtt(self.dynamoTable, "StreamArn")
    ))
    
  def create_lambda_function(self):
    self.create_lambda_role()
    t = self.template
    self.lambda_fn = t.add_resource(Function(
      "Function",
      Code=Code(S3Bucket="js-test-buckett", S3Key="lambda_code.zip"),
      Description="Function that streams data from DDB Streams to ElasticSearch",
      Environment=Environment(
        Variables={
          "ES_ENDPOINT": ES ENDPOINT HERE,
          "ES_INDEX": "movies",
          "ES_DOCTYPE": "movie"
      }),
      Handler="lambda_code.handler",
      Role=GetAtt(self.LambdaExecutionRole, "Arn"),
      Runtime="nodejs6.10"
    ))  
    t.add_output(
        Output("FunctionName", Value=Ref(self.lambda_fn))
    )
    t.add_output(
        Output("FunctionArn", Value=GetAtt(self.lambda_fn,"Arn"))
    )

  def create_template(self):
    self.create_dynamo_table()
    self.create_lambda_function()   