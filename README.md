# Spotify Streaming Analytics System

This project is a real-time streaming analytics system for Spotify data. It processes streaming data, aggregates insights, and provides a dashboard for visualizing top songs and artists.

## Project Structure

```
/home/hdoop/music-system/
├── api.py                     # Flask API for serving aggregated data
├── dashboard.html             # Frontend dashboard for visualizing analytics
├── data_ingestion_script.py   # Kafka producer for streaming Spotify data
├── spotify_history.csv        # Sample Spotify streaming history data
├── streaming_job.py           # PySpark job for real-time data processing
└── readme.md                  # Project documentation
```

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

## Setup Instructions

### Prerequisites
- Python 3.8+
- Apache Kafka
- Apache Spark
- MongoDB
- Node.js (for serving the dashboard, optional)

### Steps

1. **Install Dependencies**
     ```bash
     pip install flask flask-cors pymongo kafka-python pandas pyspark
     ```

2. **Start Kafka and MongoDB**
     - Start Kafka broker and create a topic named `spotify_streams`.
     - Start MongoDB server.

3. **Run Data Ingestion**
     ```bash
     python data_ingestion_script.py
     ```

4. **Run Streaming Job**
     ```bash
     python streaming_job.py
     ```

5. **Start API**
     ```bash
     python api.py
     ```

6. **Open Dashboard**
     - Open `dashboard.html` in a browser to view real-time analytics.

## File Details

### `spotify_history.csv`
- Sample Spotify streaming history data used for testing.

### `data_ingestion_script.py`
- Streams data from the CSV file to Kafka.

### `streaming_job.py`
- Processes Kafka streams and writes aggregated results to MongoDB.

### `api.py`
- Serves aggregated data via RESTful endpoints.

### `dashboard.html`
- Visualizes the analytics using D3.js.

## Example Usage

- **Top Songs API**: `http://localhost:5000/api/top-songs`
- **Top Artists API**: `http://localhost:5000/api/top-artists`

## Future Enhancements
- Add user authentication for the dashboard.
- Support additional analytics (e.g., most skipped songs).
- Deploy on a distributed cluster for scalability.

## License
This project is licensed under the MIT License.
## Detailed Steps

### 1. Start Zookeeper
Start the Zookeeper service, which is required for Kafka to function:
```bash
zookeeper-server-start.sh config/zookeeper.properties
```

### 2. Start Kafka
Start the Kafka broker:
```bash
kafka-server-start.sh config/server.properties
```

### 3. Create the Kafka Topic
Create the `spotify_streams` topic for streaming data:
```bash
kafka-topics.sh --create --topic spotify_streams --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
```

### 4. Start MongoDB
Start the MongoDB service:
```bash
mongod --dbpath /path/to/your/mongodb/data
```

### 5. Run the Data Ingestion Script
Simulate real-time data streaming by running the Kafka producer:
```bash
python data_ingestion_script.py
```

### 6. Run the Spark Streaming Job
Process the streaming data and store aggregated results in MongoDB:
### Running on Hadoop and Spark

#### 1. Start Hadoop Services
Before running the Spark job, ensure that Hadoop services are up and running:
```bash
### 1. Start HDFS Services
Before running the Spark job, ensure that HDFS services are up and running. Start the NameNode and DataNode services:
```bash
start-dfs.sh
```

Verify that the HDFS services are running:
```bash
jps
```
You should see `NameNode` and `DataNode` in the output.

### 2. Create HDFS Directories
Create necessary directories in HDFS for storing Spark job outputs and checkpoints:
```bash
hdfs dfs -mkdir -p /user/hadoop/checkpoints
hdfs dfs -mkdir -p /user/hadoop/output
```

Verify the directories:
```bash
hdfs dfs -ls /user/hadoop
```

Verify the HDFS setup:
```bash
hdfs dfs -ls /user/hadoop/checkpoints
```

#### 3. Run the Spark Job

##### Local Mode
Run the Spark job locally for testing:
```bash
spark-submit \
    --master local[*] \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 \
    streaming_job.py
```

##### Cluster Mode
Run the Spark job on a Hadoop YARN cluster for production:
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

#### 4. Monitor the Job
Use the Hadoop ResourceManager UI to monitor the job:
```
http://<resource-manager-host>:8088
```

### 7. Start the Flask API
Serve the aggregated data through the REST API:
```bash
python api.py
```

### 8. Start the Dashboard
Start a local HTTP server to serve the dashboard:
```bash
python -m http.server 8000
```
Open the dashboard in your browser:
```
http://localhost:8000/dashboard.html
```

## How It Works

### Data Ingestion
The `data_ingestion_script.py` reads data from `spotify_history.csv` and streams it to the Kafka topic `spotify_streams`.

### Stream Processing
The `streaming_job.py` Spark job reads data from Kafka, processes it, and writes aggregated results (e.g., top songs and artists) to MongoDB.

### API
The `api.py` Flask application provides REST endpoints to fetch aggregated data:
- `/api/top-songs`: Returns the top played songs.
- `/api/top-artists`: Returns the top played artists.

### Dashboard
The `dashboard.html` visualizes the data using D3.js and updates every 10 seconds by fetching data from the Flask API.

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
