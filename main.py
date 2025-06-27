from futurehouse_client import FutureHouseClient, JobNames
from pathlib import Path
from aviary.core import DummyEnv
import ldp

client = FutureHouseClient(
    api_key="your_api_key",
)

task_data = {
    "name": JobNames.CROW,
    "query": "Which neglected diseases had a treatment developed by artificial intelligence?",
}

task_response = client.run_tasks_until_done(task_data)