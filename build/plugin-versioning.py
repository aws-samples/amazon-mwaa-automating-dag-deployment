#Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

import json
import boto3
from botocore.exceptions import ClientError
import sys


mwaaEnvName=sys.argv[1]
dagBucket=sys.argv[2]
configFile=sys.argv[3]
pluginsChanged=None
RequirementChanged=None

if(len(sys.argv) == 6):
    pluginsChanged=sys.argv[4]
    RequirementChanged=sys.argv[5]
if(len(sys.argv) == 5):
    fileChanged=sys.argv[4]
    if(fileChanged == 'dags/requirements.txt'):
        RequirementChanged=fileChanged
    else:
       pluginsChanged=fileChanged


pluginVersion=None
requirementFileVersion=None
s3 = boto3.client('s3')    

try:
    ssm = boto3.client('ssm')
    response = ssm.get_parameters(
        Names=[
            mwaaEnvName,
        ]
    )
    if(len(response['Parameters']) > 0 ):

        envName=response['Parameters'][0]['Value']

        response = boto3.client('mwaa').get_environment(
            Name=envName
        )

        if("Environment" in response): 
            pluginVersion=response["Environment"]["PluginsS3ObjectVersion"]
            requirementFileVersion=response["Environment"]["RequirementsS3ObjectVersion"]
    else:
        pluginsChanged='new'
        RequirementChanged='new'

except ClientError as e:
    print(e)


try:
    if(pluginsChanged != None or RequirementChanged != None):
        print(pluginsChanged)
        if(pluginsChanged != None):
            response = s3.put_object(
                Body=open('plugins/plugins.zip', 'rb') ,
                Bucket=dagBucket,
                Key='plugins/plugins.zip')
            pluginVersion=response['VersionId']
        if(RequirementChanged != None):
            response = s3.put_object(
                Body=open('dags/requirements.txt', 'rb') ,
                Bucket=dagBucket,
                Key='requirements.txt')
            requirementFileVersion=response['VersionId']
    if(pluginVersion == None):
        metadata=s3.head_object(
            Bucket=dagBucket,
            Key='plugins/plugins.zip')
        pluginVersion=metadata['VersionId']
    if(requirementFileVersion == None):
        metadata=s3.head_object(
            Bucket=dagBucket,
            Key='requirements.txt')
        requirementFileVersion=metadata['VersionId']

        
    f = open(configFile, "r")
    data = json.load(f)
    f.close()

    f = open(configFile, "w")
    data['Parameters']['RequirementsFileVersion']=requirementFileVersion
    data['Parameters']['PluginsVersion']=pluginVersion

    json.dump(data, f)
    f.close()
except ClientError as e:
    print(e)
    sys.exit(-1)
