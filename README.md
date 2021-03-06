#### PyHamcrest matchers extension for json schema validation

The schema should be implemented following syntax of [Draft-07 to 2019-09](https://json-schema.org/draft-07/json-schema-release-notes.html) version.
Schema example:
```python
single_user_schema = {
    "title": "Single User Info",
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string",
            "minLength": 3
        },
        "last_name": {
            "type": "string",
            "minLength": 3
        },
        "phone_number": {
            "type": "number"
        }
    },
    "required": [
        "first_name",
        "last_name",
    ]
}

all_users_info_schema = {
    "title": "All Users Info",
    "type": "array",
    "items": single_user_schema
}
```
Then you can use `matches_json_schema` matcher with all hamcrest matchers:
```python
from hamcrest import assert_that
from json_schema_matchers.common_matcher import matches_json_schema

users_list_json_obj = [
    {
        "first_name": 'John',
        "last_name": "Johnson",
        "phone_number": 123456789
    },
    {
        "first_name": 'Jim',
        "last_name": 'Jefferson'
    }
]

assert_that(users_list_json_obj, matches_json_schema(all_users_info_schema))

assert_that(users_list_json_obj[0], matches_json_schema(single_user_schema))
```
In case of validation fail the matcher will return all mismatches iteratively:

```python
users_list_json_obj = [
    {
        "first_name": 'John',
        "last_name": "Johnson",
        "phone_number": '123456789'
    },
    {
        "first_name": None,
        "last_name": 'Je'
    }
]

assert_that(users_list_json_obj, matches_json_schema(all_users_info_schema))
```
```json
AssertionError: 
Expected: 
     JSON object should match schema "All Users Info"
     but: 
     mismatches occurred: 

'123456789' is not of type 'number'

Failed validating 'type' in schema['items']['properties']['phone_number']:
    {'type': 'number'}

On instance[0]['phone_number']:
    '123456789'

------------
'Je' is too short

Failed validating 'minLength' in schema['items']['properties']['last_name']:
    {'minLength': 3, 'type': 'string'}

On instance[1]['last_name']:
    'Je'

------------
None is not of type 'string'

Failed validating 'type' in schema['items']['properties']['first_name']:
    {'minLength': 3, 'type': 'string'}

On instance[1]['first_name']:
    None

------------
```
#### Dependencies:
```requirements.txt
jsonschema==3.2.0
PyHamcrest==2.0.2
```