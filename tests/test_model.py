# # -*- coding: utf-8 -*-
# import os
# from pathlib import Path

from app.libs import models


def test_miner_model():
    obj1 = models.JobSchema(
        job_id=661422, pool_wallet='EQDv9eExabxeFmiPigOE_NscTo_SXB9IwDXz975hPWjO_cGq',
        complexity='1906156863157627903919216023423475890402376096793739878410580',
        seed='328574290144741374257957134907128616586', iterations='100000000000',
        giver_address='kf-P_TOdwcCh0AXHhBpICDMxStxHenWdLCDLNH5QcNpwMHJ8',)

    obj2 = models.JobSchema(
        job_id=661422, pool_wallet='EQDv9eExabxeFmiPigOE_NscTo_SXB9IwDXz975hPWjO_cGq',
        complexity='1906156863157627903919216023423475890402376096793739878410580',
        seed='328574290144741374257957134907128616586', iterations='100000000000',
        giver_address='kf-P_TOdwcCh0AXHhBpICDMxStxHenWdLCDLNH5QcNpwMHJ8',)

    assert obj1.create_at != obj2.create_at
