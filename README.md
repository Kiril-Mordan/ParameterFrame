# ParameterFrame

<a><img src="https://github.com/Kiril-Mordan/ParameterFrame/blob/main/docs/parameterframe_logo.png" width="35%" height="35%" align="right" /></a>

This provides an interface for managing solution parameters. It allows for the structured storage and retrieval of parameter sets from a given database. The goal is to have a simple and rudamentory way to organize centralized configuration files storage for multiple solutions at the same times within any kind of available storage solution. More related to `parameterframe` could be seen [here](https://github.com/Kiril-Mordan/reusables).

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

Access localhost at http://127.0.0.1:8000

## Run from pre-built Docker image:

```
docker pull kyriosskia/parameterframe:latest
docker run -p 8000:8080 kyriosskia/parameterframe:latest
```

then access at http://localhost:8000

# API Endpoints


### Read Root

- **Method**: GET
- **URL**: `/`
- **Description**: No description provided.
- **Response 200**: Successful Response
  ```json
  {}
  ```


### Declare Solution

- **Method**: POST
- **URL**: `/declare_solution`
- **Description**: No description provided.
- **Request Body**:
  ```json
  {}
  ```
- **Response 200**: Successful Response
  ```json
  {}
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Upload Files

- **Method**: POST
- **URL**: `/upload_parameter_set`
- **Description**: No description provided.
- **Request Body**:
  ```json
  {}
  ```
- **Response 200**: Successful Response
  ```json
  {}
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Get Latest Parameter Set Id

- **Method**: POST
- **URL**: `/get_latest_parameter_set_id`
- **Description**: No description provided.
- **Request Body**:
  ```json
  {}
  ```
- **Response 200**: Successful Response
  ```json
  {}
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Show Parameters

- **Method**: POST
- **URL**: `/change_status_from_staging_to_production`
- **Description**: No description provided.
- **Request Body**:
  ```json
  {}
  ```
- **Response 200**: Successful Response
  ```json
  {}
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Show Parameters

- **Method**: POST
- **URL**: `/change_status_from_production_to_archived`
- **Description**: No description provided.
- **Request Body**:
  ```json
  {}
  ```
- **Response 200**: Successful Response
  ```json
  {}
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Show Parameters

- **Method**: POST
- **URL**: `/change_status_from_archived_production`
- **Description**: No description provided.
- **Request Body**:
  ```json
  {}
  ```
- **Response 200**: Successful Response
  ```json
  {}
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Show Parameters

- **Method**: POST
- **URL**: `/change_deployment_status`
- **Description**: No description provided.
- **Request Body**:
  ```json
  {}
  ```
- **Response 200**: Successful Response
  ```json
  {}
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Show Solutions

- **Method**: POST
- **URL**: `/show_solutions`
- **Description**: No description provided.
- **Response 200**: Successful Response
  ```json
  {}
  ```


### Show Parameter Sets

- **Method**: POST
- **URL**: `/show_parameter_sets`
- **Description**: No description provided.
- **Request Body**:
  ```json
  {}
  ```
- **Response 200**: Successful Response
  ```json
  {}
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Show Parameters

- **Method**: POST
- **URL**: `/show_parameters`
- **Description**: No description provided.
- **Request Body**:
  ```json
  {}
  ```
- **Response 200**: Successful Response
  ```json
  {}
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Download File

- **Method**: POST
- **URL**: `/download_parameter_set`
- **Description**: No description provided.
- **Request Body**:
  ```json
  {}
  ```
- **Response 200**: Successful Response
  ```json
  {}
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```

