# multilingual-chatbot
**Think 2018 Lab Session:**

Watson Conversation Service + Watson Language Translator to create a multilingual chatbot

## Setup
If you are at **Think 2018** and working from a Skytap VM, you can **skip this section.**
Your working environment should be ready to go.

For those not using a VM, you will need to install the dependencies below
- Docker
- Miniconda
- Bluemix CLI w/ Cloud Functions plugin
- (TODO versions)

Create a python environment with conda:
```
conda env create -f environment.yml
```

## 1. Create Watson services
TODO: what does this process look like? Pending info from conference team
(bluemix accounts, service provisioning, etc.)

...

Make a note of `<conversation-workspace-id>`


## 2. Deploying your Cloud Function
#### Configure the Bluemix CLI
Login in to your account (follow the prompts)
```
bx login
```
Target the organization and space that contains your services (follow the prompts)
```
bx target --cf
```

#### Deploy the action
Make sure you are in the `multilingual-chatbot` directory.

Run the deployment script to package and update your cloud function
```
./deploy_cloudfunction.sh
```

#### Binding your Watson services

Bind the conversation workspace ID (from above) as a default parameter
```
bx wsk action update translator --param conversation_workspace_id <conversation-workspace-id>
```

Check name of your Watson service instances
```
bx service list
```

You should see output that looks something like this:
```
<conversation-instance-name>        conversation                     free
<translator-instance-name>             language_translator         free
```

Attach these services to your cloud function
```
bx wsk service bind conversation translator --instance <conversation-instance-name>
bx wsk service bind language_translator translator --instance <translator-instance-name>
```

Verify that these services are available as parameters to your cloud function
```
bx wsk action get translator parameters
```

Send a few sample requests
```
bx wsk action invoke translator --result
bx wsk action invoke translator --result --param text "hi there"
bx wsk action invoke translator --result --param text "hola amigo"
```