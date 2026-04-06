import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as path from 'path';

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Lambda function for the backend
    const backendFunction = new lambda.Function(this, 'EverythingTrackerBackend', {
      runtime: lambda.Runtime.PYTHON_3_14,
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
              // install deps into /asset-output
              'uv pip install --system --target /asset-output .',
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
        SES_FROM_EMAIL: 'rongdevs@gmail.com'
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

    backendFunction.addToRolePolicy(new cdk.aws_iam.PolicyStatement({
      actions: ['ses:SendEmail', 'ses:SendRawEmail'],
      resources: ['*'], // Consider restricting this to specific SES resources in production
    }));
  }
}
