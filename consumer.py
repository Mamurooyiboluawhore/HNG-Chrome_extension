import pika
import os

rabbitmq_host = 'localhost' 
rabbitmq_queue = 'video_chunks'
UPLOAD_FOLDER = 'uploads'

def save_video_chunk(chunk):
    try:
        # Save the video chunk to a file in the UPLOAD_FOLDER directory
        chunk_filename = os.path.join(UPLOAD_FOLDER, 'video_chunk.mp4')  # Adjust the filename as needed
        with open(chunk_filename, 'ab') as chunk_file:
            chunk_file.write(chunk)
        print(f"Saved video chunk: {len(chunk)} bytes")
    except Exception as e:
        print(f"Error saving video chunk: {str(e)}")

def consume_video_chunks(ch, method, properties, body):
    try:
        # This function is called when a message is consumed from the queue
        # You can process the 'body' here, which contains the video chunk
        save_video_chunk(body)
    except Exception as e:
        print(f"Error processing video chunk: {str(e)}")

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Declare the queue (make sure it matches the one you use for sending)
channel.queue_declare(queue=rabbitmq_queue)

# Set up a consumer to handle incoming messages
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=consume_video_chunks, auto_ack=True)

print("Consumer started. Waiting for messages...")

# Start consuming messages
channel.start_consuming()
