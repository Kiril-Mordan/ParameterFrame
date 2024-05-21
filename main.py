# essential
import numpy as np
import os
# api
from fastapi import FastAPI, HTTPException, UploadFile, File, Response, Header, Depends, Form, Body, status
from fastapi.responses import FileResponse, JSONResponse
from typing import List, Optional
from pathlib import Path
import shutil
# core dependencies
from parameterframe import ParameterFrame, SqlAlchemyDatabaseManager, MockerDatabaseConnector
# from mocker_db import MockerDB, MockerConnector
from conf.settings import API_SETUP_PARAMS, API_VERSION
# types
from utils.data_types import *
# endpoint descriptions
from utils.response_descriptions import *
# other
from utils.other import process_and_store_files, generate_random_name


# start the app and activate mockerdb
app = FastAPI(version=API_VERSION)


def check_access_key(access_key : str):

    if access_key != API_SETUP_PARAMS['access_key']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad Access Key",
            headers={"WWW-Authenticate" : "Bearer"}
        )

def check_db_access_key(db_access_key : str):

    if db_access_key != API_SETUP_PARAMS['db_access_key']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad Access Key",
            headers={"WWW-Authenticate" : "Bearer"}
        )


# endpoints
@app.get("/")
def read_root():
    return "Still alive!"


@app.post("/set_reset_schema",
          description="For databases that require predefined schema, drops tables and sets up new schema.",
          response_model=SetResetSchemaResponse,
          responses=SetResetSchema)
async def set_reset_schema(access_key : str = Header(..., example="access_key", description = "Access key for request authentication."),
                           db_access_key : str = Header(..., example="db_access_key", description = "Additional access key for unlocking table resets if existing connection allows.")):

    try:

        check_access_key(access_key = access_key)
        # store files in new dir for adding to parameterframe

        check_db_access_key(db_access_key = db_access_key)

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':
            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )
        else:
            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        pf.database_connector.drop_tables()
        pf.database_connector.create_tables()

        return {'outcome_success' : True}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")


@app.post("/declare_solution",
          description="Provide basic description of new solution.",
          response_model=DeclareSolutionResponse,
          responses=DeclareSolution)
async def declare_solution(
    solution_name : str = Form(..., example = "solution_name",
                               description="New solution name"),
    solution_description : Optional[str] = Form(default= None,
                                                example = "Description of new example solution.",
                                                description="Description of new example solution."),
    deployment_date : Optional[str] = Form(default= None, example = "2024-xx-xx",
                                                description="Deployment date of solution."),
    deprecation_date : Optional[str] = Form(default= None, example = "2024-xx-xx",
                                            description="Deprication date of solution if known."),
    maintainers : Optional[str] = Form(default= None, example = "Maintainer 1, Mainteiner 2",
                                                description="[maintainer 1, maintainer 2, ...]"),
    access_key : str = Header(..., description = "Access key for request authentication.")
    ):

    try:

        check_access_key(access_key = access_key)

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':

            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        else:

            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        pf.add_solution(
            # mandatory
            solution_name=solution_name,
            # optional description
            solution_description=solution_description,
            deployment_date=deployment_date,
            deprecation_date=deprecation_date,
            maintainers=maintainers
        )

        pf.commit_solution(
            # either solution id or solution name should be provided
            solution_name=solution_name
        )

        pf.push_solution(
            # either solution id or solution name should be provided
            solution_name = solution_name
        )

        return {"solution_id" : pf.show_solutions()['solution_id'][0]}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e.detail}")
    # finally:
    #     shutil.rmtree(random_dir)


@app.post("/upload_parameter_set",
          description="Upload files for parameter set and assign the to already declared solution.",
          response_model=UploadParameterResponse,
          responses=UploadParameter)
async def upload_parameter_set(
    files: List[UploadFile] = File(..., description="Files that should be uploaded as parameter set"),
    solution_id : str = Form(..., example = "cec89c4cbb8c891d388407ea93d84a5cd4f996af6d5c1b0cc5fe1cb12101acf5",
                             description = "Existing solution_id."),
    parameter_set_name : Optional[str] = Form(default=None,
                                              example="5779bbf896ebb8f09a6ea252b09f8adb1a416e8780cf1424fb9bb93dbec8deb5",
                                              description="Parameter set name."),
    parameter_set_description : Optional[str] = Form(default=None,
                                                     example="example description",
                                                     description="Parameter set description."),
    access_key : str = Header(..., description = "Access key for request authentication.")
    ):

    try:

        check_access_key(access_key = access_key)

        # store files in new dir for adding to parameterframe
        random_dir_name = generate_random_name()
        process_and_store_files(files, directory=random_dir_name)

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':

            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                params_path = random_dir_name,
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        else:

            # - with database connector for MockerDB
            pf = ParameterFrame(
                params_path = random_dir_name,
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        pf.process_parameters_from_files()

        pf.make_parameter_set(
            parameter_set_name=parameter_set_name,
            parameter_set_description=parameter_set_description
        )

        parameter_set_names = [n for n in pf.param_sets]

        if len(parameter_set_names) != 1:
            raise Exception("len(parameter_set_names) != 1")

        pf.add_parameter_set_to_solution(solution_id=solution_id,
                                        parameter_set_name=parameter_set_names[0])

        solution_names = [n for n in pf.solutions]

        if len(solution_names) != 1:
            raise Exception("len(solution_names) != 1")

        pf.commit_solution(solution_name=solution_names[0],
                            parameter_set_names=parameter_set_names)

        pf.push_solution(solution_id=solution_id,
                            parameter_set_names=parameter_set_names)

        return {"parameter_set_id" : pf.show_parameter_sets(solution_id = solution_id)['parameter_set_id'][0]}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e.detail}")
    finally:
        shutil.rmtree(random_dir_name)

@app.post("/get_latest_parameter_set_id",
          description="Get parameter set ids for a given solution and deployment status, since newly defined are marked with STAGING, it is used by default.",
          response_model=GetLatestParameterSetIdResponse,
          responses=GetLatestParameterSetId)
async def get_latest_parameter_set_id(
    solution_id : str = Form(..., example = "existing solution_id",
                             description= "Solution id."),
    deployment_status : Optional[str] = Form("STAGING", example = "STAGING",
                                             description= "Deployment status for solution id."),
    access_key : str = Header(..., description = "Access key for request authentication.")
    ):

    try:

        check_access_key(access_key = access_key)

        # store files in new dir for adding to parameterframe

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':
            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )
        else:
            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        parameter_set_ids = pf.get_parameter_set_id_for_solution(solution_id=solution_id,
                                            deployment_status=deployment_status)

        return {"parameter_set_id" : parameter_set_ids}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/change_status_from_staging_to_production",
          description="Change deployment status of select parameter set from staging to production.",
          response_model=ChangeStatusFromStagingToProductionResponse,
          responses=ChangeStatusFromStagingToProduction)
async def change_status_from_staging_to_production(
    solution_id : str = Form(..., example = "existing solution_id", description= "Solution id."),
    parameter_set_id : str = Form(..., example = "existing parameter_set_id"),
    access_key : str = Header(..., description = "Access key for request authentication.")
    ):

    try:

        check_access_key(access_key = access_key)

        # store files in new dir for adding to parameterframe

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':
            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )
        else:
            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        status = pf.change_status_from_staging_to_production(
            solution_id=solution_id,
            parameter_set_id=parameter_set_id
        )

        return {'outcome_success' : status}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/change_status_from_production_to_archived",
          description="Change deployment status of select parameter set from production to archived.",
          response_model=ChangeStatusFromProductionToArchivedResponse,
          responses=ChangeStatusFromProductionToArchived)
async def change_status_from_production_to_archived(
    solution_id : str = Form(..., example = "existing solution_id", description= "Solution id."),
    parameter_set_id : str = Form(..., example = "existing parameter_set_id"),
    access_key : str = Header(..., description = "Access key for request authentication.")
    ):

    try:

        check_access_key(access_key = access_key)

        # store files in new dir for adding to parameterframe

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':
            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )
        else:
            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        status = pf.change_status_from_production_to_archived(
            solution_id=solution_id,
            parameter_set_id=parameter_set_id
        )

        return {'outcome_success' : status}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/change_status_from_archived_production",
          description="Change deployment status of select parameter set from archived to production.",
          response_model=ChangeStatusFromArchivedToProductionResponse,
          responses=ChangeStatusFromArchivedToProduction)
async def change_status_from_archived_production(
    solution_id : str = Form(..., example = "existing solution_id", description= "Solution id."),
    parameter_set_id : str = Form(..., example = "existing parameter_set_id"),
    access_key : str = Header(..., description = "Access key for request authentication.")
    ):

    try:

        check_access_key(access_key = access_key)

        # store files in new dir for adding to parameterframe

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':
            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )
        else:
            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        status = pf.change_status_from_archived_production(
            solution_id=solution_id,
            parameter_set_id=parameter_set_id
        )

        return {'outcome_success' : status}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/change_deployment_status",
          description="Change deployment status of select parameter set from existing status to new status.",
          response_model=ChangeDeploymentStatusResponse,
          responses=ChangeDeploymentStatus)
async def change_deployment_status(
    solution_id : str = Form(..., example = "existing solution_id", description= "Solution id."),
    parameter_set_id : str = Form(..., example = "existing parameter_set_id"),
    current_deployment_status : str = Form(..., example = "current deployment status"),
    new_deployment_status : str = Form(..., example = "new deployment status"),
    access_key : str = Header(..., description = "Access key for request authentication.")
    ):

    try:

        check_access_key(access_key = access_key)

        # store files in new dir for adding to parameterframe

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':
            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )
        else:
            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        status = pf.database_connector.modify_parameter_set_status(
            solution_id=solution_id,
            parameter_set_ids = parameter_set_id,
            current_deployment_status = current_deployment_status,
            new_deployment_status = new_deployment_status
        )

        return {'outcome_success' : status}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/show_solutions",
          description="Show description of all solutions in parameter storage",
          response_model=ShowSolutionsResponse,
          responses=ShowSolutions)
async def show_solutions(access_key : str = Header(..., description = "Access key for request authentication.")):

    try:

        check_access_key(access_key = access_key)
        # store files in new dir for adding to parameterframe

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':
            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )
        else:
            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        pf.pull_solution(
            pull_attribute_values = False
        )

        solutions = pf.show_solutions()

        return {'response' : solutions.to_dict('records')}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/show_parameter_sets",
          description="Show description of all or select parameter set for a given solution.",
          response_model=ShowParameterSetsResponse,
          responses=ShowParameterSets)
async def show_parameter_sets(
    solution_id : str = Form(..., example = "existing solution_id", description= "Solution id."),
    parameter_set_id : Optional[str] = Form(default=None, example = "existing parameter_set_id", description= "Parameter set id."),
    access_key : str = Header(..., description = "Access key for request authentication.")
    ):

    try:

        check_access_key(access_key = access_key)

        # store files in new dir for adding to parameterframe

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':
            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )
        else:
            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        pf.pull_solution(solution_id=solution_id,
                  # optionally specify parameter_set_id
                 parameter_set_id=parameter_set_id,
                 pull_attribute_values = False)

        parameter_sets = pf.show_parameter_sets(solution_id=solution_id)

        return {'response' :  parameter_sets.to_dict('records')}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/show_parameters",
          description="Show description of all select parameters for a given solution id and parameter set id.",
          response_model=ShowParametesResponse,
          responses=ShowParameters)
async def show_parameters(
    solution_id : str = Form(..., example = "existing solution_id", description= "Solution id."),
    parameter_set_id : str = Form(..., example = "existing parameter_set_id", description= "Parameter set id."),
    access_key : str = Header(..., description = "Access key for request authentication.")
    ):

    try:

        check_access_key(access_key = access_key)

        # store files in new dir for adding to parameterframe

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':
            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )
        else:
            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )

        pf.pull_solution(solution_id=solution_id,
                  # optionally specify parameter_set_id
                 parameter_set_id=parameter_set_id,
                 pull_attribute_values = False)

        parameters = pf.show_parameters(solution_id=solution_id,
                                            parameter_set_id=parameter_set_id)

        return {'response' : parameters.to_dict('records')}

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/download_parameter_set",
          description="Download files from a given parameter set.",
          #response_model=DownloadParameterSetResponse,
          responses=DownloadParameterSet)
async def download_parameter_set(
    solution_id : str = Form(..., example = "existing solution_id", description= "Solution id."),
    parameter_set_id : str = Form(..., example="example parameter_set_id", description= "Parameter set id."),
    access_key : str = Header(..., description = "Access key for request authentication.")
):

    try:

        check_access_key(access_key = access_key)

        # store files in new dir for adding to parameterframe
        random_dir_name = generate_random_name()

        random_dir_name = Path(random_dir_name)
        random_dir_name.mkdir(parents=True, exist_ok=True)

        if API_SETUP_PARAMS['database_connector_type'] == 'SQLALCHEMY':
            # - with SqlAlchemy database connector
            pf = ParameterFrame(
                database_connector = SqlAlchemyDatabaseManager(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )
        else:
            # - with database connector for MockerDB
            pf = ParameterFrame(
                database_connector = MockerDatabaseConnector(connection_details = {
                'base_url' : API_SETUP_PARAMS['base_url']}),
                chunk_size = API_SETUP_PARAMS['chunk_size']
            )


        pf.pull_solution(solution_id=solution_id,
                         parameter_set_id=parameter_set_id)

        pf.reconstruct_parameter_set(
            solution_id=solution_id,
            parameter_set_id=parameter_set_id,
            params_path = random_dir_name
        )

        # Create a zip file containing all files in the upload directory
        shutil.make_archive(random_dir_name, 'zip', random_dir_name)
        # Open the zip file and stream its content to the client
        with open(f"{random_dir_name}.zip", "rb") as file:
            contents = file.read()
        response = Response(content=contents)
        response.headers["Content-Disposition"] = f"attachment; filename={solution_id}_{parameter_set_id}.zip"
        return response

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")
    finally:
        shutil.rmtree(random_dir_name)
        os.remove(f"{random_dir_name}.zip")


