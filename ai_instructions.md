# Build an azure dev ops kit that provides helpful utilities

## Task

Build an azure dev ops python CLI that is able to perform below operations using Azure dev ops API

- Get all the test cases in an organization that satisfy a certain query
- Identify a case has automated, manual or automatable and aggregate the counts daily and store in a CSV file
- Plot a graph explaining the trend of test cases by these three categories

## Steps

- You should make Azure API calls and fetch the list of test cases
- You should output a json output like below:

```json
{
    "date": "2025-07-21T00:00:00.000Z"
    "automated": [{"TC1234": "/MSTeams/Foo"}, ...]
    "manual": [{"TC1236": "/MSTeams/Bar"} ...]
    "automatable": [{"TC1237": "/MSTeams/FooBar"}]
}
```

- Next you should compute the total count and prepare a JSON like below, where key is the area path and value is a dict with counts of each cases

```json
{
    "/MSTeams/Foo": {"automated": 25, "manual": 5, "automatable": 10}
}
```
