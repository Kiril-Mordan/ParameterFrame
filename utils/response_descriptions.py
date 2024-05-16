# RESPONSE DESCRIPTIONS FOR MOCKER-DB ENDPOINTS

DeclareSolution = {
             200: {"description": "solution id for new solution",
                   "content": {
                        "application/json": {
                            "example": {
                                "solution_id": "cec89c4cbb8c891d388407ea93d84a5cd4f996af6d5c1b0cc5fe1cb12101acf5"
                            }
                        }
                    }}}

UploadParameter = {
             200: {"description": "parameters set id of newly created parameter set",
                   "content": {
                        "application/json": {
                            "example": {
                                "parameter_set_id": "5779bbf896ebb8f09a6ea252b09f8adb1a416e8780cf1424fb9bb93dbec8deb5"
                            }
                        }
                    }}}

GetLatestParameterSetId = {
    200: {
        "description": "List of parameter set ids for solution and deployment status",
        "content": {
            "application/json": {
                "example": {
                    "parameter_set_id": ["5779bbf896ebb8f09a6ea252b09f8adb1a416e8780cf1424fb9bb93dbec8deb5"]
                }
            }
        }
    }
}


ChangeStatusFromStagingToProduction = {
    200: {
        "description": "List of parameter set ids for solution and deployment status",
        "content": {
            "application/json": {
                "example": {
                    "outcome_success": True
                }
            }
        }
    }
}

ChangeStatusFromProductionToArchived = {
    200: {
        "description": "List of parameter set ids for solution and deployment status",
        "content": {
            "application/json": {
                "example": {
                    "outcome_success": True
                }
            }
        }
    }
}

ChangeStatusFromArchivedToProduction = {
    200: {
        "description": "List of parameter set ids for solution and deployment status",
        "content": {
            "application/json": {
                "example": {
                    "outcome_success": True
                }
            }
        }
    }
}

ChangeDeploymentStatus = {
    200: {
        "description": "List of parameter set ids for solution and deployment status",
        "content": {
            "application/json": {
                "example": {
                    "outcome_success": True
                }
            }
        }
    }
}

ShowSolutions = {
    200: {
        "description": "List of parameter set ids for solution and deployment status",
        "content": {
            "application/json": {
                "example": [{
                    "solution_id": "cec89c4cbb8c891d388407ea93d84a5cd4f996af6d5c1b0cc5fe1cb12101acf5",
                    "solution_name": "new_example_solution",
                    "solution_description": "Description of new example solution.",
                    "deployment_date": "2024-xx-xx",
                    "deprecation_date": None,
                    "maintainers": "some text about maintainers credentials",
                    "commited_parameter_sets": 6
  }]
            }
        }
    }
}

ShowParameterSets = {
    200: {
        "description": "List of parameter set ids for solution and deployment status",
        "content": {
            "application/json": {
                "example": {
  "response": [
    {
      "parameter_set_id": "82b8c5340454adf83667e59092fedbee28213475fd58ab6b3d95b4fc60f4d45f",
      "parameter_set_name": "purple_giant_television_135",
      "parameter_set_description": "",
      "deployment_status": "STAGING",
      "insertion_datetime": "2024-05-16 00:05:43",
      "commited_parameters": 1
    },
    {
      "parameter_set_id": "2f3ee8e19d91a89298d40984df5e7bdd1f1a48008b2e61c88a7f6f81b4ab23f5",
      "parameter_set_name": "silver_happy_car_441",
      "parameter_set_description": "",
      "deployment_status": "STAGING",
      "insertion_datetime": "2024-05-16 00:03:25",
      "commited_parameters": 1
    }
  ]
}
            }
        }
    }
}

ShowParameters = {
    200: {
        "description": "List of parameter set ids for solution and deployment status",
        "content": {
            "application/json": {
                "example": {
  "response": [
    {
      "parameter_set_id": "82b8c5340454adf83667e59092fedbee28213475fd58ab6b3d95b4fc60f4d45f",
      "parameter_set_name": "purple_giant_television_135",
      "parameter_set_description": "",
      "deployment_status": "STAGING",
      "insertion_datetime": "2024-05-16 00:05:43",
      "commited_parameters": 1
    },
    {
      "parameter_set_id": "2f3ee8e19d91a89298d40984df5e7bdd1f1a48008b2e61c88a7f6f81b4ab23f5",
      "parameter_set_name": "silver_happy_car_441",
      "parameter_set_description": "",
      "deployment_status": "STAGING",
      "insertion_datetime": "2024-05-16 00:03:25",
      "commited_parameters": 1
    }
  ]
}
            }
        }
    }
}

DownloadParameterSet = {
    200: {
        "description": "File successfully downloaded",
        "content": {
            "application/zip": {}
        }
    }
}