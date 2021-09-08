# About Automating DAG deployment

This repository provides general guidelines for automating the deployment of your DAG to Amazon MWAA environment so that You can build quality DAGs and deploy them faster.

## What this repo contains

```
├── build
│   ├── buildspec.yaml           ## Run by AWS CodeBuild
│   ├── local-runner.py          ## Runs local runner and executes test
│   └── plugin-versioning.py     ## Copies plugins.zip/requirement.txt to S3 
│                                   updates versionId in param file
├── dags
│   ├── hello-mwaa.py            ## sample dag
│   └── requirements.txt         ## Additional Python dependancies
├── infra
│   ├── parameters               ## parameters for MWAA stack. one for each ENV
│   ├── pipeline.yaml            ## IaC for pipeline
│   └── template.yaml            ## IaC for MWAA env
├── plugins                      ## Plugins
    ├──.....    
└── test                      
    ├── __init__.py
    ├── dag-validation.py        ## DAG integrity test
    └── dags                     ## DAG Unit test
```
## Getting started
### Prerequisites

- Create S3 bucket for storing DAGS. [Here](https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-s3-bucket.html) is the doc on creating S3 bucket for MWAA


- Build [MWAA local runner](https://github.com/aws/aws-mwaa-local-runner) and push to ECR repo. Follow the instructions in MWAA local runner repo to build the image for version 2.0.2 of the MWAA. You will get an image ID after you build and use the image id to tag the image. Following are the commands to push the image to your ECR repo. if you are not using ECR, you will have to change the registry info in build/local-runner.py. 

```bash
aws ecr get-login-password --region {region}  | docker login --username AWS --password-stdin {account}.dkr.ecr.{region}.amazonaws.com/{repo}

aws ecr create-repository --repository-name {repo} --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true

docker tag {imageid} {account}.dkr.ecr.{region}.amazonaws.com/{repo}:2.0.2
docker push {account}.dkr.ecr.{region}.amazonaws.com/{repo}:2.0.2

```


- Create an AWS CodeStar connection for connecting to your GitHub repo

```bash
aws codestar-connections create-connection --provider-type GitHub --connection-name MWAA-GitHub-connection.
```
Note down the ARN. This will be used in the command later for creating the pipeline.
After creating the connection, Follow the instructions [here](https://docs.aws.amazon.com/dtconsole/latest/userguide/connections-update.html) to update the pending connection.


### Create your Repo

 Clone the repo. Create your own data pipeline repo as the folder structure mentioned before. Copy the infra and build  directory to your source code and commit your source code to a GitHub repo.

### Modify parameters
 infra/parameters/{ENV}.json - update the S3 bucket with the bucket name created in the prerequisite step. Leave other parameters as such. Requirements and plugins version will be updated during build process

### Create the build pipeline

```bash
aws cloudformation create-stack --stack-name mwaa-cicd  --template-body file://infra/pipeline.yaml  --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM --parameters ParameterKey=CodeRepoName,ParameterValue={CodeRepoName} ParameterKey=MWAASourceBucket,ParameterValue={MWAASourceBucket} ParameterKey=GitHubAccountName,ParameterValue={GitHubAccountName} ParameterKey=CodeStarConnectionArn,ParameterValue={CodeStarConnectionArn}

```
see example below
``` bash
aws cloudformation update-stack --stack-name mwaa-cicd  --template-body file://infra/pipeline.yaml  --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM --parameters ParameterKey=CodeRepoURL,ParameterValue=test ParameterKey=MWAASourceBucket,ParameterValue=airflow2.0-us-west-2 ParameterKey=GitHubAccountName,ParameterValue=accountname ParameterKey=CodeStarConnectionArn,ParameterValue=arn:aws:cloudformation:us-west-2:1234567890:stack/mwaa-cicd/69afe8e0-1010-11ec-a7ec-0a0e9901ce6b
```

You can access the pipeline by accessing AWS Codepipeline console. You can start the pipeline from there or modify code and commit to your source code repo.



## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.

