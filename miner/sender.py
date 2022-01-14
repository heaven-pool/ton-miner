import os
from urllib.parse import urljoin

import model
import requests
from loguru import logger

REGISTRY_API = '/registry'
JOB_API = '/job/'
UPDATE_API = '/job/update/'


def registry(miner: model.MinerSchema):
    api_url = urljoin(miner.pool_url, REGISTRY_API, miner.miner_wallet)
    logger.debug('registry_api_url: ' + api_url)

    try:
        r = requests.get(api_url, timeout=10)
        response = r.json()
    except Exception as e:
        logger.warning('Failed to connect to pool: ' + str(e))
        os._exit(1)

    if 'status' not in response:
        logger.warning('please check your wallet address: ' + response['msg'])
        os._exit(1)

    return response


def job(miner: model.MinerSchema) -> model.JobSchema:
    api_url = urljoin(miner.pool_url, JOB_API)
    logger.debug('job_api_url: ' + api_url)

    try:
        r = requests.get(api_url, timeout=10)
        response = r.json()
    except Exception as e:
        logger.warning('Failed to connect to pool: ' + str(e))

    miner_job = model.JobSchema(response)
    logger.debug('miner_job: ' + miner_job)
    return miner_job


def update(miner: model.MinerSchema, result: model.JobResultSchema):
    api_url = urljoin(miner.pool_url, UPDATE_API)
    logger.debug('api_url: ' + api_url)

    try:
        r = requests.post(api_url, data=result.json(), timeout=10)
        r.json()
    except Exception as e:
        logger.warning('Failed to connect to pool: ' + str(e))
