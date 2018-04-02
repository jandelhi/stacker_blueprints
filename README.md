# stacker_blueprints
Blueprints for stacker using troposphere

## BUILD and UPLOAD to Cloudformation
From the root folder of the project, run the following command:

```$ stacker build -d dump -r us-east-1 [env] [config]```
  
This outputs a Cloudformation json template in `dumps` folder. This template can be uploaded at the time of a stack's creation.
