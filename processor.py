import openai
import base64
from pathlib import Path
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request
import re
import json
import requests

load_dotenv()

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

def encode_image_to_base64(image_path):
    image_data = Path(image_path).read_bytes()
    return base64.b64encode(image_data).decode('utf-8')

def get_architecture_prompt():
    return """
You are a cloud infrastructure assistant.

You will be shown an image of a system architecture diagram. Your task is to identify each component and determine which Google Cloud Platform (GCP) or Firebase service should be used to host or implement it.

Output a JSON array where each item is an object with this structure:
{
  "id": <Enumerated integer starting from 1>
  "service": "<GCP or Firebase service>",
  "hosts": "<Component name from the diagram>",
  "description": "<A one-line explanation of the role this service plays in the architecture>",
  "interacts_with": "<List of other services/components it communicates with>"
}
Important instructions:

The output JSON array must list services in the order they should be created in a real-world deployment. For example, databases and storage should appear before services like Cloud Run that depend on them.

Carefully analyze the deployment strategy and determine which components should be provisioned first to support dependent services.

Use only GCP and Firebase services. Follow these mapping rules:

- If the component is a web server, backend, or API: use "Cloud Run".
- If it’s a static frontend (e.g., web client): use "Firebase Hosting".
- If it's a real-time syncing database: use "Firebase Realtime Database".
- If it's a document-style NoSQL DB: use "Firestore".
- If it's a relational database (PostgreSQL, MySQL): use "Cloud SQL".
- If it refers to a cache or Redis: use "MemoryStore".
- If it is a storage bucket, file server, or media storage: use "Cloud Storage".
- If it's a queue or task processor: use "Cloud Tasks".
- If it's an event system or pub/sub messaging layer: use "Pub/Sub".
- If it mentions login, signup, or authentication: use "Firebase Authentication".
- If it runs scheduled jobs, or serverless code snippets: use "Cloud Functions".
- If it performs machine learning or AI inference: use "Vertex AI".
- If it’s a monitoring or logging component: use "Cloud Logging" or "Cloud Monitoring".
- Only include services that are required for deployment.
- Do not make up service names. Only use real GCP or Firebase services.

Return only the JSON array. Do not include any explanation or commentary.
Return only the final JSON array as raw JSON (not in a code block), without any explanation or formatting.
Begin analysis.
""".strip()


def analyze_architecture_image(image_path):    
    response = requests.get(image_path)
    image_bytes = response.content
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in analyzing architecture diagrams and mapping them to GCP and Firebase services."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": get_architecture_prompt()},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }}
                ]
            }
        ],
        temperature=0.2
    )
    return response.choices[0].message.content
