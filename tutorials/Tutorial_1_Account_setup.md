# Tutorial 1: Set up your account for GDSC 2024

Welcome to the first tutorial of the 2024 GDSC: The Grade-AI Generation! The tutorials will teach you all the necessary steps to participate in (and hopefully win) the challenge. 
This first tutorial covers the (boring) groundwork that we need to cover before we can jump into the AI parts. It explains how to create an account, sign in, create and join a team and how to access AWS.

But before we jump in make sure you join the [GDSC Teams channel](https://teams.microsoft.com/l/team/19%3a4017a2e9af4942e7aa157d6ec9d751b4%40thread.skype/conversations?groupId=7d77d672-dff1-4c9f-ac55-3c837c1bebf9&tenantId=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61/) for all updates from the organisation team and meeting and connecting with other participants. 

Here is a quick overview of what we'll cover:

  - [1. Signing up and logging to the website](#1-signing-up-and-logging-to-the-website)
  - [2. Creating and joining a team](#2-team-management)
  - [3. Setting up your AWS accounts](#3-setting-up-your-aws-accounts)
  - [4. How to use AWS](#4-how-to-use-aws)
    - [4.1. Accessing GenAI Models with AWS Bedrock](#41-accessing-genai-models)
    - [4.2. Managing source code with AWS CodeCommit](#42-managing-source-code)
    - [4.3. Developing AI solutions with Sagemaker](#43-developing-ai-solutions)
    - [4.4. Keeping track of the costs](#44-costs-management)
  - [5. Where to develop your solution](#5-coding-environment-options)
    - [5.1. On your laptop](#51-locally)
    - [5.2. With AWS Sagemaker](#52-in-aws)
  - [6. Conclusion](#6-conclusion)

## 1. Signing up and logging to the website:

1. Navigate to the GDSC Portal's Sign-up page - [https://gdsc.ce.capgemini.com/app/signup/](https://gdsc.ce.capgemini.com/app/signup/). Make sure to enter your Capgemini email. The full name is not mandatory to sign up, but it is necessary to receive a certificate of completion after the challenge. ![Signup](../images/t1_signup.png)
2. Once you Sign-up, you will receive an e-mail like the one shown below from gdsc.ce@capgemini.com.  ![Welcome email](../images/t1_welcomeemail.png)
3. Please click on the Verfication link provided in the e-mail. You will receive an error such as this. But do not worry, you can now login to the website.

   <img src="../images/t1_invalid_link.png" width="400"/>
4. To login to the website, navigate to the login page - [https://gdsc.ce.capgemini.com/app/login/](https://gdsc.ce.capgemini.com/app/login/) and enter your credentials. ![Login](../images/t1_login.png)
5. Once you login you will have access to the Resources - [https://gdsc.ce.capgemini.com/app/portal/resources/](https://gdsc.ce.capgemini.com/app/portal/resources/). The page has link to all the information and Tutorials that you will be needing for the challenge. You can also access the Usecase page to learn more about the challenge. Feel free to explore the website for information about the current challenge and the past editions.

## 2. Team management

All team management actions are done in the My Team page - [https://gdsc.ce.capgemini.com/app/portal/](https://gdsc.ce.capgemini.com/app/portal/).

1. Every participant needs to be in a team to participate in a challenge. These are your three options:
   * Create a team only for yourself
   * Create a team, find other people to join, share their team id with them. They will request to join and you can accept
   * Request to join an existing team
2. If you want to do the challenge as a group, you can find other people in the GDSC Teams channel 'Looking for Team'. There can be up to 4 people in a team.
3. Example of creating a new team

   ![Team Creation Button](../images/t1_create_team.png)
4. Once a team is created, you are assgned a Team ID, which you can share with potential team members and ask them to join your team. You are also assigned an AWS account, in this example *AneTestAccount0008*

   ![Team Created](../images/t1_team_created.png)
5. Example of requesting to join a team

   ![Team Join Request](../images/t1_join_request.png)
6. Once requested to join a team, you can cancel your request

   ![Team Join Request](../images/t1_join_request2.png)
7. Team lead can approve or decline requests from new members

   ![Team Approvals](../images/t1_approve.png)
8.  Team members can choose to leave the team
9.  The team lead (the team creator) can remove members from the team. Any new join requests can then be taken care of

    ![Team Approvals](../images/t1_approval2.png)
10. ⚠️ Warning for the Team Leads: If you delete the team, all members, permissions and resources in your AWS account will be destroyed

## 3. Setting up your AWS accounts

1. You can find information about accessing AWS in the My Team page. If you have created a team, you will see the account name in the third step.
2. You can login to your AWS account with your Capgemini email address as the user name [https://gdsc22.awsapps.com/start#/](https://gdsc22.awsapps.com/start#/)

   <img src="../images/t1_aws_1.png" width="400"/>
3. Once you do this, you will receive an email from no-reply@login.awsapps.com with the verification code and then you can set your password.

   <img src="../images/t1_aws_2.png" width="600"/>
4. Once your password is set, you can log in to your account afterwards. You will see the AWS Portal with your account and the TeamAccess role.

   ![](../images/t1_aws_acc2.png)
5. You can develop your solution in the AWS console or locally. If you will be developing locally, you can export your credentials. Click on the Access keys for the TeamAccess role, copy the export commands from option 1 and paste them in your terminal. Then, run the command `aws sts get-caller-identity`. If you see the response shown in the screenshot, you are all set. If it says the token is expired, refresh the AWS page and copy the credentials again

   ![AWS CLI access](../images/t1_aws_cli.png)

## 4. Exploring AWS resources

This is the main page in the AWS console, showing the most used resources and an overview of the costs.
* Make sure you are in N. Virginia region (on the top right)
* You can change language and the theme in the settings button to the left of the region
* On the top left, you can search for services

![Overview of the AWS console](../images/t1_aws_console.png)

### 4.1. Bedrock

For an overview of the LLM models, access the Bedrock service. By opening the panel on the left, you can access the Base models for an overview of the models, and use the Text Playground to interact with models. In the GDSC only some models are allowed, those will be shared at the beginning of the challenge

![Bedrock overview](../images/t1_bedrock_overview.png)

### 4.2. CodeCommit

CodeCommit contains the code for the challenge. Navigating to the CodeCommit resource in AWS, you will find the GDSC repository. This repository contains the initial code provided to you to start the challenge. Your code will also have to be in this repository for the challenge.

To test your code before submitting a solution, push the code to the branch `test_submission`, to submit the code push the code to the branch `submission`. How to test and submit solutions will be explained in tutorial 4.

![CodeCommit overview](../images/t1_aws_codecommit.png)

### 4.3. Sagemaker

Sagemaker notebooks are your IDE in the cloud. Navigate into the Sagemaker service and then to Notebooks. You will find 4 stopped notebooks created for your team.

![Sagemaker overview](../images/t1_aws_sagemaker.png)

You can use one notebook per teammate to work independently. When you start a notebook, it will show "Pending" and it will take around 5mins to start. Then, click on Open JupyterLab.

![Notebook overview](../images/t1_aws_notebook.png)

The notebook is connected to the CodeCommit, the code can be found on the left side. You are able to pull and push the code from the notebook directly.

You can edit the appearance of the environment in the Settings, for instance changing to dark mode or changing the language.

### 4.4. Costs

To explore the costs, you can see a summary in the AWS overview in the main page when you log in, or you can find more detailed information in the "Bililng and cost management" service. On the main page, you can see a summary of the existing costs, and forecasted costs for the current month.

In the "Cost explorer" tab on the left, you can see a more detailed view of the costs. On the right side, you can filter by time range, granularity and dimension.

![Cost explorer overview](../images/t1_aws_cost.png)

## 5. Coding environment options

In the GDSC, you can develop your solution in two ways: either locally or in AWS.

### 5.1. Locally

These are some required configuration to develop locally:

- Set up your development tools: code editor, terminal, git, aws cli library
- Export your AWS credentials as explained in the previous section so you are authenticated to AWS
- Pull the code from the account's CodeCommit to your computer and push it when you are ready to test or submit

### 5.2. In AWS

These are some required configuration to develop in AWS:

- Start your notebook instance when you are ready to develop in Sagemaker
- Pull the code from CodeCommit and push via the notebook directly
- Remember to stop your instance when you are not using it to save costs. If not, it will be automatically be stopped if it's not in use for one hour

## 6. Conclusion

In this tutorial you have learnt how to sign up for the challenge and form your team. You have been assigned an AWS account, where you have explored the code, coding environment, LLM models and costs.

You are now ready for tutorial 2, where you will learn about the dataset for the challenge.
