# stacker_blueprints
Blueprints for stacker using troposphere

## BUILD and UPLOAD to Cloudformation
This can be done 2 ways:

1. From the root folder of the project, run the following command:

```$ stacker build -d dump -r us-east-1 [env] [config]```
  
This outputs a Cloudformation json template in `dumps` folder. This template can be uploaded at the time of a stack's creation.

2. From the root folder of the project, run the following command:

```stacker build --stacks [stacks] -t [env] [config]```

This uploads the json template to an s3 bucket and creates stacks for you in Cloudformation.