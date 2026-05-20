terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "artifacts" {
  bucket        = "student-devin-johnson-s3-${var.project_name}"
  force_destroy = false
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.artifacts.id
  key    = "lambda/${var.project_name}.zip"
  source = var.lambda_zip_path
  etag   = filemd5(var.lambda_zip_path)
}

resource "aws_lambda_function" "api" {
  function_name = var.lambda_function_name
  role          = var.lambda_role_arn
  runtime       = var.lambda_runtime
  handler       = var.lambda_handler

  s3_bucket = aws_s3_bucket.artifacts.id
  s3_key    = aws_s3_object.lambda_zip.key

  source_code_hash = filebase64sha256(var.lambda_zip_path)

  timeout     = 30
  memory_size = 512

  environment {
    variables = merge({ APP_ENV = var.environment }, var.lambda_environment_variables)
  }
}

resource "aws_apigatewayv2_api" "http" {
  name          = "student-devin-johnson-bankapp-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_proxy" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.api.invoke_arn
  payload_format_version = "2.0"
  integration_method     = "POST"
}

resource "aws_apigatewayv2_route" "root" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "ANY /"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_proxy.id}"
}

resource "aws_apigatewayv2_route" "proxy" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_proxy.id}"
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = var.api_stage_name
  auto_deploy = true
}

resource "aws_lambda_permission" "allow_apigw" {
  statement_id  = "AllowExecutionFromApiGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}

variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Short project name used in resource naming"
  type        = string
  default     = "bankapp"
}

variable "environment" {
  description = "Environment name (dev, staging, prod, etc.)"
  type        = string
  default     = "prod"
}

variable "lambda_runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.14"
}

variable "lambda_handler" {
  description = "Lambda handler in module.function format"
  type        = string
  default     = "main.lambda_handler"
}

variable "lambda_function_name" {
  description = "Lambda function name"
  type        = string
  default     = "prod"
}

variable "lambda_role_arn" {
  description = "Existing IAM role ARN for Lambda execution"
  type        = string
}

variable "lambda_zip_path" {
  description = "Absolute or relative path to your packaged Lambda zip file"
  type        = string
  default     = "../Python/bankapp.zip"
}

variable "api_stage_name" {
  description = "API Gateway stage name"
  type        = string
  default     = "student-devin-johnson-bankapp-api-gw"
}

variable "lambda_environment_variables" {
  description = "Environment variables exposed to the Lambda runtime"
  type        = map(string)
  default     = {}
}

output "api_invoke_url" {
  description = "Invoke URL for the deployed API stage"
  value       = aws_apigatewayv2_stage.prod.invoke_url
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.api.function_name
}

output "artifact_bucket_name" {
  description = "S3 bucket used for Lambda deployment artifacts"
  value       = aws_s3_bucket.artifacts.bucket
}


