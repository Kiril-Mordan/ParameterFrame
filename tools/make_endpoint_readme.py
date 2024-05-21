import json
from typing import Dict, Any

def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)

def resolve_ref(ref: str, components: Dict[str, Any]) -> Dict[str, Any]:
    ref_path = ref.split('/components/schemas/', 1)[-1]
    return components['schemas'][ref_path]

def extract_example(schema: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
    if '$ref' in schema:
        schema = resolve_ref(schema['$ref'], components)
    if 'example' in schema:
        return schema['example']
    example = {}
    for prop, details in schema.get('properties', {}).items():
        if '$ref' in details:
            resolved_schema = resolve_ref(details['$ref'], components)
            example[prop] = extract_example(resolved_schema, components)
        elif 'properties' in details:
            example[prop] = extract_example(details, components)
        else:
            example[prop] = details.get('example', f'example_{prop}')
    return example

def extract_response_example(content: Dict[str, Any], components: Dict[str, Any]) -> Dict[str, Any]:
    for content_type, content_details in content.items():
        schema = content_details.get('schema', {})
        if 'example' in content_details:
            return content_details['example']
        return extract_example(schema, components)
    return {}

def generate_markdown(data: Dict[str, Any]) -> str:
    components = data.get('components', {})
    endpoints = ["# API Endpoints\n\n"]

    for path, methods in data.get('paths', {}).items():
        for method, details in methods.items():
            endpoint_str = f"### {details.get('summary', 'API Endpoint')}\n\n"
            endpoint_str += f"- **Method**: {method.upper()}\n"
            endpoint_str += f"- **URL**: `{path}`\n"
            endpoint_str += f"- **Description**: {details.get('description', 'No description provided.')}\n"

            # Extracting Request Body Example
            request_body = details.get('requestBody', {})
            if request_body:
                for content_type, content in request_body.get('content', {}).items():
                    schema = content.get('schema', {})
                    example = extract_example(schema, components)
                    example_json = json.dumps(example, indent=2).replace('\n', '\n  ')
                    endpoint_str += f"- **Request Body ({content_type})**:\n  ```json\n  {example_json}\n  ```\n"

            # Handling Responses
            responses = details.get('responses', {})
            for status_code, response in responses.items():
                response_description = response.get('description', '')
                content = response.get('content', {})
                if content:
                    content_type = list(content.keys())[0]  # Fix to get the first key
                    example = extract_response_example(content, components)
                    example_json = json.dumps(example, indent=2).replace('\n', '\n  ')
                    endpoint_str += f"- **Response {status_code} ({content_type})**: {response_description}\n  ```json\n  {example_json}\n  ```\n\n"

            endpoints.append(endpoint_str)

    return "\n".join(endpoints)

def main():
    openapi_data = load_json('openapi.json')  # Load your OpenAPI spec JSON file
    markdown_content = generate_markdown(openapi_data)

    with open('docs/API_ENDPOINTS.md', 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)

if __name__ == "__main__":
    main()
