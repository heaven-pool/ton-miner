# # -*- coding: utf-8 -*-
# import os
# from pathlib import Path

# from app import models

# ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
# DATA_DIR = Path(BASE_DIR, 'data')


# def test_miner_model():

#     config_file = Path(DATA_DIR, "miner.json")
#     model_data = models.MinerSchema.parse_file(config_file)

#     assert model_data.pool_wallet == b"EQB6UzwFx-gZTIZmJmiFWZ7_qTIZ9RwBaR1_2IPtKR4UuAoJ"
#     assert model_data.miner_wallet == b"EQDv9eExabxeFmiPigOE_NscTo_SXB9IwDXz975hPWjO_cGq"
#     assert model_data.computer_uuid == b"0x1e0062221865"
#     assert "1" in model_data.GPUs
