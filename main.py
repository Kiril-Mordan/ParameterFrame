# essential
import numpy as np
import os
# api
from fastapi import FastAPI, HTTPException, UploadFile, File, Response, Header, Depends, Form
from fastapi.responses import FileResponse, JSONResponse
from typing import List
from pathlib import Path
import shutil
# core dependencies
from parameterframe import ParameterFrame, SqlAlchemyDatabaseManager, MockerDatabaseConnector
# from mocker_db import MockerDB, MockerConnector
from conf.settings import API_SETUP_PARAMS, API_VERSION
# types
#from utils.response_descriptions import *
# other
from utils.other import process_and_store_files, generate_random_name

# types
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# start the app and activate mockerdb
app = FastAPI(version=API_VERSION)

# endpoints
@app.get("/")
def read_root():
    return "Still alive!"


# Temporary directory to store uploaded files
UPLOAD_DIR = Path("persist")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)



@app.post("/declare_solution")
async def declare_solution(
    solution_name : str = Form(..., example = "new solution name"),
    solution_description : Optional[str] = Form(None, example = "Description of new example solution."),
    deployment_date : Optional[str] = Form(None, example = "2024-xx-xx"),
    deprecation_date : Optional[str] = Form(None, example = "2024-xx-xx"),
    maintainers : Optional[str] = Form(None, example = "some text about maintainers credentials")
    ):


    try:

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



@app.post("/upload_parameter_set")
async def upload_files(
    files: List[UploadFile] = File(...),
    solution_id : str = Form(..., example = "existing solution_id"),
    parameter_set_name : Optional[str] = Form(default=None, example="example parameter set name"),
    parameter_set_description : Optional[str] = Form(default=None, example="example description")
    ):

    try:
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

@app.post("/get_latest_parameter_set_id")
async def get_latest_parameter_set_id(
    solution_id : str = Form(..., example = "existing solution_id"),
    deployment_status : Optional[str] = Form("STAGING", example = "STAGING")
    ):

    try:
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

@app.post("/change_status_from_staging_to_production")
async def show_parameters(
    solution_id : str = Form(..., example = "existing solution_id"),
    parameter_set_id : str = Form(..., example = "existing parameter_set_id")
    ):

    try:
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

        pf.change_status_from_staging_to_production(
            solution_id=solution_id,
            parameter_set_id=parameter_set_id
        )

        return True

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/change_status_from_production_to_archived")
async def show_parameters(
    solution_id : str = Form(..., example = "existing solution_id"),
    parameter_set_id : str = Form(..., example = "existing parameter_set_id")
    ):

    try:
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

        pf.change_status_from_production_to_archived(
            solution_id=solution_id,
            parameter_set_id=parameter_set_id
        )

        return True

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/change_status_from_archived_production")
async def show_parameters(
    solution_id : str = Form(..., example = "existing solution_id"),
    parameter_set_id : str = Form(..., example = "existing parameter_set_id")
    ):

    try:
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

        pf.change_status_from_archived_production(
            solution_id=solution_id,
            parameter_set_id=parameter_set_id
        )

        return True

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/change_deployment_status")
async def show_parameters(
    solution_id : str = Form(..., example = "existing solution_id"),
    parameter_set_id : str = Form(..., example = "existing parameter_set_id"),
    current_deployment_status : str = Form(..., example = "current deployment status"),
    new_deployment_status : str = Form(..., example = "new deployment status")
    ):

    try:
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

        pf.database_connector.modify_parameter_set_status(
            solution_id=solution_id,
            parameter_set_ids = parameter_set_id,
            current_deployment_status = current_deployment_status,
            new_deployment_status = new_deployment_status
        )

        return True

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/show_solutions")
async def show_solutions():

    try:
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

        pf.pull_solution()

        solutions = pf.show_solutions()

        return  solutions.to_dict('records')

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/show_parameter_sets")
async def show_parameter_sets(
    solution_id : str = Form(..., example = "existing solution_id"),
    parameter_set_id : Optional[str] = Form(default=None, example = "existing parameter_set_id")
    ):

    try:
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
                 parameter_set_id=parameter_set_id)

        parameter_sets = pf.show_parameter_sets(solution_id=solution_id)

        return  parameter_sets.to_dict('records')

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")

@app.post("/show_parameters")
async def show_parameters(
    solution_id : str = Form(..., example = "existing solution_id"),
    parameter_set_id : str = Form(..., example = "existing parameter_set_id")
    ):

    try:
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
                 parameter_set_id=parameter_set_id)

        parameters = pf.show_parameters(solution_id=solution_id,
                                            parameter_set_id=parameter_set_id)

        return  parameters.to_dict('records')

    except HTTPException as e:
        print(f"HTTPException : {e.detail}")
    except Exception as e:
        raise Exception(f"Error : {e}")


@app.post("/download_parameter_set")
async def download_file(
    solution_id : str = Form(..., example = "existing solution_id"),
    parameter_set_id : str = Form(..., example="example parameter_set_id"),
):

    try:

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


