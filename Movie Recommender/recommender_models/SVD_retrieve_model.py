'''
This file retrieves a model from the model registry
at stage "Staging".
'''

# !pip install surprise python-dotenv azure-ai-ml mlflow azureml-mlflow

import warnings
warnings.filterwarnings("ignore")

import mlflow
import os
from mlflow.tracking import MlflowClient
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
load_dotenv()


# Model parameters
SVD_EXPERIMENT_NAME = "SVD-Product-Based-Recommendation-Experiment"
SVD_MODEL_NAME = "SVD-Product-Based-Recommendation-Model"
SVD_ARTIFACT_PATH = "artifact-path-model"
SVD_MODEL_STAGE = "Staging"


# Set Azure variables and set mlflow tracking uri to Azure
if 'AZURE_CLIENT_ID' not in os.environ:
  raise Exception("It seems that Azure environment variables are not set. Please ask alex to provide you with the .env file.")

subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = os.environ.get("AZURE_RESOURCE_GROUP")
workspace = os.environ.get("AZURE_WORKSPACE")

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

azureml_tracking_uri = ml_client.workspaces.get(
    ml_client.workspace_name
).mlflow_tracking_uri
mlflow.set_tracking_uri(azureml_tracking_uri)

###############################################################################

model_path = f"models:/{SVD_MODEL_NAME}/{SVD_MODEL_STAGE}"
model = mlflow.sklearn.load_model(model_path)