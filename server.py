from fastapi import FastAPI, Request
from processor import analyze_architecture_image
from command_engine import Session
import json

app = FastAPI()

@app.post("/analyze")
async def analyze_diagram(r: Request):
    data = await r.json()
    url = data['url']
    result = analyze_architecture_image(url)
    # json_like = re.search(r'\[\s*{.*?}\s*\]', result, re.DOTALL)
    # if json_like:
    #     try:
    #         parsed = json.loads(json_like.group())
    #         res = json.dumps(parsed, indent=2)
    #         return res
    #     except json.JSONDecodeError as e:
    #         print("JSON parsing error:", e)
    # else:
    #     print("No JSON structure found.")
    res = json.loads(result)
    return res
"""
[
    {
        "id": 1,
        "service": "Cloud Run",
        "hosts": "Template Engine",
        "description": "Runs HTTP server and makes API calls to AI services.",
        "interacts_with": [
            "Tasks",
            "Server"
        ]
    },
    {
        "id": 2,
        "service": "Cloud Tasks",
        "hosts": "Tasks",
        "description": "Handles task queuing for the template engine.",
        "interacts_with": [
            "Template Engine",
            "Server"
        ]
    },
    {
        "id": 3,
        "service": "Cloud Run",
        "hosts": "Server",
        "description": "Stores data and communicates with other components.",
        "interacts_with": [
            "Template Engine",
            "Tasks",
            "Realtime Database",
            "Database Postgres",
            "Storage bucket",
            "Frontend Client"
        ]
    },
    {
        "id": 4,
        "service": "Firebase Realtime Database",
        "hosts": "Realtime Database",
        "description": "Provides real-time data syncing.",
        "interacts_with": [
            "Server",
            "Frontend Client"
        ]
    },
    {
        "id": 5,
        "service": "Cloud SQL",
        "hosts": "Database Postgres",
        "description": "Stores relational data.",
        "interacts_with": [
            "Server"
        ]
    },
    {
        "id": 6,
        "service": "Cloud Storage",
        "hosts": "Storage bucket",
        "description": "Stores media and files.",
        "interacts_with": [
            "Server"
        ]
    },
    {
        "id": 7,
        "service": "Firebase Hosting",
        "hosts": "Frontend Client",
        "description": "Hosts the static frontend client.",
        "interacts_with": [
            "Server",
            "Realtime Database"
        ]
    }
]
"""
@app.post("/start-deployment/{project_name}")
async def start_deployment(project_name:str, r: Request):
    data = await r.json()
    with open("deploy.sh", 'w') as f:
        f.write("gcloud auth login\n")
        f.write(f"gcloud config projects set {project_name}\n")
        for d in data:
            if 'sql' in d['service'].lower():
                f.write(f"gcloud sql instances create {d['name']} --database-version={d['type']} --cpu=1 --memory=512MB --region={d['zone']} --root-password={d['pwd']}\n")
            elif d['service'].lower() == 'cloud run':
                f.write(f"docker build {d['project_path']} -t {d['zone']}-docker.pkg.dev/{project_name}/{d['registry_name']}/{d['image_name']}:latest\n")
                f.write(f"docker push {d['zone']}-docker.pkg.dev/{project_name}/{d['registry_name']}/{d['image_name']}:latest\n")
                f.write(f"gcloud run deploy --image={d['zone']}-docker.pkg.dev/{project_name}/{d['registry_name']}/{d['image_name']}:latest --region={d['zone']} --platform-managed --allow-unauthenticated\n")
            elif d['service'].lower() == 'cloud storage':
                f.write(f"gcloud storage buckets create gs://{d['name']} --location={d['zone']}\n")
    
    return {'detail':'file saved'}


    # s = Session()
    # s.set_project(project_name)
    # command_args = {}
    # for d in data:
    #     if 'sql' in d['service'].lower():
    #         command_args.update({
    #             'sql':{
    #                 'name':d['name'],
    #                 'type':'',
    #                 'pwd':d['pwd']
    #             }
    #         })
    #     elif d['service'].lower() == 'cloud run':
    #         command_args.update({
    #             'cloud_run':{
    #                 'name': d['name'],
    #                 'project_path': d['project_path'],
    #                 'registry_name': d['registry_name'],
    #                 'image_name': d['image_name'],
    #             }
    #         })
    #     elif d['service'].lower() == 'cloud storage':
    #         command_args.update({
    #             'cloud_storage':{
    #                 'name': d['name']
    #             }
    #         })

    # if 'sql' in command_args:
    #     s.create_sql_instance(command_args['sql']['name'], command_args['sql']['type'], command_args['sql']['pwd'])
    # if 'cloud_storage' in command_args:
    #     s.create_storage_bucket(command_args['cloud_storage']['name'])
    # if 'cloud_run' in command_args:
    #     run = command_args['cloud_run']
    #     s.create_artifact_registry(run['registry_name'])
    #     s.prepare_image_for_registry(run['project_path', run['image_name']])
    #     s.create_cloud_run_instance(run['name'])
    