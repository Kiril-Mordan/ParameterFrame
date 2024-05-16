# DATA TYPES FOR MOCKER-DB ENDPOINTS

# types
from fastapi import Form, Body, File, UploadFile, Response
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Dict, Union



class DeclareSolutionResponse(BaseModel):
    solution_id : str

class UploadParameterResponse(BaseModel):
    parameter_set_id : str

class GetLatestParameterSetIdResponse(BaseModel):
    parameter_set_id: List[str]

class ChangeStatusFromStagingToProductionResponse(BaseModel):
    outcome_success: bool

class ChangeStatusFromProductionToArchivedResponse(BaseModel):
    outcome_success: bool

class ChangeStatusFromStagingToProductionResponse(BaseModel):
    outcome_success: bool

class ChangeStatusFromArchivedToProductionResponse(BaseModel):
    outcome_success: bool

class ChangeDeploymentStatusResponse(BaseModel):
    outcome_success: bool

class ShowSolutionsResponse(BaseModel):
    response : List[Dict]

class ShowParameterSetsResponse(BaseModel):
    response : List[Dict]

class ShowParametesResponse(BaseModel):
    response : List[Dict]

class ErrorResponseModel(BaseModel):
    detail: str


