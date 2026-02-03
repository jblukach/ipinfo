#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ipinfo.ipinfo_deploy import IpinfoDeploy
from ipinfo.ipinfo_download import IpinfoDownload
from ipinfo.ipinfo_finduse1 import IpinfoFindUse1
from ipinfo.ipinfo_findusw2 import IpinfoFindUsw2
from ipinfo.ipinfo_stack import IpinfoStack

app = cdk.App()

IpinfoDeploy(
    app, 'IpinfoDeploy',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

IpinfoDownload(
    app, 'IpinfoDownload',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

IpinfoFindUse1(
    app, 'IpinfoFindUse1',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

IpinfoFindUsw2(
    app, 'IpinfoFindUsw2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-west-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

IpinfoStack(
    app, 'IpinfoStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

cdk.Tags.of(app).add('Alias','ipinfo')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/ipinfo')
cdk.Tags.of(app).add('Org','lukach.io')

app.synth()