from troposphere import (
    Base64, GetAtt, FindInMap, Join, Output, Ref, Parameter, Template
)
from troposphere.s3 import (
    Bucket, PublicRead, WebsiteConfiguration
)
from troposphere.cloudfront import (
    Distribution, DistributionConfig, Origin, CustomOrigin, CacheBehavior, DefaultCacheBehavior, Cookies, ForwardedValues, S3Origin, Logging
)
from stacker.blueprints.base import Blueprint

class s3_and_cloudfront(Blueprint):
    def create_s3_bucket(self):
        t = self.template
        self.s3Bucket = t.add_resource(Bucket(
            "testS3Bucket2",
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

    def create_cloudfront_distr(self):
        t = self.template
        self.cloudfrontDistr = t.add_resource(Distribution(
            "jtdistr",
            DistributionConfig = DistributionConfig(
                Origins = [Origin(
                Id="Origin 1", 
                DomainName=GetAtt(self.s3Bucket, "DomainName"),
                S3OriginConfig=S3Origin())
            ],
            DefaultCacheBehavior=DefaultCacheBehavior(
                TargetOriginId="Origin 1",
                ForwardedValues = ForwardedValues(QueryString=False),
                ViewerProtocolPolicy="allow-all"
            ),
            Enabled = True,
            HttpVersion="http2"
            )))
        t.add_output([
            Output(
                "DistributionId",
                Value=Ref(self.cloudfrontDistr)
                ),
            Output(
                "DistributionName",
                Value=Join("", ["http://", GetAtt(self.cloudfrontDistr, "DomainName")]))
            ])

    def create_template(self):
        self.create_s3_bucket();
        self.create_cloudfront_distr();
    
