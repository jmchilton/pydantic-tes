import pytest

from pydantictes.funnelfixture import funnel_client


tes_funnel_client = pytest.fixture(scope="module")(funnel_client)
