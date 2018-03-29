# multilingual-chatbot
**Think 2018 Lab Session:**

Watson Assistant + Watson Language Translator to create a multilingual chatbot

## Setup

Verify that your system satisfies the dependencies below:
- Docker
- Miniconda
- Bluemix CLI w/ Cloud Functions plugin

Create a python environment with conda:
```
conda env create -f environment.yml
```

Activate the environment
```
source activate watson
```

## 1. Create Watson services

Sign up for an IBM Cloud account at https://console.bluemix.net/

#### Watson Language Translator
From the dashboard, click on **Create resource** and search for **Language Translator**.

Provision an instance of Language Translator under the **Lite** plan.

Create a set of credentials by clicking **Service credentials** > **New credential** > **Add**.

#### Watson Assistant
From the dashboard, click on **Create resource** and search for **Watson Assistant**.

Provision an instance of Watson Assistant under the **Lite** plan.

Click **Launch Tool**.

Create an instance by clicking on **Edit Sample** of the Car Dashboard workspace.

Make a note of `<conversation-workspace-id>`.
This can be found under **Deployment > Credentials** of the individual workspace editor
or by clicking on **View Details** from the home **Workspaces** page of the tool.

Once Watson has finished training, you may test out interacting with the assistant
by clicking on **Try it** on the right side of the page.

**Challenge:** try editing your workspace to customize the flows and responses.


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
<conversation-instance-name>    conversation    free
<translator-instance-name>    language_translator    free
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

## Run a full conversation

Get the namespace for your deployed cloud function
```
bx wsk action get translator namespace
```

Run the program. Experiment with switching between languages mid-conversation
```
python main.py --namespace <namespace>
```

