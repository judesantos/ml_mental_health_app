import json
import requests
from loguru import logger
from typing import List, Dict

from google.cloud import run_v2
from app.ml.config.gcp import gcp_settings


_cloud_run_url = None


def _get_cloud_run_url(project_id, region, service_name):
    """
    Fetch the Cloud Run URL using the Google Cloud Run API.
    """
    global _cloud_run_url
    logger.info('Fetching Cloud Run URL...')

    if _cloud_run_url is not None:
        logger.info(f'Cloud Run URL: {_cloud_run_url}')
        return _cloud_run_url

    service_path = f"projects/{project_id}/locations/{region}/services/{service_name}"
    client = run_v2.ServicesClient()

    try:

        service = client.get_service(name=service_path)
        cloud_run_url = service.uri

        logger.info(f'Found Cloud Run URL: {cloud_run_url}')

        return cloud_run_url

    except Exception as e:
        logger.error(f'Failed to retrieve Cloud Run URL: {e}')
        return None


def get_prediction(data: List[Dict]):

    logger.info('get_prediction...')

    # endpoint_url = _get_cloud_run_url(
    #    gcp_settings.gcp_project_id,
    #    gcp_settings.gcp_region,
    #    gcp_settings.gcp_service_name
    # )
    endpoint_url = 'https://mlops-endpoint-416879185829.us-central1.run.app'

    if not endpoint_url:
        raise RuntimeError(
            'Cloud Run URL not found. Service might not be deployed.')

    logger.info(f'Cloud Run URL: {endpoint_url}')

    headers = {'Content-Type': 'application/json'}
    uri = f"{endpoint_url}/predict"

    logger.info(f'Sending request to {uri}')

    payload = {"instances": data}
    payload_json = json.dumps(payload)
    logger.debug(f'Payload: {payload_json}')

    response = requests.post(
        uri,
        data=payload_json,
        headers=headers
    )

    logger.info(f'Response status code: {response.status_code}')
    logger.info(f'Response content: {response.content}')

    json_response = response.json()

    if 'success' in json_response and json_response['success']:
        if 'prediction' in json_response:
            return json_response['prediction']
        else:
            raise RuntimeError('Prediction not found in response.')
    else:
        raise RuntimeError('Prediction failed.')
