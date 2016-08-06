# extend_cfn_example
Example of extending CloudFormation with lambda custom resource.

## Preparation and Demonstration
Before for creating a custom resource in CloudFormation, you need to prepare a CloudFormation template that creates a lambda function. We will demonstrate a nested template, a child template will create our lambda function, another child template will create the VPC, after both are complete the parent template will call the custom resource to attach the VPC to a Route 53 internal hosted zone. The internal hosted zone ID will be passed to the parent template by use of a parameter. From here this blog turns into a tutorial.

### Assumptions:
You have an AWS Account.
You’re using Bash.
You have pip installed
You're the AWS CLI installed, preferred version 1.10.x or greater. Help
You have configured the CLI, set up AWS IAM access credentials. Help

### Step 1: Create a internal hosted zone. 
When creating a internal hosted zone you must specify a VPC, for this we will use one of the default VPC’s created with your AWS account. If you do not have a default VPC, create a dummy VPC and use that. If you feel more comfortable using the console feel free. If you already have a internal hosted zone you can skip this portion. 

```
VPCID=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query 'Vpcs[].VpcId' --output text --region us-east-1)

aws route53 create-hosted-zone --name example.internal --caller-reference 2016-08-06 --vpc VPCRegion=us-east-1,VPCId=$VPCID --hosted-zone-config Comment="command-line version",PrivateZone=true
```
You now have a internal hosted zone. It may take a moment to produce as the create-hosted-zone call is asynchronous. 

Get the internal hosted zone Id, this command will list all hosted zones, query for the one we just created, get it’s Id, and cut just the id, because the Id for some reason when returned by this command starts with /hostedzone/{Id}

```
aws route53 list-hosted-zones --query "HostedZones[?Name == 'example.internal.'].Id" --output text | cut -d/ -f3
```

### Step 2: Create a S3 Bucket.
You will need a S3 bucket to work out of, we will use this bucket to upload our CloudFormation templates and our lambda code zip. Create the bucket with the following CLI command or through the console. Keep in mind that S3 bucket names are globally unique and you will have to come up with a bucket name for yourself. 
```
aws s3 mb s3://extend_cfn_example_{yourName}
```

### Step 3: Clone the example Github project.
I have prepared a Github project with all of the example CloudFormation and code to get you off the ground. Clone this Github project to your local machine. 

https://github.com/dbrainnet/extend_cfn_example


### Step 4: Run the scripts.
You must run two scripts from within the Github project. Both of these scripts are to be ran from the base of the repository. 

Script 1: build_lambdas.sh, this script will utilize pip to install the required packages for the lambda to the local directory, zip up the lambda function with all of the dependencies and place it in a new directory ./builds/. 

```
./scripts/build_lambdas.sh
```

 Script 2: s3_sync.sh, this script will sync all the necessary files to your S3 bucket. The files it syncs are the builds and cloudformation directories. 

```
./scripts/s3_sync.sh -b extend_cfn_example_{yourName}
```

### Step 5: Create the CloudFormation Stack.
This is the final step in the demonstration, the following command sets the stack name to extend-cfn-example. The template url is specified, you will need to modify this to point at your own bucket. The parameters come next, the CloudToolsBucket parameter is the name of your bucket, the PrivateDomain parameter is the name of your internal hosted zone, and the InternalHostedZone parameter is the Id of the internal hosted zone you’ve created. After this you must provide IAM capabilities to this CloudFormation stack because we must create an IAM role for the lambda function to run. 

```
aws cloudformation create-stack --stack-name extend-cfn-example --template-url https://s3.amazonaws.com/extend_cfn_example_{yourName}/cloudformation/network/top.json --parameters ParameterKey=CloudToolsBucket,ParameterValue=extend_cfn_example_{yourName} ParameterKey=PrivateDomain,ParameterValue=example.internal ParameterKey=InternalHostedZone,ParameterValue={YourInternalHostedZoneId} --capabilities CAPABILITY_IAM
```

Wait for the CloudFormation stack to complete and then check in on the internal hosted zone, it should be associated with the new VPC. This concludes the demonstration. Next we will talk about what when into the code and how the code interacts with CloudFormation and vise versa. 
