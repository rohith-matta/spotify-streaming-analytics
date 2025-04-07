import json
import time
import pandas as pd
from kafka import KafkaProducer
from datetime import datetime

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Load the Spotify Streaming History CSV file
df = pd.read_csv('spotify_history.csv')

# Optional: Convert the 'ts' column to epoch seconds if it’s in a date format.
# Here we assume 'ts' is a datetime string; adjust based on your CSV format.
df['ts'] = pd.to_datetime(df['ts']).astype(int) // 10**9

# Stream the data in sequential order by iterating over each row.
# A delay is added to simulate real-time streaming.
for index, row in df.iterrows():
    event_data = {
        "spotify_track_uri": row["spotify_track_uri"],
        "track_name": row["track_name"],
        "artist_name": row["artist_name"],
        "album_name": row["album_name"],
        "ts": row["ts"],
        "platform": row["platform"],
        "ms_played": row["ms_played"],
        "reason_start": row["reason_start"],
        "reason_end": row["reason_end"],
        "shuffle": row["shuffle"],
        "skipped": row["skipped"]
    }
    # Send the event to the 'spotify_streams' Kafka topic
    producer.send("spotify_streams", event_data)
    print(f"Sent: {event_data}")
    
    # Introduce a delay to simulate real-time data streaming (adjust as needed)
    time.sleep(1)

# Ensure all messages are sent and close the producer
producer.flush()
producer.close()
