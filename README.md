# Spotify Streaming Analytics System

This project is a real-time streaming analytics system for Spotify data. It processes streaming data, aggregates insights, and provides a dashboard for visualizing top songs and artists.

---

## Project Structure

```
/home/hdoop/music-system/
├── api.py                     # Flask API for serving aggregated data
├── dashboard.html             # Frontend dashboard for visualizing analytics
├── data_ingestion_script.py   # Kafka producer for streaming Spotify data
├── spotify_history.csv        # Sample Spotify streaming history data
├── streaming_job.py           # PySpark job for real-time data processing
└── README.md                  # Project documentation
```

---

## Components

### 1. **Data Ingestion**
- **Script**: `data_ingestion_script.py`
- **Description**: Reads Spotify streaming history from `spotify_history.csv` and streams it to a Kafka topic (`spotify_streams`) in real-time.
- **Technology**: Python, Kafka

### 2. **Real-Time Data Processing**
- **Script**: `streaming_job.py`
- **Description**: Processes streaming data from Kafka using PySpark, aggregates insights (e.g., top songs and artists), and writes results to MongoDB.
- **Technology**: PySpark, MongoDB, Kafka

### 3. **API**
- **Script**: `api.py`
- **Description**: Provides RESTful endpoints to fetch aggregated data from MongoDB.
     - `/api/top-songs`: Returns top played songs.
     - `/api/top-artists`: Returns top played artists.
- **Technology**: Flask, MongoDB

### 4. **Dashboard**
- **File**: `dashboard.html`
- **Description**: A web-based dashboard that visualizes top songs and artists using D3.js.
- **Technology**: HTML, CSS, JavaScript, D3.js

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Apache Kafka
- Apache Spark
- MongoDB
- Node.js (optional, for serving the dashboard)

### Steps

1. **Install Dependencies**
   ```bash
   pip install flask flask-cors pymongo kafka-python pandas pyspark
   ```

2. **Start Required Services**
   - Start Zookeeper and Kafka broker.
   - Start MongoDB server.

3. **Run the Project**
   - **Data Ingestion**: `python data_ingestion_script.py`
   - **Streaming Job**: `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 streaming_job.py`
   - **API**: `python api.py`
   - **Dashboard**: Open `dashboard.html` in a browser.

---

## Detailed Steps

### 1. Start Zookeeper and Kafka
Start Zookeeper:
```bash
zookeeper-server-start.sh config/zookeeper.properties
```

Start Kafka:
```bash
kafka-server-start.sh config/server.properties
```

Create the Kafka topic:
```bash
kafka-topics.sh --create --topic spotify_streams --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
```

### 2. Start MongoDB
Start the MongoDB service:
```bash
mongod --dbpath /path/to/your/mongodb/data
```

### Create the Required Database and Collections
Once MongoDB is running, create the database and collections used in the `streaming_job.py` script. Open the MongoDB shell:
```bash
mongosh
```

Run the following commands to create the database and collections:
```javascript
use music_streaming;
db.createCollection("aggregated_results_songs");
db.createCollection("aggregated_results_artists");
```

Verify the collections:
```javascript
show collections;
```

### 3. Run Data Ingestion
Simulate real-time data streaming:
```bash
python data_ingestion_script.py
```

### 4. Run the Spark Streaming Job
#### Start HDFS
Before running the Spark Streaming job, ensure that HDFS is running. Start the NameNode and DataNode services:

Start the NameNode:
```bash
hadoop-daemon.sh start namenode
```

Start the DataNode:
```bash
hadoop-daemon.sh start datanode
```

Verify that HDFS is running:
```bash
hdfs dfsadmin -report
```

#### Create Required Directories in HDFS
Create the directories in HDFS that are used for checkpointing in the Spark Streaming job:

```bash
hdfs dfs -mkdir -p /user/hdoop/checkpoints/spotify_streaming_songs
hdfs dfs -mkdir -p /user/hdoop/checkpoints/spotify_streaming_artists
```

Verify the directories:
```bash
hdfs dfs -ls /user/hdoop/checkpoints
```

#### Local Mode
Run the Spark Streaming job in local mode:
```bash
spark-submit \
     --master local[*] \
     --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 \
     streaming_job.py
```

#### Cluster Mode
Run the Spark Streaming job in cluster mode:
```bash
spark-submit \
     --master yarn \
     --deploy-mode cluster \
     --num-executors 1 \
     --executor-memory 1G \
     --executor-cores 1 \
     --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 \
     streaming_job.py
```

### 5. Start the Flask API
Serve the aggregated data:
```bash
python api.py
```

### 6. Start the Dashboard
Serve the dashboard locally:
```bash
python -m http.server 8000
```
Open in a browser:
```
http://localhost:8000/dashboard.html
```

---

## Example Usage

- **Top Songs API**: `http://localhost:5000/api/top-songs`
- **Top Artists API**: `http://localhost:5000/api/top-artists`

---

## Troubleshooting

### Kafka Not Running
Ensure Zookeeper and Kafka are running:
```bash
zookeeper-server-start.sh config/zookeeper.properties
kafka-server-start.sh config/server.properties
```

### MongoDB Connection Issues
Ensure MongoDB is running:
```bash
mongod --dbpath /path/to/your/mongodb/data
```

### Spark Job Fails
Ensure the Kafka package is included in the `spark-submit` command:
```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 streaming_job.py
```

### Dashboard Not Updating
Ensure the Flask API is running and accessible at `http://localhost:5000`.
## Acknowledgments
- Spotify for the inspiration.
- Open-source libraries and tools used in this project.
- D3.js for data visualization.
- Apache Kafka and Spark for real-time processing.
