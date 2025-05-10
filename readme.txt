
To run the code locally, please follow below steps

1- Install python in your local machine
2- open the source code in visual studio code
3- in VS code menu click on view tab and open the terminal 
then run the commands one be one-  
4- python -m venv venv 
5- venv\Scripts\activate
6- pip install -r requirements.txt

once all packages are isntalled then run below command to start the app-
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

and then go to chrome browser and paste the belwo url 

http://localhost:8000/docs
---------------------------------------------------------------------------------------------

Deploying a FastAPI web service on an AWS EC2 instance involves the following steps:

Step 1: Launch an EC2 Instance
Login to AWS Console → Go to EC2 Dashboard.

Launch an EC2 Instance:

Choose Amazon Linux 2 or Ubuntu 22.04 LTS (recommended).

Select an appropriate instance type (e.g., t3.micro for small applications).

Configure security group:

Allow HTTP (80) and HTTPS (443) (for public access).

Allow port 22 for SSH access.

Allow port 8000 (or your chosen FastAPI port).

Click Launch and download the key-pair file (.pem).

Connect to EC2 via SSH:

bash
Copy
ssh -i your-key.pem ec2-user@your-ec2-public-ip
ssh -i VirtualHeathAPIKey.pem ec2-user@ec2-54-84-47-62.compute-1.amazonaws.com

Step 2: Install Dependencies
Once connected to the EC2 instance, install the necessary packages:

Update the system:

bash
Copy
sudo apt update && sudo apt upgrade -y    # For Ubuntu
sudo yum update -y                        # For Amazon Linux
Install Python and pip:

bash
Copy
sudo apt install python3 python3-pip -y  # For Ubuntu
sudo yum install python3 python3-pip -y  # For Amazon Linux
Install virtual environment:

bash
Copy
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv


Step 3: Set Up Your FastAPI Application
Clone or create your FastAPI project:

bash
Copy
mkdir fastapi-app && cd fastapi-app
Create a virtual environment and activate it:

bash
Copy
python3 -m venv venv
source venv/bin/activate
Install FastAPI and Uvicorn:

bash
Copy
pip install fastapi uvicorn
Create app.py:

bash
Copy
nano app.py
Add the following FastAPI example:

python
Copy
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI on EC2!"}
Run FastAPI to test:

bash
Copy
uvicorn app:app --host 0.0.0.0 --port 8000

cd ~/VirtualHeathAPI-PredictiveAI
source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > output.log 2>&1 &

Open http://your-ec2-public-ip:8000 in your browser.
http://54.84.47.62:8000/docs#/default/predict_combined_predict_combined_post

If you see {"message":"Hello, FastAPI on EC2!"}, it’s working.

