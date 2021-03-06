from urllib.parse import urljoin

import requests
from libs import models
from loguru import logger

REGISTRY_API = '/registry'
JOB_API = '/job'
SUBMIT_API = '/submit'


# def registry(miner: models.MinerSchema):
#     api_url = urljoin(miner.pool_url, REGISTRY_API, miner.miner_wallet)
#     logger.debug('registry_api_url: ' + api_url)

#     try:
#         r = requests.get(api_url, timeout=10)
#         response = r.json()
#     except Exception as e:
#         logger.warning('Failed to connect to pool: ' + str(e))
#         os._exit(1)

#     if 'status' not in response:
#         logger.warning('please check your wallet address: ' + response['msg'])
#         os._exit(1)

#     return response


def job(miner: models.MinerSchema) -> models.JobSchema:
    api_url = urljoin(miner.pool_url, JOB_API)
    logger.debug('job_api_url: ' + api_url)

    try:
        r = requests.get(api_url, timeout=10)
        response = r.json()
    except requests.RequestException as e:
        logger.warning('Failed to connect to pool: ' + str(e))
    else:
        if r.ok:
            job = models.JobSchema.parse_obj(response)
            return job
        else:
            return None


def submit(miner: models.MinerSchema, result: models.JobResultSchema):
    api_url = urljoin(miner.pool_url, SUBMIT_API)
    logger.debug('api_url: ' + api_url)

    try:
        r = requests.post(api_url, data=result.json(), timeout=10)
    except requests.RequestException as e:
        logger.warning('Failed to connect to pool: ' + str(e))
    else:
        if not r.ok:
            logger.warning('Failed to connect to pool: ' + str(r.text))
        return 1 if r.ok else 0  # TODO count should be decided by caller
