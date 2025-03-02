import pytest
from alfred.utils.common import perform_search

def test_perform_search_not_none():
    query = "NVDA current stock price?"
    result = perform_search(query)
    assert result is not None  # Check that the result is not None

if __name__ == '__main__':
    pytest.main()