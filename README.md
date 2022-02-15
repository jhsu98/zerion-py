# zerion-py (zerionAPI)

The zerionAPI project is an open-source effort to simplify and standardize integrations with the various services offered by Zerion Software. Written in Python, zerionAPI lets you start working with the iFormBuilder or Dataflow Automation API in minutes. No experience necessary.

zerionAPI is also the successor to the ifb-wrapper library which only support iFormBuilder and was restricted to version 6.0 of the API.

## Installation
To install zerionAPI, ensure you have Python 3.0+ installed. Download using the following command:
```
pip install zerionAPI
```
*Note: If you are on MacOS you may need to use the command `pip3` due to Python 2.7 also being installed.*

## Getting Started
To start a new project, import the specific service(s) you want to interact with. We'll import both the iFormBuilder and Dataflow Automation services in our example below.
```python
from zerionAPI import IFB, DFA
```
To connect to a service, create a new object by supplying three values: server name, client key, client secret. There is a fourth optional value (params) which is used to further customize the connection.
```python
from zerion API import IFB, DFA

ifb = IFB('myserver', '**client_key_goes_here**', '**client_secret_goes_here**')
```
That's it! The zerionAPI library will automatically request an access token with your credentials and has functions to interact with every available resource.

For more information on creating a Zerion API App please contact your Customer Success Manager

For more information on creating an iFormBuilder-only API app please visit: https://iformbuilder.zendesk.com/hc/en-us/articles/201702900-What-are-the-API-Apps-Start-Here-
### Customization through Params
To use the params configuration, pass a dictionary with the appropriate key-value pairs to modify your API connection. Below is a table of options, the service(s) they apply to, and their default values.

|Option|Service|Default|
|------|-------|-------|
|rate_limit_retry | All | False|
|isQA|All|False|
|version|IFB|8.0|

## Structuring Requests
The zerionAPI library is organized by the specific resources available. Every method requires the REST method as the first argument followed by required values then optional values. Each method will return an API_Response object which has three properties (headers, status_code, and response).

Let's take a look at an example API call to retrieve all profiles in an iFormBuilder environment and print the status code of the request.
```python
from zerionAPI import IFB

ifb = IFB('myserver', '**client_key_goes_here**', '**client_secret_goes_here**')

result = ifb.Profiles('GET')
print(result.status_code) # 200
```
What if we want to retrieve data about a specific profile? We use the same resource method, but include the optional value for profile id in our request.
```python
result = ifb.Profiles('GET', 12345)
```
Since profiles is the top-level resource in the iFormBuilder hierarchy, no additional parameters are needed. Let's try another API call to retrieve information about a specific user id. Note that the profile id value is required (users belong to a profile) but the user id value is technically optional.
```python
profile_id = 12345
user_id = 67890
result = ifb.Users('GET', profile_id, user_id)
```
Instead of a specific user, what if we want to query users based on field grammar?
```python
result = ifb.Users('GET', 12345, params={'fields': 'username(="jhsu98")'})
```
The previous example would retrieve all users within the profile 12345 who have a username that equals jhsu98.

## Utility Functions
Both IFB and DFA classes have companion helper functions to simply tasks and extend the functionality of the library. Use the following import statement for the utility functions.
```python
from zerionAPI import dfa_utilities, ifb_utilities
```
Note that all utility functions require a valid Class object as the first argument. Below is a list of functions in each utility.
|Service|Function|Description|
|------|-------|-------|
|IFB | `exportImages(api, profile_id, page_id, isRecursive=False, directory = '.')` | Exports all image and drawing fields from a page. Recursive and directory configurations are optional|
|DFA|`copyDataflow(api, dataflow_id, new_dataflow_name)` |Copies a Dataflow using the supplied name for new Dataflow|

## Changelog
- v0.0.6: February 15, 2022
  - Added `ActionErrors()` method to DFA
  - Added `RerunActionErrors()` method to DFA
  - Fixed issue building param list in DFA library
- v0.0.5: February 4, 2022
  - Added Boolean param `ifb_api_credentials`, which is defaulted to False and needs to be set to True when using IFB issued API app credentials
  - Added String param `region`, which is defaulted to 'us' and needs to be set to 'hipaa', 'uk' or 'au' based on data center. Use 'qa' for sandbox environments.
- v0.0.4: January 8, 2022
  - Added `DataflowCount()` method to DFA
  - Added ifb utility function `exportImages()`
  - Added dfa utility function `copyDataflow()`
- v0.0.3: January 3, 2022
  - Added `getParams()` method to API
  - Added `getVersion()` method to IFB
  - Begun unit testing
- v0.0.2: January 2, 2022
  - Modified `API` class to be abstract base class
  - Added `URI` to __resources for IFB and DFA
  - Added `describeResources()` and `describeResource(resource)` to IFB & DFA
  - Added `Events` resource to DFA
  - Fixed issue with `__repr__` returning int
- v0.0.1: January 1, 2022