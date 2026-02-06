from aws_cdk import (
    Duration,
    RemovalPolicy,
    Size,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_s3 as _s3,
    aws_s3_deployment as _deployment
)

from constructs import Construct

class IpinfoDeploy(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account

    ### S3 BUCKETS ###

        bucket = _s3.Bucket.from_bucket_name(
            self, 'bucket',
            bucket_name = 'ipinfo-staged-use2-lukach-io'
        )

        deployment = _deployment.BucketDeployment(
            self, 'DeployFunctionFile',
            sources = [_deployment.Source.asset('code')],
            destination_bucket = bucket,
            prune = False
        )

        use1 = _s3.Bucket.from_bucket_name(
            self, 'use1',
            bucket_name = 'ipinfo-staged-use1-lukach-io'
        )

        usw2 = _s3.Bucket.from_bucket_name(
            self, 'usw2',
            bucket_name = 'ipinfo-staged-usw2-lukach-io'
        )

    ### IAM ROLE ###

        role = _iam.Role(
            self, 'role',
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )

        role.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'lambda:UpdateFunctionCode',
                    's3:GetObject',
                    's3:PutObject'
                ],
                resources = [
                    '*'
                ]
            )
        )

    ### LAMBDA FUNCTION ###

        deploy = _lambda.Function(
            self, 'deploy',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('deploy'),
            handler = 'deploy.handler',
            environment = dict(
                S3_BUCKET = bucket.bucket_name,
                S3_USE1 = use1.bucket_name,
                S3_USW2 = usw2.bucket_name,
                LAMBDA_FUNCTION_USE1 = 'arn:aws:lambda:us-east-1:'+str(account)+':function:find',
                LAMBDA_FUNCTION_USW2 = 'arn:aws:lambda:us-west-2:'+str(account)+':function:find'
            ),
            ephemeral_storage_size = Size.gibibytes(1),
            timeout = Duration.seconds(900),
            memory_size = 1024,
            role = role
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+deploy.function_name,
            retention = _logs.RetentionDays.ONE_WEEK,
            removal_policy = RemovalPolicy.DESTROY
        )

        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '5',
                hour = '11',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )

        event.add_target(
            _targets.LambdaFunction(
                deploy
            )
        )
