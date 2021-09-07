# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from airflow.plugins_manager import AirflowPlugin
from operators.hello_mwaa_operator import HelloOperator
                    
class mwaa_plugins(AirflowPlugin):
    name = 'mwaa_plugins'
    operators = [HelloOperator]
