# Terraform deployment for Coginixia Python API

This folder provisions:
- S3 bucket for Lambda deployment artifacts
- Lambda function for the Python API
- API Gateway HTTP API + routes
- Lambda invoke permission for API Gateway

Note: IAM role creation is intentionally not managed here. Provide an existing role ARN via `lambda_role_arn`.

## Prerequisites
- Terraform >= 1.6
- AWS CLI authenticated to the target account
- A pre-existing Lambda execution role ARN with required permissions
- A Lambda zip package at `../Python/function.zip`

## 1) Build Lambda zip
Run from the repository root:

```bash
cd Python
rm -rf package bankapp.zip
mkdir -p package

pip install -r requirements.txt -t package

cp main.py package/
cp -r controllers package/
cp -r domain package/
cp -r models package/
cp -r repo package/
cp -r services package/
cp -r utilities package/

cd package
zip -r ../bankapp.zip .
cd ..
rm -rf package
```

## 2) Create variables file
Copy the example and fill in values:

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

`terraform.tfvars` contains environment values passed directly to Lambda via `lambda_environment_variables`.
Do not commit this file.

Required values for the current API auth flow:
- `API_PATH_SECRET` (long random secret embedded in the request path after `/api/`)

## 3) Initialize and deploy

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## 4) Get API URL

```bash
cd terraform
terraform output -raw api_invoke_url
```

## Update flow
When code changes:
1. Rebuild `../Python/function.zip`
2. Re-run `terraform apply`

Terraform detects zip changes using `source_code_hash` and updates Lambda automatically.

