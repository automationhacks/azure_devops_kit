"""Tests for the TestCaseManager class."""
import json
import pytest
from unittest.mock import Mock, patch
from azure_devops_kit.test_case_manager import TestCaseManager

@pytest.fixture
def mock_azure_devops():
    """Create mock Azure DevOps client."""
    with patch('azure_devops_kit.test_case_manager.Connection') as mock_connection:
        mock_client = Mock()
        mock_connection.return_value.clients.get_work_item_tracking_client.return_value = mock_client
        yield mock_client

def test_get_test_cases(mock_azure_devops):
    """Test getting test cases."""
    # Mock work items
    mock_work_item1 = Mock(id=1234)
    mock_work_item1.fields = {
        "Microsoft.VSTS.TCM.AutomationStatus": "Automated",
        "System.AreaPath": "/MSTeams/Foo"
    }
    
    mock_work_item2 = Mock(id=1236)
    mock_work_item2.fields = {
        "Microsoft.VSTS.TCM.AutomationStatus": "Not Automated",
        "System.AreaPath": "/MSTeams/Bar"
    }

    # Set up mock responses
    mock_azure_devops.query_by_wiql.return_value.work_items = [
        Mock(id=1234),
        Mock(id=1236)
    ]
    mock_azure_devops.get_work_item.side_effect = [mock_work_item1, mock_work_item2]

    # Create manager and get test cases
    manager = TestCaseManager("org", "project", "pat")
    result = json.loads(manager.get_test_cases())

    # Verify results
    assert len(result["automated"]) == 1
    assert len(result["manual"]) == 1
    assert result["automated"][0] == {"TC1234": "/MSTeams/Foo"}
    assert result["manual"][0] == {"TC1236": "/MSTeams/Bar"}

def test_aggregate_test_cases(mock_azure_devops, tmp_path):
    """Test aggregating test cases."""
    # Mock get_test_cases response
    test_cases = {
        "date": "2025-07-21T00:00:00.000Z",
        "automated": [{"TC1234": "/MSTeams/Foo"}],
        "manual": [{"TC1236": "/MSTeams/Foo"}],
        "automatable": [{"TC1237": "/MSTeams/Foo"}]
    }

    manager = TestCaseManager("org", "project", "pat")
    with patch.object(manager, 'get_test_cases', return_value=json.dumps(test_cases)):
        output_file = tmp_path / "test_output.csv"
        result = json.loads(manager.aggregate_test_cases(str(output_file)))

        assert result["/MSTeams/Foo"] == {
            "automated": 1,
            "manual": 1,
            "automatable": 1
        }

def test_plot_trend(tmp_path):
    """Test plotting trends."""
    # Create test CSV data
    test_data = """AreaPath,automated,manual,automatable
/MSTeams/Foo,25,5,10"""
    
    input_file = tmp_path / "test_input.csv"
    output_file = tmp_path / "test_output.png"
    
    with open(input_file, "w") as f:
        f.write(test_data)

    manager = TestCaseManager(None, None, None)
    manager.plot_trend(str(input_file), str(output_file))

    assert output_file.exists()
