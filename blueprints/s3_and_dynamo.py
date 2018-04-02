from troposphere import (
    Base64, GetAtt, FindInMap, Join, Output, Ref, Parameter, Template
)
from troposphere.s3 import (
    Bucket, PublicRead, WebsiteConfiguration
)
from troposphere.dynamodb import (
    Table, KeySchema, AttributeDefinition, ProvisionedThroughput
)
from stacker.blueprints.base import Blueprint

class s3_and_dynamo(Blueprint):
    def create_s3_bucket(self):
        t = self.template
        self.s3Bucket = t.add_resource(Bucket(
            "testS3Bucket",
            AccessControl=PublicRead,
            WebsiteConfiguration=WebsiteConfiguration(
                IndexDocument="index.html",
                ErrorDocument="error.html"
                )
            ))
        t.add_output([
            Output(
                "WebsiteURL",
                Value=GetAtt(self.s3Bucket, "WebsiteURL"),
                Description="URL for website hosted on S3"
                ),
            Output(
                "S3BucketSecureURL",
                Value=Join("", ["http://", GetAtt(self.s3Bucket, "DomainName")]),
                Description="Name of S3 bucket to hold website content"
                ),
            ])

    def create_dynamo_table(self):
        t = self.template

        self.dynamoTable = t.add_resource(Table(
            "sampleDBTable",
            AttributeDefinitions=[
                AttributeDefinition(
                    AttributeName="artist",
                    AttributeType="S"
                ),
                AttributeDefinition(
                    AttributeName="album",
                    AttributeType="S"
                )
            ],
            KeySchema=[
                KeySchema(
                    AttributeName="artist",
                    KeyType="HASH"
                ),
                KeySchema(
                    AttributeName="album",
                    KeyType="RANGE"
                )
            ],
            ProvisionedThroughput=ProvisionedThroughput(
                ReadCapacityUnits=5,
                WriteCapacityUnits=5
            )
        ))

        t.add_output(Output(
            "TableName",
            Value=Ref(self.dynamoTable),
            Description="Table name of my new sample table"
        ))
        
    def create_template(self):
        self.create_s3_bucket();
        self.create_dynamo_table();