#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import random
import time
import os

import boto3

random.seed(47)

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
KINESIS_STREAM_NAME = os.getenv('KINESIS_STREAM_NAME', 'csv-word-count-streams')

kinesis = boto3.client('kinesis', region_name=AWS_REGION_NAME)

#pylint: disable=C0301
SENTENCES = [
'''Amazon Kinesis Data Analytics is the easiest way to analyze streaming data, gain actionable insights, and respond to your business and customer needs in real time.''',
'''Amazon Kinesis Data Analytics reduces the complexity of building, managing, and integrating streaming applications with other AWS services.''',
'''SQL users can easily query streaming data or build entire streaming applications using templates and an interactive SQL editor.''',
'''Java developers can quickly build sophisticated streaming applications using open source Java libraries and AWS integrations to transform and analyze data in real-time.''',
'''Amazon Kinesis Data Analytics takes care of everything required to run your real-time applications continuously and scales automatically to match the volume and throughput of your incoming data.''',
'''With Amazon Kinesis Data Analytics, you only pay for the resources your streaming applications consume.''',
'''There is no minimum fee or setup cost.''',
'''Amazon Kinesis Data Analytics provides built-in functions to filter, aggregate, and transform streaming data for advanced analytics.''',
'''It processes streaming data with sub-second latencies, enabling you to analyze and respond to incoming data and streaming events in real time.''',
'''Amazon Kinesis Data Analytics is serverless; there are no servers to manage.''',
'''It runs your streaming applications without requiring you to provision or manage any infrastructure.''',
'''Amazon Kinesis Data Analytics automatically scales the infrastructure up and down as required to run your applications with low latency.''',
'''With Amazon Kinesis Data Analytics, you pay only for the processing resources that your streaming applications use. There are no minimum fees or upfront commitments.'''
]

while True:
  idx = random.choice([e for e in range(len(SENTENCES))]) #pylint: disable=R1721
  words = ['{},1'.format(e.strip().lower()) for e in SENTENCES[idx].replace(',', ' ').split() if e.strip()]
  records = []
  for wc in words:
    partition_key = 'pk-{:05}'.format(random.randint(1, 1024)) #pylint: disable=C0103
    records.append({'Data': wc, 'PartitionKey': partition_key})
  print('\n'.join(words))

  res = kinesis.put_records(Records=records, StreamName=KINESIS_STREAM_NAME)
  print('\nOK\n' if res['ResponseMetadata']['HTTPStatusCode'] == 200 else '\nFailed\n')

  n = float('{:.2}'.format(random.random()))
  time.sleep(n)
