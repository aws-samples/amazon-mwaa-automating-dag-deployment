# About Automating DAG deployment

This repository provides general guidelines for automating the deployment of your DAG to Amazon MWAA environment so that You can build quality DAGs and deploy them faster.

## What this repo contains

```
├── build
│   ├── buildspec.yaml           ## Run by AWS CodeBuild
│   ├── local-runner.py          ## Runs local runner and executes test
│   └── plugin-versioning.py     ## Copies plugins.zip/requirement.txt to S3 │                                   updates versionId in param file
├── dags
│   ├── hello-mwaa.py            ## sample dag
│   └── requirement.txt          ## Additional Python dependancies
├── infra
│   ├── parameters               ## parameter for MWAA stack. one for eac ENV
│   ├── pipeline.yaml             ## IaC for pipeline
│   └── template.yaml             ## IaC for MWAA env
├── plugins                      ## Plugins
    ├──.....    
└── test                      
    ├── __init__.py
    ├── dag-validation.py        ## DAG integrity test
    └── dags                     ## DAG Unit test
```

## Prerequisites

- Create S3 bucket for storing DAGS. [Here](https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-s3-bucket.html) is the doc on creating S3 bucket for MWAA


- Build [MWAA local runner](https://github.com/aws/aws-mwaa-local-runner) and push to ECR repo. The images are used in build/local-runner.py for testing the DAGs. You can change the repo name there.

```bash
aws ecr get-login-password --region {region}  | docker login --username AWS --password-stdin {account}.dkr.ecr.{region}.amazonaws.com/{repo}

aws ecr create-repository --repository-name {repo} --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true

docker tag {imageid} {account}.dkr.ecr.{region}.amazonaws.com/{repo}
docker push {account}.dkr.ecr.{region}.amazonaws.com/{repo}

```
- [Setup Github oAuth token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) in Secret Manager as MyGitHubToken[You can change the name in the infra/pipeline.yaml]. 

```bash
aws secretsmanager create-secret --name MyGitHubToken --description "Github oAuth Token" --secret-string "{\"token\": \"{MyGitHubToken}\"}"
```

## Get started

Clone the repo. Create your own data pipeline repo as the folder structure mentioned before. Copy the files in infra and build directory to your source code. Commit your source code to a Github repo.

### Modify parameters
- infra/parameters/{ENV}.json - update your S3 bucket 
- infra/pipeline.yaml - update your repository name/Github account and S3 bucket 

### Create the build pipeline

```bash
aws cloudformation create-stack --stack-name mwaa-cicd1  --template-body file://pipeline.yaml  --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM --parameters ParameterKey=CodeRepoURL,ParameterValue={CodeRepoURL} ParameterKey=MWAASourceBucket,ParameterValue={MWAASourceBucket} ParameterKey=GitHubAccountName,ParameterValue={GitHubAccountName}
```

You can access the pipeline by accessing AWS Codepipeline console. You can start the pipeline from there or modify code and commit to your source code repo.


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.

