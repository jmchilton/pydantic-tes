import os
import time

from .api import TesClient
from .funnelwrapper import FunnelServer


def funnel_client():
    """A ready made fixture for deploying and testing against funnel.

    This can be deployed by setting a conftest.py in your test directory
    with the following line.

    tes_funnel_client = pytest.fixture(scope="module")(funnel_client)
    """
    funnel_server_target = os.environ.get(
        "FUNNEL_SERVER_TARGET", "http://localhost:8000"
    )
    if funnel_server_target == "DEPLOY":
        server = FunnelServer()
        server.start()
        # sleep some to wait for the server to start...
        # todo poll...
        time.sleep(5)
        client = TesClient(url="http://localhost:8000")
        yield client
        server.stop()
    else:
        client = TesClient(url=funnel_server_target)
        yield client
