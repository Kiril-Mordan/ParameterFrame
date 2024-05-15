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

