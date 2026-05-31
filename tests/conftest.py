import pytest 

@pytest.fixture
def typical_c_antenna():
    """A typical C-band antenna"""
    return {
        "diameter_m": 2.4,
        "frequency_ghz": 4.0,
        "efficiency": 0.65,
    }

@pytest.fixture
def typical_ku_antenna():
    """A typical Ku-band antenna"""
    return {
        "diameter_m": 1.2,
        "frequency_ghz": 12.0,
        "efficiency": 0.65,
    }

@pytest.fixture
def typical_link():
    """A typical LBA"""
    return {
        "eirp_dbw": 57.2,
        "fspl_db": 165.6,
        "g_over_t_db_k": 22.97,
        "bandwidth_hz": 36e6,
    }
