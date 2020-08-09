#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import json
import random
import datetime
import time
import os

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
KINESIS_STREAM_NAME = os.getenv('KINESIS_STREAM_NAME', 'stocks-streams')

kinesis = boto3.client('kinesis', region_name=AWS_REGION_NAME)

def get_referrer():
  data = {}
  now = datetime.datetime.now()
  str_now = now.isoformat()
  data['EVENT_TIME'] = str_now
  data['TICKER'] = random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV'])
  price = random.random() * 100
  data['PRICE'] = round(price, 2)
  return data

while True:
  stock_info = get_referrer()
  json_data = json.dumps(stock_info['TICKER'])
  print(json_data)

  kinesis.put_record(
    StreamName=KINESIS_STREAM_NAME,
    Data=json_data,
    PartitionKey="partitionkey")

  n = float('{:.2}'.format(random.random()))
  time.sleep(n)
