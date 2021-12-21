# watermark-cloud-function

A Python cloud function that watermarks an uploaded pdf to cloud storage

# pre-requesites

To use this repo you will require:
* Python 3
* gcloud cli

# creating a cloud function from gcloud

Before you create a gcloud function in GCP make sure you have created a GCP project.
To set the current project to deploy to use the following command:

```
gcloud projects list
```
To set your desired project run the command:

```
gcloud config set project project-name
```

# Deploying the sample function

To deploy the function run the following gcloud function from the folder where the function resides:

In this repo change 
```
gcloud functions deploy watermark_file \
--runtime python39 --trigger-bucket=storagebucket 
```

Where storagebucket is the bucket triggering the function.