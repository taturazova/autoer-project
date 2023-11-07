# GoCD Setup

## Installation

GoCD is split into two components:

- The main server which controls the GoCD browser frontend and CI/CD configuration/initiation.
- An agent which executes CI/CD instructions sent from the GoCD server.

You can install the above components as follows:

1. Install the GoCD server as detailed [here](https://docs.gocd.org/current/installation/installing_go_server.html).

2. Install the GoCD agent as detailed [here](https://docs.gocd.org/current/installation/installing_go_agent.html).

## Accessing GoCD over SSH

Working with GoCD requires using the GoCD website frontend. GoCD publishes this frontend at http://localhost8153. Initial configuration of GoCD does not allow access to the frontend publically.

To access this frontend in a secure manner, SSH port forwarding can be used to expose GoCD on your local system. Before beginning, please ensure you have no other services bound to port 8153 and that you also have SSH access to the server GoCD is running on.

For Linux and macOS users, the built-in SSH utility can be used to expose GoCD with the following command:

```bash
ssh -L 8153:SSH_SERVER_IP:8153 SSH_USERNAME@SSH_SERVER_IP
```

For Windows users, the newest versions of Windows 10 (as of June 23rd 2021) provide a built-in SSH CLI capable of running the above command. Windows users that use an SSH utility (such as Putty), must search their respective utility's documentation for port forwarding functionality.

## Getting Started with GoCD

For a general overview of using GoCD over the browser frontend, please consult the Introduction guide found [here](https://www.gocd.org/getting-started/part-1/).

## Running Continuous Integration or Coninuous Deployment Jobs

GoCD defines a given Continuous Integration (CI) or Continuous Deployment (CD) job as a "pipeline" within the server. Pipelines contain material (or code) that is interacted with based on defined CI/CD tasks (basically a series of command line arguments). Further reading on concepts within GoCD can be found [here](https://docs.gocd.org/current/introduction/concepts_in_go.html)

### Creating a Pipeline

Generally, the easiest way to initially define a pipeline is through use of GoCD's Pipeline Wizard. Instructions on access/use of the wizard can be found [here](https://docs.gocd.org/current/configuration/quick_pipeline_setup.html).

### Extra Details on Adding Material to a Pipeline

Repositories or other resources polled for changes and deployed from are defined as "Materials" within GoCD. On initial setup of the GoCD server, you will be prompted to setup an initial material. If this is a public repository, you can simply include the repository's URL and desired branch name from which changes are tracked from. 

If the desired repository is private, a user's Git credentials must be provided in order to allow GoCD to access the repo. Github, specifically, requires users who have enabled 2FA use a Personal Access Token in the place of their Github password. Documentation on generating Github Personal Access Tokens can be found [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token).

Further documentation on adding materials to GoCD can be found [here](https://docs.gocd.org/current/configuration/admin_add_material.html).

## Adding Authentication to GoCD

An initial setup GoCD installation provides no authentication and defaults to unauthenticated administrative priviledges on access. Authentication can be added to GoCD through use of file-based password logins or OAuth-based logins. Further details on setup can be found [here](https://docs.gocd.org/current/configuration/dev_authentication.html)

## Disabling Pipelines

1. Navigate to the dashboard of GoCD and click on the Gear icon within the pipeline you would like to disable.

2. Within the pipeline's settings menu, uncheck the tick box with the label "Automatic Pipeline Scheduling". Unchecking this box will prevent the pipeline from running when the linked material is updated. This effectively disables the pipeline (unless run manually).
