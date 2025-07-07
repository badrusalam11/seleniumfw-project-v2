from seleniumfw.runner import Runner
from seleniumfw.config import Config

def run():
    runner = Runner()
    config = Config()
    print(config.get('environment'))
    runner.run_feature("include/features/login.feature")
