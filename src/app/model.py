# -*- coding: utf-8 -*-s
import uuid
from typing import List, Optional

from pydantic import BaseModel


class MinerSchema(BaseModel):
    pool_wallet: str = "EQB6UzwFx-gZTIZmJmiFWZ7_qTIZ9RwBaR1_2IPtKR4UuAoJ"
    pool_url: str = 'https://ton.heaven-pool.com'
    miner_wallet: str
    unique_id: bytes = hex(uuid.getnode())  # mac address
    GPUs: List[str]

    def _get_mac(self) -> bytes:
        self.unique_id = hex(uuid.getnode())
        return self.unique_id


class JobSchema(BaseModel):
    job_id: int
    expire: int
    complexity: str
    seed: str
    iterations: int
    giver_address: str

class JobResultSchema(BaseModel):
    job_id: int
    wallet: str
    computer_name: str
    computer_uuid: str
    gpu_uuid: str
    hashrate: int
    boc: str

class MineCmdSchema(BaseModel):
    job_id: int
    gpu_id: int
    boost_factor: int = 16
    timeout: int = 900
    expire: int
    complexity: bytes
    seed: str
    iterations: int = 100000000000
    pool_wallet: bytes
    giver_address: bytes
    boc_name: str

    def _cmd(self):
        cmd = f'-v -g {self.gpu_id} -F {self.boost_factor} -t {self.timeout} -e {self.expire} '
        cmd += f'{self.pool_wallet} {self.seed} {self.complexity} {self.iterations} '
        cmd += f'{self.giver_address} {self.boc_name} '
        return cmd
