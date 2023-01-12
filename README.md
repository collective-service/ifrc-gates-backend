# Collective Service Server
Backend Server for Collective Service Project

# Sync Filter Options
Whenever there is an **update in Production Database (e.g. addition of Indicators)**, the Filter Options need to be synced. This can be achieved by logging into the Django Admin Panel and click on the button `SYNC FILTER OPTIONS` on the top right.

# Deployment
- Staging
    - Login to the VM.
      ```bash
        # Update client and server
        cd ~/services/client
        git pull
        
        cd ~/services/server
        git pull
        
        # Update docker containers
        cd ~/services/
        docker-compose up --build -d
      ```
- Production
    - The Github Actions deployment pipeline is triggered whenever changes are pushed to the branch `release`.
    - Requires approval from the administrator.

# Access AWS ECS Container
- Environment
    - Linux or MacOS
- Installations
    - [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html): Install latest version of AWS command line tool
    - [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html): Install latest version of Session Manager plugin for AWS CLI
- Setup AWS Credentials
    - Ask AWS Admin to create a user for you and give you the credentials to login to AWS
    - Run the command:
    - > $ aws configure
    - Provide the credentials
    - Check in the directory if the setup is done correctly.
    - > $ cd ~/.aws (Two files must be created viz. `config` and `credentials`)
    - Note that if you don't define the profile, a `default` profile will be created.
- Login to AWS
    - Login to the AWS Console
    - Ask the Admin to assign ECS access and other ECS policies in the IAM.
    - Navigate to the Elastic Container Service(ECS)
    - In the Clusters tab, note the few names:
        - Cluster Name: e.g. `cluster-backend-prod`
        - Task Definition: e.g. `backend-task-prod:3`
        - Service Name: e.g. `backend-service-prod`
        - Task ID: e.g. `4d038f255f2f41da9eer186a1b976xxx`
        - Container Name: e.g. `backend-container-prod`
    - Once those information is gathered, run the following command in the terminal.
    - > aws ecs --profile `<profile>` update-service --cluster `<cluster_name>` --task-definition `<task_def_name>` --enable-execute-command --service `<service_name>` --desired-count 1
    - Then, try to access the container using the following command in your terminal.
    - > aws ecs --profile `<profile>` execute-command --cluster `<cluster_name>` --task `<task_id>` --container `<container_name>` --interactive --command "/bin/sh"
    - If for some reason you don't have access to the container, you need remove/delete/stop the task within the Cluster. After that, a new task will be created automatically (just wait for a couple of minutes until the new container status reaches `RUNNING`)
    - Then, repeat above steps.
    - Once you have access to the container, run commands for maintenance or debug.