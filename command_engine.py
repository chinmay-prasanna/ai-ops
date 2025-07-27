import subprocess
import os
import re

class Session:
    def __init__(self):
        self.process = subprocess.Popen(
            ['/bin/bash'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
    
    def display_users(self):
        self.process.stdin.write("gcloud auth list; echo __END__\n")
        self.process.stdin.flush()

        emails = []
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+$"
        while True:
            line = self.process.stdout.readline()
            if line.startswith("*"):
                line = line[1:]
            match = re.search(pattern, line.strip())
            if match:
                emails.append(match.group())
            if line.strip() == "__END__":
                break
    
    def display_projects(self):
        self.process.stdin.write("gcloud projects list; echo __END__\n")
        self.process.stdin.flush()

        projects = []
        pattern = r"\d+"
        while True:
            line = self.process.stdout.readline()
            match = re.search(pattern, line.strip())
            if match:
                projects.append(line.strip().split()[0])
            if line.strip() == "__END__":
                break

        print(projects)

    def create_project(self, name):
        self.process.stdin.write(f"gcloud projects create {name} --set-as-default; echo __END__\n")     
        self.process.stdout.flush()
        lines = []
        while True:
            line = self.process.stdout.readline()
            lines.append(line)
            if line.strip() == "__END__":
                break
        self.project_name = name

    def set_project(self, name):
        self.process.stdin.write(f"gcloud config set project {name}")
        self.project_name = name

    def create_sql_instance(
        self,name, type, r_pwd,cpu_n=1,memory="512mb",
        zone="asia-south1"
    ):
        self.process.stdin.write(f"gcloud sql instances create {name} --database-version={type} --cpu={cpu_n} --memory={memory} --region={zone} --root-password={r_pwd}; echo __END__\n")
        self.process.stdin.flush()
        lines = []
        while True:
            line = self.process.stdout.readline()
            lines.append(line)
            if line.strip() == "__END__":
                break
    
    def create_storage_bucket(self, name, zone="asia-south1"):
        self.process.stdin.write(f"gcloud storage buckets create gs://{name} --location={zone}; echo __END__\n")
        self.process.stdin.flush()
        lines = []
        while True:
            line = self.process.stdout.readline()
            lines.append(line)
            if line.strip() == "__END__":
                break

    def create_queue(self, name, zone="asia-south1"):
        self.process.stdin.write(f"glcoud tasks queues create {name} --location={zone}; echo __END__\n")
        self.process.stdin.flush()
        lines = []
        while True:
            line = self.process.stdout.readline()
            lines.append(line)
            if line.strip() == "__END__":
                break

    def create_artifact_registry(self, name, zone="asia-south1", format="docker"):
        self.process.stdin.write(f"gcloud artifacts repositories create {name} --repository-format={format} --location={zone}; echo __END__\n")
        self.process.stdin.flush()
        lines = []
        while True:
            line = self.process.stdout.readline()
            lines.append(line)
            if line.strip() == "__END__":
                break
        self.registry_name = name
        self.registry_zone = zone

    def prepare_image_for_registry(self, project_path, image_name, tag):
        self.process.stdin.write(f"docker build {project_path} -t {self.registry_zone}-docker.pkg.dev/{self.project_name}/{self.registry_name}/{image_name}:{tag}; echo __END__\n")
        self.process.stdin.flush()
        lines = []
        while True:
            line = self.process.stdout.readline()
            lines.append(line)
            if line.strip() == "__END__":
                break
        self.image = f"{self.registry_zone}-docker.pkg.dev/{self.project_name}/{self.registry_name}/{image_name}:{tag}"
        
    def push_image_to_registry(self):
        self.process.stdin.write(f"docker push {self.image}; echo __END__\n")
        self.process.stdin.flush()
        lines = []
        while True:
            line = self.process.stdout.readline()
            lines.append(line)
            if line.strip() == "__END__":
                break

    def create_cloud_run_instance(self, name, zone="asia=south1"):
        self.process.stdin.write(f"gcloud run deploy --image={self.image} --region={zone} --platform-managed --allow-unauthenticated; echo __END__\n")
        self.process.stdin.flush()
        lines = []
        while True:
            line = self.process.stdout.readline()
            lines.append(line)
            if line.strip() == "__END__":
                break

s = Session()
s.create_project("testing-from-ai-fordakew")