import * as cdk from "aws-cdk-lib";
import { LambdaIntegration, RestApi } from "aws-cdk-lib/aws-apigateway";
import { AttributeType, Table } from "aws-cdk-lib/aws-dynamodb";
import { Function, Code, Runtime } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class GalactisStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const user_db = new Table(this, "UserTable", {
      partitionKey: {
        name: "username",
        type: AttributeType.STRING,
      },
    });

    const token_db = new Table(this, "TokenTable", {
      partitionKey: {
        name: "token",
        type: AttributeType.STRING,
      },
    });

    const register_handler = new Function(this, "RegisterHandler", {
      runtime: Runtime.PYTHON_3_11,
      code: Code.fromAsset("resources", { exclude: ["login.py, validate.py"] }),
      handler: "register.handler",
      environment: {
        USER_TABLE: user_db.tableName,
        TOKEN_TABLE: token_db.tableName,
      },
    });

    const login_handler = new Function(this, "LoginHandler", {
      runtime: Runtime.PYTHON_3_11,
      code: Code.fromAsset("resources", {
        exclude: ["register.py, validate.py"],
      }),
      handler: "login.handler",
      environment: {
        USER_TABLE: user_db.tableName,
        TOKEN_TABLE: token_db.tableName,
      },
    });

    const validate_handler = new Function(this, "ValidateHandler", {
      runtime: Runtime.PYTHON_3_11,
      code: Code.fromAsset("resources", { exclude: ["login.py, register.py"] }),
      handler: "validate.handler",
      environment: {
        USER_TABLE: user_db.tableName,
        TOKEN_TABLE: token_db.tableName,
      },
    });

    user_db.grantReadData(login_handler);
    user_db.grantFullAccess(register_handler);
    user_db.grantReadData(validate_handler);

    token_db.grantFullAccess(register_handler);
    token_db.grantFullAccess(login_handler);
    token_db.grantReadData(validate_handler);

    const api = new RestApi(this, "GalactisRestApi", {
      deployOptions: {
        throttlingBurstLimit: 10,
        throttlingRateLimit: 10,
      },
    });

    const register_endpoint = api.root.addResource("register");
    register_endpoint.addMethod(
      "POST",
      new LambdaIntegration(register_handler)
    );

    const login_endpoint = api.root.addResource("login");
    login_endpoint.addMethod("POST", new LambdaIntegration(login_handler));

    const validate_endpoint = api.root.addResource("validate");
    validate_endpoint.addMethod(
      "GET",
      new LambdaIntegration(validate_handler),
      {
        apiKeyRequired: true,
      }
    );

    const key = api.addApiKey("GalactisApiKey");
    const plan = api.addUsagePlan("GalatisUsagePlan", {
      name: "Prod",
    });
    plan.addApiKey(key);
    plan.addApiStage({
      api,
      stage: api.deploymentStage,
    });
  }
}
