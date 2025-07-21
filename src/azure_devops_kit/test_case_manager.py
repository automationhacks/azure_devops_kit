"""Test case management and analysis functionality."""
import json
from datetime import datetime
from azure.devops.connection import Connection
from azure.devops.v7_1.work_item_tracking.models import Wiql
import pandas as pd
import matplotlib.pyplot as plt

class TestCaseManager:
    """Manages test cases in Azure DevOps."""

    def __init__(self, organization, project, pat):
        """Initialize with Azure DevOps credentials."""
        self.organization = organization
        self.project = project
        if organization and project and pat:
            organization_url = f"https://dev.azure.com/{organization}"
            self.connection = Connection(base_url=organization_url, creds=pat)
            self.client = self.connection.clients.get_work_item_tracking_client()

    def get_test_cases(self, query=None):
        """Get test cases based on query."""
        if not query:
            query = """
            SELECT [System.Id]
            FROM WorkItems
            WHERE [System.WorkItemType] = 'Test Case'
            ORDER BY [System.Id]
            """

        wiql = Wiql(query=query)
        results = self.client.query_by_wiql(wiql).work_items

        test_cases = {}
        test_cases["date"] = datetime.utcnow().isoformat()
        test_cases["automated"] = []
        test_cases["manual"] = []
        test_cases["automatable"] = []

        for result in results:
            work_item = self.client.get_work_item(result.id)
            automation_status = work_item.fields.get("Microsoft.VSTS.TCM.AutomationStatus", "")
            area_path = work_item.fields["System.AreaPath"]
            
            item = {f"TC{work_item.id}": area_path}
            
            if automation_status.lower() == "automated":
                test_cases["automated"].append(item)
            elif automation_status.lower() == "planned":
                test_cases["automatable"].append(item)
            else:
                test_cases["manual"].append(item)

        return json.dumps(test_cases, indent=2)

    def aggregate_test_cases(self, output_file):
        """Aggregate test cases by area path and automation status."""
        test_cases = json.loads(self.get_test_cases())
        
        aggregated = {}
        
        for status in ["automated", "manual", "automatable"]:
            for item in test_cases[status]:
                for _, area_path in item.items():
                    if area_path not in aggregated:
                        aggregated[area_path] = {"automated": 0, "manual": 0, "automatable": 0}
                    aggregated[area_path][status] += 1

        # Convert to DataFrame and save to CSV
        df = pd.DataFrame.from_dict(aggregated, orient='index')
        df.to_csv(output_file)
        
        return json.dumps(aggregated, indent=2)

    def plot_trend(self, input_file, output_file):
        """Plot trend of test case automation status."""
        df = pd.read_csv(input_file)
        
        # Create stacked bar chart
        ax = df.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title('Test Case Automation Status by Area Path')
        plt.xlabel('Area Path')
        plt.ylabel('Number of Test Cases')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(output_file)
        plt.close()
