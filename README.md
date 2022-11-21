# RCCE Collective Service Server

Backend Server for RCCE Collective Service Project

# Sync Filter Options

## Local Deployment

The following command needs to be executed inside the container every time new indicators are added in the database.

`docker-compose exec server python manage.py sync_filter_options`

## AWS Deployment

Run these commands to get shell access in the ECS Container. If you don't get the access, remove the task from ECS and in some time, another task instance shall pop-up which shall have execute command.

```bash
aws ecs --profile <profile-name> update-service --cluster <cluster-name> --task-definition <task-def-name> --enable-execute-command --service <service-name> --desired-count 1
```

To get shell access to the ECS Container, run the following command. If you don't get the shell access, delete the task and wait for sometime for the task to create.

```bash
aws ecs --profile <profile-name> execute-command --cluster <cluster-name> --task <task-id> --container <container-name> --interactive --command "/bin/sh"
```

Once you have the shell access, run the command to sync the updated indicators list.

`python manage.py sync_filter_options`