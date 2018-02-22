# multilingual-chatbot
**Think 2018 Lab Session:**
Watson Conversation Service + Watson Language Translator to create a multilingual chatbot

## Setup
If you are at **Think 2018** and working from a Skytap VM, you can **skip this section.**
Your working environment should be ready to go.

For those not using a VM, you will need to install the dependencies below
- Docker
- Miniconda
- Bluemix CLI
- (TODO versions)

Create a python environment with conda:
```
conda cenv create -f environment.yml
```

## 1. Create Watson Services
TODO: what does this process look like? Pending info from conference team
(bluemix accounts, service provisioning, etc.)

## 2. Deploying your Cloud Function
Make sure you are in the `multilingual-chatbot` directory.
Run the deployment script to package and update your cloud function
```
./deploy_cloudfunction.sh
```