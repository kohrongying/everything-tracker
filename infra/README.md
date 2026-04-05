# Everything Tracker Infrastructure

This directory contains the AWS CDK infrastructure code for the Everything Tracker application.

## Architecture

The infrastructure consists of:
- **API Gateway**: REST API that serves as the entry point for the application
- **Lambda Function**: Python runtime running the FastAPI backend
- **CORS Configuration**: Allows cross-origin requests from the frontend

## Prerequisites

1. **AWS CLI**: Install and configure AWS CLI with appropriate credentials
2. **Node.js**: Version 18 or higher
3. **AWS CDK**: Install globally with `npm install -g aws-cdk`

## Setup

1. **Install dependencies**:
   ```bash
   cd infra
   npm install
   ```

2. **Bootstrap CDK** (first time only):
   ```bash
   npm run cdk:bootstrap
   ```

3. **Deploy the infrastructure**:
   ```bash
   npm run cdk:deploy
   ```

## Useful Commands

- `npm run cdk:synth` - Synthesize the CloudFormation template
- `npm run cdk:diff` - Compare deployed stack with current state
- `npm run cdk:deploy` - Deploy the stack
- `npm run cdk:destroy` - Destroy the stack

## Configuration

The Lambda function is configured with:
- **Runtime**: Python 3.10
- **Memory**: 256 MB
- **Timeout**: 30 seconds
- **Handler**: `app.main.handler`

## Environment Variables

Set the following environment variables in the Lambda function:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI`
- `DYNAMODB_TABLE`
- `AWS_REGION`

## API Gateway

The API Gateway is configured with:
- CORS enabled for all origins, methods, and headers
- Proxy integration to the Lambda function
- URL output available as `ApiGatewayUrl` in the CloudFormation outputs
