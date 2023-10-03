#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { GalactisStack } from "../lib/galactis-stack";

const app = new cdk.App();
new GalactisStack(app, "GalactisStack", {
  env: { account: "446708209687", region: "us-west-2" },
});
