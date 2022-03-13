# PyBuilder Example - Producer/Consumer for Kinesis Data Streams

### Description
- kinesis data streams 관련 CLI(Command-line Instruction) code snippets

### Kinesis Streams Consumer
- kinesis data streams 에서 실시간으로 데이터를 읽어오는 CLI

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

### Kinesis Streams Producers
- kinesis data streams 에서 실시간으로 데이터를 넣는 CLI


|  Name | Description  | 
| ------------- |:-------------:| 
| sentences | 임의의 문장 생성 |
| words | 임의의 단어와 발생 횟수(1) 튜플 생성 (예: ("hello", 1) | 
| stocks | 임의의 주식 정보 생성 | 

예를 들어, 임의의 문장을 생성해서 Kinesis Data Streams에 넣으려면, 
다음과 같이 `AWS_REGION_NAME` 과 `KINESIS_STREAM_NAME` 환경 변수를 설정하고,
`sentences.py` 스크립트를 실행한다.

```shell script
$ export AWS_REGION_NAME='us-east-1'
$ export KINESIS_STREAM_NAME='sentences-streams'
$ python sentences.py
```

### Build & Deploy
- [PyBuilder](https://pybuilder.io/)를 이용해서 전체 코드 조각들을 mono repository로 관리

#### Useful PyBuilder commands
- `pyb -t`: 전체 작업 목록을 표시한다.
- `pyb checkstyle`: [pylint](https://www.pylint.org/)를 이용해서 code style을 검사한다.
- `pyb package`: 배포한 소스 코드나 resources, script 파일들을 배포 준비 디렉터리(target)에 패키징한다.
- `pyb publish`: 패키징된 소스 코드와 resources, script 파일들을 배포한다.
- `pyb clean`: 배포 준비 디렉터리(target)의 파일들을 삭제한다.

`git clone` 명령어를 실행해서 소스 코드를 다운로드 한 후에, 아래와 같이 python virtualenv 환경을 생성하고,
필요한 python 패키지를 설치한다.

```shell script
$ python3 -m venv kinesis-streams-samples
$ source bin/activate
$ pip install - requirements.txt
```

전체 작업(Task)을 `pyb -t` 또는 `pyb --list-tasks` 를 이용해서 확인 할 수 있다.

```shell script
$ pyb -t
Tasks found for project "kinesis-streams-samples":
                         analyze - <no description available>
                      checkstyle - check code style using pylint
                                   depends on tasks: prepare
                           clean - Cleans the generated output.
                 compile_sources - Compiles source files that need compilation.
                                   depends on tasks: prepare
                         install - Installs the published project.
                                   depends on tasks: package publish(optional)
      install_build_dependencies - Installs all build dependencies specified in the build descriptor
                                   depends on tasks: prepare
            install_dependencies - Installs all (both runtime and build) dependencies specified in the build descriptor
                                   depends on tasks: prepare
    install_runtime_dependencies - Installs all runtime dependencies specified in the build descriptor
                                   depends on tasks: prepare
                kinesis_consumer - kinesis data streams consumer
               kinesis_producers - kinesis data streams producers
         kinesis_stocks_producer - kinesis data streams producer: stocks
               list_dependencies - Displays all dependencies the project requires
                         package - Packages the application. Package a python application.
                                   depends on tasks: compile_sources run_unit_tests(optional)
                         prepare - Prepares the project for building. Creates target VEnvs
               print_module_path - Print the module path.
              print_scripts_path - Print the script path.
                         publish - Publishes the project.
                                   depends on tasks: package verify(optional)
           run_integration_tests - Runs integration tests on the packaged application.
                                   depends on tasks: package
                  run_unit_tests - Runs all unit tests.
                                   depends on tasks: compile_sources
                          verify - Verifies the project and possibly integration tests.
                                   depends on tasks: run_integration_tests(optional)
```

`pyb checkstyle`로 [pylint](https://www.pylint.org/)를 이용해서 소스 코드의 coding style을 검사할 수 있다. 

```shell script
$ pyb kinesis_consumer checkstyle
PyBuilder version 0.12.7
Build started at 2020-08-13 01:45:14
------------------------------------------------------------
[INFO]  Building kinesis-streams-samples version 1.0.dev0
[INFO]  Executing build in kinesis-streams-samples
[INFO]  Going to execute tasks: kinesis_consumer, checkstyle
[INFO]  Creating target 'build' VEnv in 'kinesis-streams-samples/target/venv/build/cpython-3.6.9.final.0'
[INFO]  Processing dependency packages 'pylint~=2.5.0' to be installed with {'upgrade': True}
[INFO]  Creating target 'test' VEnv in 'kinesis-streams-samples/target/venv/test/cpython-3.6.9.final.0'
[INFO]  Executing pylint on project sources.
[WARN]
--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)


[INFO]  Pass (score=10.00, cutoff=8.50)
------------------------------------------------------------
BUILD SUCCESSFUL
------------------------------------------------------------
Build Summary
             Project: kinesis-streams-samples
             Version: 1.0.dev0
      Base directory: kinesis-streams-samples
        Environments:
               Tasks: kinesis_consumer [0 ms] prepare [5026 ms] checkstyle [856 ms]
Build finished at 2020-08-13 01:45:23
Build took 8 seconds (8941 ms)
```

배포할 소스 코드 및 Resources, Script 등을 `pyb package` 를 이용해서 배포 준비 디렉터리(target)에 패키징 할 수 있다.

```shell script
$ pyb kinesis_consumer package
PyBuilder version 0.12.7
Build started at 2020-08-13 01:25:19
------------------------------------------------------------
[INFO]  Building kinesis-streams-samples version 1.0.dev0
[INFO]  Executing build in kinesis-streams-samples
[INFO]  Going to execute tasks: kinesis_consumer, package
[INFO]  Creating target 'build' VEnv in 'kinesis-streams-samples/target/venv/build/cpython-3.6.9.final.0'
[INFO]  Processing dependency packages 'pylint~=2.5.0' to be installed with {'upgrade': True}
[INFO]  Creating target 'test' VEnv in 'kinesis-streams-samples/target/venv/test/cpython-3.6.9.final.0'
[INFO]  Building distribution in kinesis-streams-samples/target/dist/kinesis-streams-consumer
[INFO]  Copying scripts to kinesis-streams-samples/target/dist/kinesis-streams-consumer
------------------------------------------------------------
BUILD SUCCESSFUL
------------------------------------------------------------
Build Summary
             Project: kinesis-streams-samples
             Version: 1.0.dev0
      Base directory: kinesis-streams-samples
        Environments:
               Tasks: kinesis_consumer [0 ms] prepare [5026 ms] compile_sources [0 ms] run_unit_tests [0 ms] package [0 ms]
Build finished at 2020-08-13 01:25:27
Build took 8 seconds (8084 ms)
```

배포할 소스 코드 및 Resources, Script 등을 패키징해서 `pyb publish`로 배포할 수 있다.

```shell script
$ pyb kinesis_consumer publish
PyBuilder version 0.12.7
Build started at 2020-08-13 01:33:55
------------------------------------------------------------
[INFO]  Building kinesis-streams-samples version 1.0.dev0
[INFO]  Executing build in kinesis-streams-samples
[INFO]  Going to execute tasks: kinesis_consumer, publish
[INFO]  Creating target 'build' VEnv in 'kinesis-streams-samples/target/venv/build/cpython-3.6.9.final.0'
[INFO]  Processing dependency packages 'pylint~=2.5.0' to be installed with {'upgrade': True}
[INFO]  Creating target 'test' VEnv in 'kinesis-streams-samples/target/venv/test/cpython-3.6.9.final.0'
[INFO]  Building distribution in kinesis-streams-samples/target/dist/kinesis-streams-consumer
[INFO]  Copying scripts to kinesis-streams-samples/target/dist/kinesis-streams-consumer
------------------------------------------------------------
BUILD SUCCESSFUL
------------------------------------------------------------
Build Summary
             Project: kinesis-streams-samples
             Version: 1.0.dev0
      Base directory: kinesis-streams-samples
        Environments:
               Tasks: kinesis_consumer [0 ms] prepare [5863 ms] compile_sources [0 ms] run_unit_tests [0 ms] package [0 ms] run_integration_tests [0 ms] verify [0 ms] publish [0 ms]
Build finished at 2020-08-13 01:34:04
Build took 8 seconds (8921 ms)
```

모든 배포 관련 작업이 완료되면, `pyb clean` 을 이용해서 배포 준비 디렉터리(target)의 내용을 삭제할 수 있다.

```shell script
$ pyb clean
PyBuilder version 0.12.7
Build started at 2020-08-13 01:27:36
------------------------------------------------------------
[INFO]  Building kinesis-streams-samples version 1.0.dev0
[INFO]  Executing build in kinesis-streams-samples
[INFO]  Going to execute task clean
[INFO]  Removing target directory kinesis-streams-samples/target
------------------------------------------------------------
BUILD SUCCESSFUL
------------------------------------------------------------
Build Summary
             Project: kinesis-streams-samples
             Version: 1.0.dev0
      Base directory: kinesis-streams-samples
        Environments:
               Tasks: clean [49 ms]
Build finished at 2020-08-13 01:27:39
Build took 3 seconds (3139 ms)
```
