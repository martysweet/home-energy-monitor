#!/usr/bin/env bash
set -e

# Import custom variables
source env.sh

# Deploy the functions
aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket ${DEPLOYMENT_BUCKET} \
    --output-template-file packaged-template.yaml \
    --profile ${AWS_PROFILE}

# See if the stack exists

#aws cloudformation create-stack --stack-name ${STACK_NAME} \
#       --template-body file://packaged-template.yaml \
#       --parameters file://template-parameters.json \
#       --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM \
#       --profile ${AWS_PROFILE}

aws cloudformation deploy --template-file packaged-template.yaml \
    --stack-name ${STACK_NAME} \
    --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM \
    --profile ${AWS_PROFILE}


rm packaged-template.yaml