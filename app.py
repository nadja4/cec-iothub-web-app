import os
from flask import Flask, render_template
from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask constructor 
app = Flask(__name__)

# Get connection string from environment variables
connection_string = os.environ["COSMOS_DB_CONNECTION_STRING"]

# Initialize Cosmos client using the connection string
client = CosmosClient.from_connection_string(connection_string)

database_string = os.environ['COSMOS_DB_DATABASE']
container_string = os.environ['COSMOS_DB_CONTAINER']

database = client.get_database_client(database_string)
container = database.get_container_client(container_string)

# Function to fetch data from Cosmos DB
def fetch_data_from_cosmos():
    query = 'SELECT * FROM c'
    items = list(container.query_items(query, enable_cross_partition_query=True))
    labels = [item['time'] for item in items]
    rel_humidity = [item['relative humidity'] for item in items]
    return labels, rel_humidity

# Root endpoint 
@app.route('/')
def homepage():
    labels, rel_humidity = fetch_data_from_cosmos()
    return render_template(
        template_name_or_list='index.html',
        rel_humidity=rel_humidity,
        labels=labels,
    )

# Main Driver Function 
if __name__ == '__main__':
    # Run the application on the local development server
    app.run(debug=True)