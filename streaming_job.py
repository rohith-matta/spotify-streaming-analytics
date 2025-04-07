import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, LongType, BooleanType
import json
from pymongo import MongoClient

# Get the master argument from the command line (default to 'local[*]')
master = "local[*]"  # Default to local mode
if len(sys.argv) > 1:
    master = sys.argv[1]  # Use the first argument as the master (e.g., 'yarn')

# Create Spark Session
spark = SparkSession.builder \
    .appName("SpotifyStreamingAnalysis") \
    .master(master) \
    .config("spark.executor.memory", "1G") \
    .config("spark.executor.cores", "1") \
    .config("spark.driver.memory", "1G") \
    .config("spark.sql.shuffle.partitions", "10") \
    .getOrCreate()

# Define schema for the Spotify dataset
schema = StructType([
    StructField("spotify_track_uri", StringType(), True),
    StructField("track_name", StringType(), True),
    StructField("artist_name", StringType(), True),
    StructField("album_name", StringType(), True),
    StructField("ts", LongType(), True),
    StructField("platform", StringType(), True),
    StructField("ms_played", LongType(), True),
    StructField("reason_start", StringType(), True),
    StructField("reason_end", StringType(), True),
    StructField("shuffle", BooleanType(), True),
    StructField("skipped", BooleanType(), True)
])

# Read streaming data from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "spotify_streams") \
    .option("startingOffsets", "earliest") \
    .option("maxOffsetsPerTrigger", "100") \
    .load()

# Parse the JSON messages
parsed_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("data"))
data_df = parsed_df.select("data.*")

# Convert epoch seconds to timestamp for window operations
data_df = data_df.withColumn("eventTime", to_timestamp(col("ts")))

# Aggregation for top played songs (group by track_name)
aggregated_songs = data_df \
    .withWatermark("eventTime", "10 minutes") \
    .groupBy(window(col("eventTime"), "5 minutes", "2 minutes"), col("track_name")) \
    .count()

# Aggregation for top played artists (group by artist_name)
aggregated_artists = data_df \
    .withWatermark("eventTime", "10 minutes") \
    .groupBy(window(col("eventTime"), "5 minutes", "2 minutes"), col("artist_name")) \
    .count()

# Function to write each micro-batch to MongoDB into a given collection
def write_to_mongo(collection_name):
    def writer(batch_df, batch_id):
        try:
            print(f"Processing batch {batch_id} with {batch_df.count()} records for {collection_name}.")
            records = batch_df.toJSON().map(lambda j: json.loads(j)).collect()
            if records:
                client = MongoClient("mongodb://localhost:27017/")
                db = client["music_streaming"]
                collection = db[collection_name]
                collection.insert_many(records)
                client.close()
                print(f"Batch {batch_id} written to MongoDB collection {collection_name} with {len(records)} records.")
        except Exception as e:
            print(f"Error writing batch {batch_id} to MongoDB: {e}")
    return writer

# Write aggregated results to MongoDB collections
query_songs = aggregated_songs.writeStream \
    .outputMode("update") \
    .option("checkpointLocation", "hdfs://localhost:9000/user/hdoop/checkpoints/spotify_streaming_songs") \
    .foreachBatch(write_to_mongo("aggregated_results_songs")) \
    .start()

query_artists = aggregated_artists.writeStream \
    .outputMode("update") \
    .option("checkpointLocation", "hdfs://localhost:9000/user/hdoop/checkpoints/spotify_streaming_artists") \
    .foreachBatch(write_to_mongo("aggregated_results_artists")) \
    .start()

query_songs.awaitTermination()
query_artists.awaitTermination()
