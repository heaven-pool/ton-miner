# -*- coding: utf-8 -*-s
import platform
import uuid
from typing import List, Optional

from pydantic import BaseModel

# Miner -> create GPUWorker
# Job + GPUWorker -> JobResult


class JobSchema(BaseModel):
    job_id: int
    pool_wallet: str
    complexity: str
    seed: str
    iterations: str
    giver_address: str


class JobResultSchema(BaseModel):
    job_id: int
    miner_wallet: str
    computer_name: str
    computer_uuid: str
    gpu_uuid: str
    hash_rate: int
    boc: str


class GPUWorkerSchema(BaseModel):
    job: Optional[JobSchema]
    gpu_id: int
    boost_factor: int = 16
    timeout: int = 900
    boc_name: str = "mined_default.boc"
    miner_wallet: str
    computer_name: str
    computer_uuid: str

    def _cmd(self):
        cmd = f"-vv -g{self.gpu_id} -F{self.boost_factor} -t{self.timeout} "
        cmd += f"{self.job.pool_wallet} {self.job.seed} {self.job.complexity} {self.job.iterations} "
        cmd += f"{self.job.giver_address} {self.boc_name}"
        return cmd

    def _add_job(self, job: JobSchema) -> JobResultSchema:
        self.job = job

    def _generate_job_result(self):
        contexts = ''
        with open(self.boc_name, 'r') as f:
            contexts = f.read()

        result = JobResultSchema(
            job_id=self.job.job_id,
            miner_wallet=self.miner_wallet,
            computer_name=self.computer_name,
            computer_uuid=self.computer_uuid,
            gpu_uuid=self.gpu_id,
            hash_rate=666,
            boc=contexts,
        )
        return result


class MinerSchema(BaseModel):
    pool_url: str
    miner_wallet: str
    computer_name: str = platform.node()
    computer_uuid: str = hex(uuid.getnode())  # mac address
    devices: List[str]
    gpus: List[str]
    workers: Optional[List[GPUWorkerSchema]]

    def _create_wokers(self) -> List[GPUWorkerSchema]:
        self.workers = [GPUWorkerSchema(
            gpu_id=gpu,
            miner_wallet=self.miner_wallet,
            computer_name=self.computer_name,
            computer_uuid=self.computer_uuid,
            boc_name=f"mined-{gpu}.boc")
            for gpu in self.gpus]

        return self.workers
