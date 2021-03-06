# -*- coding: utf-8 -*-s
import platform
import time
import uuid
from pathlib import Path
from typing import List, Optional

from libs import utils
from pydantic import BaseModel, Field
from typing_extensions import Annotated

# Miner -> create GPUWorker
# Job + GPUWorker -> JobResult

APP_ROOT_PATH = Path(__file__).parent.resolve()


class JobSchema(BaseModel):
    create: Annotated[float, Field(default_factory=lambda: time.time())]
    job_id: int
    pool_wallet: str
    complexity: str
    seed: str
    iterations: str
    giver_address: str


class JobResultSchema(BaseModel):
    create: float
    update: float
    job_id: int
    miner_wallet: str
    computer_name: str
    computer_uuid: str
    gpu_uuid: str
    hash_rate: float  # MHz
    boc: str


class GPUWorkerSchema(BaseModel):
    job: Optional[JobSchema]
    gpu_id: int
    gpu_device: str
    boost_factor: int = 1024
    timeout: int = 900
    boc_name: str = "mined_default.boc"
    miner_wallet: str
    computer_name: str
    computer_uuid: str

    @property
    def _cmd(self) -> str:
        cmd = f"-vv -g{self.gpu_id} -F{self.boost_factor} -t{self.timeout} "
        cmd += f"{self.job.pool_wallet} {self.job.seed} {self.job.complexity} {self.job.iterations} "
        cmd += f"{self.job.giver_address} {self.boc_name}"
        return cmd

    def _add_job(self, job: JobSchema) -> JobResultSchema:
        self.job = job

    def _generate_job_result(self, hash_rate):
        contexts = utils.readfile_to_hexstring(self.boc_name)
        result = JobResultSchema(
            create=self.job.create,
            update=time.time(),
            job_id=self.job.job_id,
            miner_wallet=self.miner_wallet,
            computer_name=self.computer_name,
            computer_uuid=self.computer_uuid,
            gpu_uuid=self.gpu_id,
            hash_rate=hash_rate,
            boc=contexts,
        )
        return result


class MinerSchema(BaseModel):
    pool_url: str
    miner_wallet: str
    computer_name: str = platform.node()
    computer_uuid: str = str(uuid.UUID(int=uuid.getnode()))  # mac address
    devices: List[str]
    gpus: List[str]
    workers: Optional[List[GPUWorkerSchema]]

    # why not init?
    def _create_wokers(self) -> List[GPUWorkerSchema]:
        self.workers = [
            GPUWorkerSchema(
                gpu_id=gpu,
                gpu_device=device,
                miner_wallet=self.miner_wallet,
                computer_name=self.computer_name,
                computer_uuid=self.computer_uuid,
                boc_name=str(Path(APP_ROOT_PATH, f"mined-{gpu}.boc")),
            )
            for gpu, device in zip(self.gpus, self.devices)
        ]
        return self.workers
