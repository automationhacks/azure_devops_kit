# Azure DevOps Kit

A Python CLI tool for managing and analyzing test cases in Azure DevOps.

## Features

- Fetch test cases from Azure DevOps based on custom queries
- Identify and categorize test cases as automated, manual, or automatable
- Generate daily aggregation reports in CSV format
- Create trend visualizations for test case automation status

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/azure-devops-kit.git
cd azure-devops-kit
```

2. Install using Poetry:

```bash
poetry install
```

## Usage

### Get Test Cases

```bash
poetry run azdo-kit get-test-cases \
    --organization "your-org" \
    --project "your-project" \
    --pat "your-pat" \
    --query "your-query"
```

### Aggregate Test Cases

```bash
poetry run azdo-kit aggregate-cases \
    --organization "your-org" \
    --project "your-project" \
    --pat "your-pat" \
    --output "test_cases.csv"
```

### Plot Trends

```bash
poetry run azdo-kit plot-trend \
    --input "test_cases.csv" \
    --output "trend.png"
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Running with Coverage

```bash
poetry run pytest --cov=azure_devops_kit
```

## License

This project is licensed under the terms of the included LICENSE file.
