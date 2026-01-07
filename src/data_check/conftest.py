import os

import pandas as pd
import pytest
import wandb


def pytest_addoption(parser):
    parser.addoption("--csv", action="store")
    parser.addoption("--ref", action="store")
    parser.addoption("--kl_threshold", action="store")
    parser.addoption("--min_price", action="store")
    parser.addoption("--max_price", action="store")


def _download_csv(run, artifact_name: str) -> str:
    if artifact_name is None:
        pytest.fail("You must provide the --csv/--ref option on the command line")

    artifact = run.use_artifact(artifact_name)

    # IMPORTANT: use a Windows-safe root folder (avoid ':' in paths like ':latest')
    artifact_dir = artifact.download(root="wandb_artifacts")

    for fname in os.listdir(artifact_dir):
        if fname.lower().endswith(".csv"):
            return os.path.join(artifact_dir, fname)

    pytest.fail(f"No CSV found in artifact {artifact_name}")


@pytest.fixture(scope="session")
def data(request):
    run = wandb.init(job_type="data_tests", resume=True)
    data_path = _download_csv(run, request.config.option.csv)
    return pd.read_csv(data_path)


@pytest.fixture(scope="session")
def ref_data(request):
    run = wandb.init(job_type="data_tests", resume=True)
    data_path = _download_csv(run, request.config.option.ref)
    return pd.read_csv(data_path)


@pytest.fixture(scope="session")
def kl_threshold(request):
    if request.config.option.kl_threshold is None:
        pytest.fail("You must provide a threshold for the KL test")
    return float(request.config.option.kl_threshold)


@pytest.fixture(scope="session")
def min_price(request):
    if request.config.option.min_price is None:
        pytest.fail("You must provide min_price")
    return float(request.config.option.min_price)


@pytest.fixture(scope="session")
def max_price(request):
    if request.config.option.max_price is None:
        pytest.fail("You must provide max_price")
    return float(request.config.option.max_price)
