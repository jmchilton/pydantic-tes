#!/bin/bash

# must be run from a virtualenv with...
# https://github.com/koxudaxi/datamodel-code-generator
datamodel-codegen --url "https://raw.githubusercontent.com/ga4gh/task-execution-schemas/develop/openapi/task_execution_service.openapi.yaml" --output "models.py"
# datamodel-codegen --url "https://raw.githubusercontent.com/ga4gh-discovery/ga4gh-service-info/v1.0.0/service-info.yaml#/components/schemas/Service" --output Service.py
