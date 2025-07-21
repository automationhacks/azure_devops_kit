"""Command line interface for Azure DevOps Kit."""
import click
from datetime import datetime
from .test_case_manager import TestCaseManager

@click.group()
def main():
    """Azure DevOps Kit CLI tool."""
    pass

@main.command()
@click.option('--organization', '-o', required=True, help='Azure DevOps organization name')
@click.option('--project', '-p', required=True, help='Azure DevOps project name')
@click.option('--pat', required=True, help='Personal Access Token for Azure DevOps')
@click.option('--query', '-q', help='Query to filter test cases')
def get_test_cases(organization, project, pat, query):
    """Get all test cases matching the specified query."""
    manager = TestCaseManager(organization, project, pat)
    test_cases = manager.get_test_cases(query)
    click.echo(test_cases)

@main.command()
@click.option('--organization', '-o', required=True, help='Azure DevOps organization name')
@click.option('--project', '-p', required=True, help='Azure DevOps project name')
@click.option('--pat', required=True, help='Personal Access Token for Azure DevOps')
@click.option('--output', '-out', default='test_cases.csv', help='Output CSV file path')
def aggregate_cases(organization, project, pat, output):
    """Aggregate test cases by automation status and save to CSV."""
    manager = TestCaseManager(organization, project, pat)
    manager.aggregate_test_cases(output)
    click.echo(f"Test cases aggregated and saved to {output}")

@main.command()
@click.option('--input', '-i', required=True, help='Input CSV file with test case data')
@click.option('--output', '-o', default='trend.png', help='Output plot file path')
def plot_trend(input, output):
    """Plot test case automation trend from CSV data."""
    manager = TestCaseManager(None, None, None)  # No Azure DevOps connection needed for plotting
    manager.plot_trend(input, output)
    click.echo(f"Trend plot saved to {output}")

if __name__ == '__main__':
    main()
