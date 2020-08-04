
### Kinesis Streams Consumer
- kinesis data streams 에서 실시간으로 데이터를 읽어오는 CLI(Command-line Instruction)

```
$ python src/main/python/consumer/kinesis_consumer.py --help
usage: kinesis_consumer.py [-h] [--stream-name STREAM_NAME]
                           [--iter-type {TRIM_HORIZON,LATEST}]
                           [--region-name REGION_NAME]

optional arguments:
  -h, --help            show this help message and exit
  --stream-name STREAM_NAME
                        kinesis stream-name
  --iter-type {TRIM_HORIZON,LATEST}
                        kinesis stream shard iterator type: [TRIM_HORIZON,
                        LATEST]
  --region-name REGION_NAME
                        aws region name (default: us-east-1)
```
