# ParameterFrame

<a><img src="https://github.com/Kiril-Mordan/ParameterFrame/blob/main/docs/parameterframe_logo.png" width="35%" height="35%" align="right" /></a>

This provides an interface for managing solution parameters. It allows for structured storage and retrieval of parameter sets from a given database. The goal is to have a simple and rudamentory way to organize centralized configuration file storage for multiple solutions at the same time within any kind of available storage solution. More related to `parameterframe` could be seen [here](https://github.com/Kiril-Mordan/reusables).

## Run locally

Use underlying python package from [pypi](https://pypi.org/project/parameterframe/):
```
pip install parameterframe
```

Run API locally:
```
git clone https://github.com/Kiril-Mordan/ParameterFrame.git
cd ParameterFrame
uvicorn main:app --port 8000
```


## Run from pre-built Docker image:

```
docker pull kyriosskia/parameterframe:latest
docker run -p 8000:8080 -e DATABASE_URL='postgresql://user:password@localhost/dbname' -e ACCESS_KEY='your_access_key_value' -e DB_ACCESS_KEY='access_key' kyriosskia/parameterframe:latest
```

  - DATABASE_URL : connection string for database
  - ACCESS_KEY : key to access endpoints
  - DB_ACCESS_KEY : key to reset schema if databases that allow it


# API Endpoints


### Read Root

- **Method**: GET
- **URL**: `/`
- **Description**: No description provided.
- **Response 200 (application/json)**: Successful Response
  ```json
  {}
  ```


### Set Reset Schema

- **Method**: POST
- **URL**: `/set_reset_schema`
- **Description**: For databases that require predefined schema, drops tables and sets up new schema.
- **Response 200 (application/json)**: Success status
  ```json
  {
    "outcome_success": true
  }
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Declare Solution

- **Method**: POST
- **URL**: `/declare_solution`
- **Description**: Provide basic description of new solution.
- **Request Body (application/x-www-form-urlencoded)**:
  ```json
  {
    "solution_name": "example_solution_name",
    "solution_description": "example_solution_description",
    "deployment_date": "example_deployment_date",
    "deprecation_date": "example_deprecation_date",
    "maintainers": "example_maintainers"
  }
  ```
- **Response 200 (application/json)**: solution id for new solution
  ```json
  {
    "solution_id": "cec89c4cbb8c891d388407ea93d84a5cd4f996af6d5c1b0cc5fe1cb12101acf5"
  }
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Upload Parameter Set

- **Method**: POST
- **URL**: `/upload_parameter_set`
- **Description**: Upload files for parameter set and assign the to already declared solution.
- **Request Body (multipart/form-data)**:
  ```json
  {
    "files": "example_files",
    "solution_id": "example_solution_id",
    "parameter_set_name": "example_parameter_set_name",
    "parameter_set_description": "example_parameter_set_description"
  }
  ```
- **Response 200 (application/json)**: parameters set id of newly created parameter set
  ```json
  {
    "parameter_set_id": "5779bbf896ebb8f09a6ea252b09f8adb1a416e8780cf1424fb9bb93dbec8deb5"
  }
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Get Latest Parameter Set Id

- **Method**: POST
- **URL**: `/get_latest_parameter_set_id`
- **Description**: Get parameter set ids for a given solution and deployment status, since newly defined are marked with STAGING, it is used by default.
- **Request Body (application/x-www-form-urlencoded)**:
  ```json
  {
    "solution_id": "example_solution_id",
    "deployment_status": "example_deployment_status"
  }
  ```
- **Response 200 (application/json)**: List of parameter set ids for solution and deployment status
  ```json
  {
    "parameter_set_id": [
      "5779bbf896ebb8f09a6ea252b09f8adb1a416e8780cf1424fb9bb93dbec8deb5"
    ]
  }
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Change Status From Staging To Production

- **Method**: POST
- **URL**: `/change_status_from_staging_to_production`
- **Description**: Change deployment status of select parameter set from staging to production.
- **Request Body (application/x-www-form-urlencoded)**:
  ```json
  {
    "solution_id": "example_solution_id",
    "parameter_set_id": "example_parameter_set_id"
  }
  ```
- **Response 200 (application/json)**: Success status
  ```json
  {
    "outcome_success": true
  }
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Change Status From Production To Archived

- **Method**: POST
- **URL**: `/change_status_from_production_to_archived`
- **Description**: Change deployment status of select parameter set from production to archived.
- **Request Body (application/x-www-form-urlencoded)**:
  ```json
  {
    "solution_id": "example_solution_id",
    "parameter_set_id": "example_parameter_set_id"
  }
  ```
- **Response 200 (application/json)**: Success status
  ```json
  {
    "outcome_success": true
  }
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Change Status From Archived Production

- **Method**: POST
- **URL**: `/change_status_from_archived_production`
- **Description**: Change deployment status of select parameter set from archived to production.
- **Request Body (application/x-www-form-urlencoded)**:
  ```json
  {
    "solution_id": "example_solution_id",
    "parameter_set_id": "example_parameter_set_id"
  }
  ```
- **Response 200 (application/json)**: Success status
  ```json
  {
    "outcome_success": true
  }
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Change Deployment Status

- **Method**: POST
- **URL**: `/change_deployment_status`
- **Description**: Change deployment status of select parameter set from existing status to new status.
- **Request Body (application/x-www-form-urlencoded)**:
  ```json
  {
    "solution_id": "example_solution_id",
    "parameter_set_id": "example_parameter_set_id",
    "current_deployment_status": "example_current_deployment_status",
    "new_deployment_status": "example_new_deployment_status"
  }
  ```
- **Response 200 (application/json)**: Success status
  ```json
  {
    "outcome_success": true
  }
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Show Solutions

- **Method**: POST
- **URL**: `/show_solutions`
- **Description**: Show description of all solutions in parameter storage
- **Response 200 (application/json)**: List of parameter set ids for solution and deployment status
  ```json
  [
    {
      "solution_id": "cec89c4cbb8c891d388407ea93d84a5cd4f996af6d5c1b0cc5fe1cb12101acf5",
      "solution_name": "new_example_solution",
      "solution_description": "Description of new example solution.",
      "deployment_date": "2024-xx-xx",
      "maintainers": "some text about maintainers credentials",
      "commited_parameter_sets": 6,
      "aos": 0.397157,
      "pos": 0.428571
    }
  ]
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Show Parameter Sets

- **Method**: POST
- **URL**: `/show_parameter_sets`
- **Description**: Show description of all or select parameter set for a given solution.
- **Request Body (application/x-www-form-urlencoded)**:
  ```json
  {
    "solution_id": "example_solution_id",
    "parameter_set_id": "example_parameter_set_id"
  }
  ```
- **Response 200 (application/json)**: List of parameter set ids for solution and deployment status
  ```json
  {
    "response": [
      {
        "parameter_set_id": "82b8c5340454adf83667e59092fedbee28213475fd58ab6b3d95b4fc60f4d45f",
        "parameter_set_name": "purple_giant_television_135",
        "parameter_set_description": "",
        "deployment_status": "STAGING",
        "insertion_datetime": "2024-05-16 00:05:43",
        "commited_parameters": 1,
        "aos": 0.371413,
        "pos": 0.142857
      },
      {
        "parameter_set_id": "2f3ee8e19d91a89298d40984df5e7bdd1f1a48008b2e61c88a7f6f81b4ab23f5",
        "parameter_set_name": "silver_happy_car_441",
        "parameter_set_description": "",
        "deployment_status": "STAGING",
        "insertion_datetime": "2024-05-16 00:03:25",
        "commited_parameters": 1,
        "aos": 0.0,
        "pos": 0.0
      }
    ]
  }
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Show Parameters

- **Method**: POST
- **URL**: `/show_parameters`
- **Description**: Show description of all select parameters for a given solution id and parameter set id.
- **Request Body (application/x-www-form-urlencoded)**:
  ```json
  {
    "solution_id": "example_solution_id",
    "parameter_set_id": "example_parameter_set_id"
  }
  ```
- **Response 200 (application/json)**: List of parameter set ids for solution and deployment status
  ```json
  {
    "response": [
      {
        "parameter_set_id": "82b8c5340454adf83667e59092fedbee28213475fd58ab6b3d95b4fc60f4d45f",
        "parameter_set_name": "purple_giant_television_135",
        "parameter_set_description": "",
        "deployment_status": "STAGING",
        "insertion_datetime": "2024-05-16 00:05:43",
        "commited_parameters": 1,
        "aos": 0.0
      },
      {
        "parameter_set_id": "2f3ee8e19d91a89298d40984df5e7bdd1f1a48008b2e61c88a7f6f81b4ab23f5",
        "parameter_set_name": "silver_happy_car_441",
        "parameter_set_description": "",
        "deployment_status": "STAGING",
        "insertion_datetime": "2024-05-16 00:03:25",
        "commited_parameters": 1,
        "aos": 0.0
      }
    ]
  }
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```


### Download Parameter Set

- **Method**: POST
- **URL**: `/download_parameter_set`
- **Description**: Download files from a given parameter set.
- **Request Body (application/x-www-form-urlencoded)**:
  ```json
  {
    "solution_id": "example_solution_id",
    "parameter_set_id": "example_parameter_set_id"
  }
  ```
- **Response 200 (application/json)**: File successfully downloaded
  ```json
  {}
  ```

- **Response 422 (application/json)**: Validation Error
  ```json
  {
    "detail": "example_detail"
  }
  ```

