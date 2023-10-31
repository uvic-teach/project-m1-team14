#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { SiteDeployStack } from "../lib/frontend-stack";

const app = new cdk.App();
new SiteDeployStack(app, "SiteDeployStack", {
  env: { account: "446708209687", region: "us-east-1" },
});
