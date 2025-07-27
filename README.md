# AI-Ops

**AI-Ops** is a tool that helps you quickly generate deployment scripts from an architectural model of your project. It identifies key infrastructure components and maps them to appropriate Google Cloud Platform (GCP) or Firebase services.

## Requirements

- A GCP account with billing enabled  
- [gcloud CLI](https://cloud.google.com/sdk/docs/install)  
- Python 3.8+  

## Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-ops.git
cd ai-ops

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn server:app --host 0.0.0.0 --port $PORT
