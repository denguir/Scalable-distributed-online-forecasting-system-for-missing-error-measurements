# Scalable distributed online forecastingsystem for missing error measurements

## Folder structure

```
├── data
│   ├── data.conv.txt.gz
│   └── mote_locs.txt
├── docker
│   ├── hdfs
│   │   ├── docker-compose.yml
│   │   └── hadoop.env
│   ├── kafka
│   │   └── docker-compose.yml
│   ├── serve
│   │   ├── data-serving
│   │   │   ├── hbase-site.xml
│   │   │   ├── opentsdb.conf
│   │   │   └── rollup_config.json
│   │   ├── docker-compose.yml
│   │   ├── grafana-storage
│   │   │   ├── grafana.db
│   │   │   ├── plugins
│   │   │   └── png [error opening dir]
│   │   └── opentsdb-docker
│   │       ├── docker-compose.yml
│   │       ├── Dockerfile
│   │       ├── files
│   │       │   ├── create_table.sh
│   │       │   ├── create_tsdb_tables.sh
│   │       │   ├── entrypoint.sh
│   │       │   ├── hbase-site.xml
│   │       │   ├── opentsdb.conf
│   │       │   ├── start_hbase.sh
│   │       │   └── start_opentsdb.sh
│   │       ├── LICENSE
│   │       └── README.md
│   └── spark
│       ├── docker-compose-aws.yml
│       ├── docker-compose-test.yml
│       ├── docker-compose.yml
│       └── stream-data-processing
│           ├── Dockerfile
│           ├── jupyter_notebook_config.py
│           ├── spark-env.sh
│           └── start-spark
├── docs
│   └── Assignment.pdf
├── notebooks
│   ├── fairscheduler-statedump.log
│   ├── KafkaSparkStreamingPersistence
│   │   ├── KafkaReceivePersistence.ipynb
│   │   └── KafkaSendPersistence.ipynb
│   ├── KafkaSparkStreamingRLS
│   │   ├── KafkaReceiveRLS.ipynb
│   │   └── KafkaSendRLS.ipynb
│   └── Work.ipynb
└── README.md
```
## Data creation
before running the scripts, create the data directory in scripts:
mkdir scripts/data

## Architecture

### Apache Kafka

- 3 Zoookeper nodes
- 3 Kafka Brockers

### Apache Spark

- 1 Master node
- 2 Workers
    - Each with 4 cores and 4Gb of RAM

### OpenTSDB

- HDFS cluster with 1 name-node and 3 data-nodes
- HBase

### Grafana

- 1 Dashboard  
`note`: the Grafana's storage will not be stored in the repository

## How to deploy

1. Deploy Kafka cluster service:
    ```bash
    cd docker/kafka
    docker-compose up -d
    ```
2. Deploy HDFS cluster service:
    ```bash
    cd docker/hdfs
    docker-compose up -d
    ```
    `note`: not necessary when deploying it locally for testing purposes.
3. Deploy Spark cluster:
    ```bash
    cd docker/spark
    docker-compose up -f docker-compose-aws.yml -d # if deploying it in a server
    docker-compose up -d # if deploying for testing with HDFS
    docker-compose -f docker-compose-test.yml up -d # ... without hdfs   
    ```
    `note`: After run the Spark Cluster a Jupyter notebook is then available in http://[IP]:8888 whose `password` is "**secret**". The folder `notebooks` will synchronize its content with a `notebooks` folder in the master node, so any work you want to save, should be placed in the `noteboks` folder.
4. Deploy OpenTSDB + Grafana:
    ```bash
    cd docker/serve
    docker-compose up -d
    ```
    `note`: You can access the openTSDB web ui in http://[IP]:4242 and the Grafana Dashboard in http://[IP]:3000. The user and `password` for the Dashboard are "**admin**", "**admin**".