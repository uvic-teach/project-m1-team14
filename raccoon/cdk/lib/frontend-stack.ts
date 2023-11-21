import * as cdk from "aws-cdk-lib";
import { Bucket } from "aws-cdk-lib/aws-s3";
import { BucketDeployment, Source } from "aws-cdk-lib/aws-s3-deployment";
import { Construct } from "constructs";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class SiteDeployStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = Bucket.fromBucketArn(
      this,
      "DestinationBucket",
      "arn:aws:s3:::www.brennanmcmicking.net"
    );

    new BucketDeployment(this, "BucketDeployment", {
      sources: [Source.asset("../raccoon/build")],
      destinationBucket: bucket,
      destinationKeyPrefix: "seng350/",
      distributionPaths: ["/seng350/*"],
    });
  }
}
