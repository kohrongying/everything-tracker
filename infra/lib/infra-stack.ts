import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as path from 'path';
import * as ssm from 'aws-cdk-lib/aws-ssm';

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // https://docs.aws.amazon.com/powertools/python/3.14.0/#x86_65
    const powertools_layer = lambda.LayerVersion.fromLayerVersionArn(this, "lambda-powertools",
      `arn:aws:lambda:${props?.env?.region}:017000801446:layer:AWSLambdaPowertoolsPythonV3-python313-x86_64:16`,
    )

    // Lambda function for the backend
    const backendFunction = new lambda.Function(this, 'EverythingTrackerBackend', {
      runtime: lambda.Runtime.PYTHON_3_14,
      layers: [powertools_layer],
      code: lambda.Code.fromAsset(path.join(__dirname, '../../backend'), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_14.bundlingImage,
          command: [
            'bash', '-c',
            [
              // Set writable cache for uv (avoid permission issues when bundling)
              'export UV_CACHE_DIR=/tmp/.uv',
              // install uv
              'pip install uv',
              // Export deps to requirements.txt
              'uv export --frozen --no-dev --no-editable -o requirements.txt',
              // install deps into /asset-output
              'pip install --target /asset-output -r requirements.txt',
              // copy source code
              'cp -r . /asset-output'
            ].join(' && ')
          ],
        },
      }),
      handler: 'app.main.handler',
      timeout: cdk.Duration.seconds(30),
      memorySize: 256,
      environment: {
        // Add environment variables as needed
        STAGE: 'prod', // Defaults to RestApi default stage name
        SES_FROM_EMAIL: 'rongdevs@gmail.com',
        FRONTEND_URL_PARAMETER_NAME: '/everything-tracker/rest-api-url',
        JWT_SECRET_KEY_PARAMETER_NAME: '/everything-tracker/jwt-secret-key'
      },
    });

    // API Gateway
    const api = new apigateway.RestApi(this, 'EverythingTrackerAPI', {
      restApiName: 'EverythingTrackerAPI',
      description: 'API for Everything Tracker application',
      endpointConfiguration: {
        types: [apigateway.EndpointType.REGIONAL]
      },
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: ['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key'],
      },
    });

    // Lambda integration
    const lambdaIntegration = new apigateway.LambdaIntegration(backendFunction, {
      requestTemplates: { 'application/json': '{ "statusCode": "200" }' },
    });

    // API Gateway resource and method
    const rootResource = api.root;
    rootResource.addMethod('ANY', lambdaIntegration);

    // Add proxy resource for all paths
    const proxyResource = rootResource.addResource('{proxy+}');
    proxyResource.addMethod('ANY', lambdaIntegration);

    // Create parameter store string
    new ssm.StringParameter(this, 'RestApiUrl', {
      parameterName: '/everything-tracker/rest-api-url',
      stringValue: api.url
    });

    // Grant SES permissions to the Lambda function
    backendFunction.addToRolePolicy(new cdk.aws_iam.PolicyStatement({
      actions: ['ses:SendEmail', 'ses:SendRawEmail'],
      resources: [`arn:aws:ses:${props?.env?.region}:${props?.env?.account}:identity/rongdevs@gmail.com`],
    }));

    backendFunction.addToRolePolicy(new cdk.aws_iam.PolicyStatement({
      actions: ['ssm:GetParameter'],
      resources: [
        `arn:aws:ssm:${props?.env?.region}:${props?.env?.account}:parameter/everything-tracker/jwt-secret-key`,
        `arn:aws:ssm:${props?.env?.region}:${props?.env?.account}:parameter/everything-tracker/rest-api-url`
      ],
    }));

    backendFunction.addToRolePolicy(new cdk.aws_iam.PolicyStatement({
      actions: ['kms:Decrypt'],
      resources: ['*'], // Consider restricting this to specific KMS keys in production
    }));
  
}}
