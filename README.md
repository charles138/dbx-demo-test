# dbx-demo-test
This repository is a continuation of the [csc-project](https://github.com/charles138/csc-project). However, it includes different unit and integration tests and a demonstration to determine the environment (development, staging, or production) based on the repository's metadata. Using this information, we can retrieve the corresponding catalog, landing path, and databases from a provided JSON file. Additionally, it includes a pull request template to gather relevant information.

Lastly, there are three Gitaction YAML files to achieve Continuous Integration and Continuous Deployment (CI/CD), which will be demonstrated in the following steps.

Note:
- I assume you have set up conda, git, gh, databricks cli, and dbx on your local laptop.
- If you want to run the demonstration with an Azure Service Principal (SP), please refer to the document titled "[[Provision a Service Principal, Generate the SP Token, Update the Token to Downstream Applications](https://github.com/charles138/dbx-demo-test/blob/main/docs/Azure%20Service%20Principal%20Token.md)](./docs/Azure%20Service%20Principal%20Token.md)" to set it up.

## 1.	Import the Repository to Your GitHub
```
https://github.com/charles138/dbx-demo-test.git
```

## 2.	Preparing the Local Environment
```bash
####--------------------------------------------------------
### Create conda environment
####--------------------------------------------------------
conda activate base
conda create -n charming-aurora python=3.9  -y
conda activate charming-aurora

####--------------------------------------------------------
### Install databricks cli and dbx
####--------------------------------------------------------
python -m pip install --upgrade pip
pip install databricks-cli --upgrade
pip install dbx --upgrade
databricks --version
dbx --version

####--------------------------------------------------------
### Setup and check Databricks CLI
####--------------------------------------------------------
databricks configure --profile charming-aurora --token
databricks --profile charming-aurora workspace ls /Repos
databricks jobs configure --version=2.1 --profile charming-aurora

####--------------------------------------------------------
### Install blackbricks linter
####--------------------------------------------------------
pip install blackbricks
```
Note: Please refer to the webpages titled "[Databricks CLI (legacy)](https://docs.databricks.com/archive/dev-tools/cli/index.html)" for instructions on configuring Databricks CLI authentication, and "[blackbricks](https://github.com/inspera/blackbricks)" for information about the usage of blackbricks.

## 3.	Clone the Repository to Your Local Laptop
```bash
git clone https://github.com/<your_name>/dbx-demo-test.git
cd dbx-demo-test
```

## 4.	Setup GitHub Repository Secrets
```bash
gh secret set DATABRICKS_HOST
gh secret set DATABRICKS_TOKEN
gh secret list
```
Note: Please refer to the step 2 for DATABRICKS_HOST and DATABRICKS_TOKEN.

## 5.	Setup at Databricks
- Interactive Cluster: Create a lightweight interactive cluster and modify the CLUSTER_ID in the conf/vars.yml file to reduce waiting times during testing. Please be aware that this approach is not recommended for production environments. For best practices, please refer to the "[Cluster Type](https://dbx.readthedocs.io/en/latest/concepts/cluster_types/)" documentation.
- Deployment File: For any modifications, please consult the webpage titled "[Deployment File Reference](https://dbx.readthedocs.io/en/latest/reference/deployment/)."
- Repository Folders: Create three repository folders: /Repos/Development, /Repos/Staging, and /Repos/Production.
- Git Integration: Follow the instructions on the webpage titled "[Git Integration with Databricks Repos](https://docs.databricks.com/repos/index.html#git-integration-with-databricks-repos)" to set up the integration.
```bash
####--------------------------------------------------------
### Create Development - featurenn Repo
### Assuming that feature109 branch exists.
####--------------------------------------------------------
export FEATURE_BRANCH=feature109
echo FEATURE_BRANCH=$FEATURE_BRANCH
databricks repos delete --path /Repos/Development/dbx-demo-test-$FEATURE_BRANCH --profile charming-aurora || true
databricks repos create --url "https://github.com/charles138/dbx-demo-test.git" --provider gitHub --path "/Repos/Development/dbx-demo-test-$FEATURE_BRANCH" --profile charming-aurora
databricks repos update --path "/Repos/Development/dbx-demo-test-$FEATURE_BRANCH" --branch $FEATURE_BRANCH --profile charming-aurora

####--------------------------------------------------------
### Create Staging Repo
####--------------------------------------------------------
databricks repos create --url "https://github.com/<your name>/dbx-demo-test.git" --provider gitHub --path "/Repos/Staging/dbx-demo-test" --profile charming-aurora

####--------------------------------------------------------
### Create Production Repo
####--------------------------------------------------------
databricks repos create --url "https://github.com/<your name>/dbx-demo-test.git" --provider gitHub --path "/Repos/Production/ dbx-demo-test" --profile charming-aurora
```

## 6. Testing: Run Unit Tests
```bash
pip install -e ".[local,test]"
pytest tests/unit --cov
```

## 7. Testing: Run Integration Tests
```bash
####--------------------------------------------------------
### dbx submit a job
### Assuming that feature109 branch exists.
####--------------------------------------------------------
export FEATURE_BRANCH=feature109
echo FEATURE_BRANCH=$FEATURE_BRANCH
databricks jobs list --profile charming-aurora --output json \
| jq --arg FEATURE_BRANCH_JOB "dbx-demo-test-development-$FEATURE_BRANCH-job" '.jobs[] | select(.settings.name == $FEATURE_BRANCH_JOB) | .job_id' \
| xargs -n 1 databricks --profile charming-aurora jobs delete --job-id 

dbx deploy dbx-demo-test-development-$FEATURE_BRANCH-job --jinja-variables-file=conf/vars.yml
dbx launch dbx-demo-test-development-$FEATURE_BRANCH-job
```

## 8. Testing: Run Staging ETL Task
```bash
dbx deploy dbx-demo-test-staging-job --jinja-variables-file=conf/vars.yml
dbx launch dbx-demo-test-staging-job
```

## 9. Testing: Run Production ETL Task
```bash
dbx deploy dbx-demo-test-production-job --jinja-variables-file=conf/vars.yml
dbx launch dbx-demo-test-production-job 
```

## 10.	Trigger Unit and Integration Tests (.github/workflows/onpush.yml)
Note: For the steps 10 ~ 12, please choose proper feathurexx and vxx.xx.xx. 
```bash
git checkout main
git pull origin main

git checkout -b feature110
# Append a line to tag.txt, such as “csc 2023-08-01 16:08: feature110”.
blackbricks --check .  # Check the notebooks format
blackbricks .   # Format the notebooks
git status
git add .
git commit -m "csc 2023-08-01 16:08: feature110"
git push --set-upstream origin feature110
```

## 11.	Trigger the deployment of the main branch to the staging repository and deploy the job to Databricks (.github/workflows/after_pull_request_merge.yml)
Complete the following steps:
- Navigate to the Actions tab of the Github repository.
- Wait for the workflow - CI pipeline of Gitaction to complete successfully.
- Navigate to the Workflow of Databricks and search for the job named "dbx-demo-test-development-featurennn-job." Review the logs and copy the link.
- Navigate to the Code tab of the Github repository, and click on "Compare & pull request."
- Complete the "Open a pull request" form, including pasting the link from the above log in the Testing section.
- Scroll down the page and review all the changes.
- If everything is okay, click on "Create pull request."
- Click on "Show all checks" and then click on "details." If necessary, you can review the CI pipeline log again.
- Click on "Merge pull request" and "confirm merge" to trigger the Github action "after_pull_request_merge.yml."
- Navigate to the Actions tab of the Github repository, review the "Merge from feature* to main" workflow, and ensure it has completed successfully.
- It's now ready for QA.
- If it passes the QA tests, it's ready for Change Management approval.

## 12.	Trigger the release process, deploy the release to the production repository and deploy the job to Databricks (.github/workflows/onrelease.yml)
Once it has been approved by Change Management, it is ready for the release process.
```bash
git pull origin main
# Append a line to tag.txt, such as “csc 2023-08-01 16:50 v110.0.0”.
git status
git add .
git commit -m "2023-08-01 16:36 v110.0.0"
git push origin main

git tag -a v110.0.0 -m "v110.0.0"
git push origin v110.0.0
```




