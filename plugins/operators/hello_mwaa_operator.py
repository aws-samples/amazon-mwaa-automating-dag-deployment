# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from airflow.operators.bash import BaseOperator
from airflow.utils.decorators import apply_defaults


class HelloOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 my_field,
                 *args,
                 **kwargs):
        super(HelloOperator, self).__init__(*args, **kwargs)
        self.my_field = my_field

    def execute(self, context):
        message = "Hello! {}".format(self.my_field)
        print(message)
        return message
