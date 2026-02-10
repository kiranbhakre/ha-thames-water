import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield

@pytest.fixture
def mock_thames_water_client():
    """Mock the ThamesWater client."""
    with patch("custom_components.thames_water.thameswaterclient.ThamesWater") as mock_client:
        instance = mock_client.return_value
        yield instance
