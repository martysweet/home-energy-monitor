#!/usr/bin/env bash
set -e

# Import custom variables
source env.sh

# Build the functions with dependencies
sam build \
    --template template.yaml \
    --profile ${AWS_PROFILE}

# Deploy the functions
sam package \
    --template-file .aws-sam/build/template.yaml \
    --s3-bucket ${DEPLOYMENT_BUCKET} \
    --output-template-file packaged-template.yaml \
    --profile ${AWS_PROFILE}

# See if the stack exists, create/update with parameters accordingly
if aws cloudformation describe-stacks --stack-name ${STACK_NAME} --profile ${AWS_PROFILE} > /dev/null; then
   aws cloudformation update-stack --stack-name ${STACK_NAME} \
       --template-body file://packaged-template.yaml \
       --parameters file://template-parameters.json \
       --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM \
       --profile ${AWS_PROFILE}
else
    aws cloudformation create-stack --stack-name ${STACK_NAME} \
       --template-body file://packaged-template.yaml \
       --parameters file://template-parameters.json \
       --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM \
       --profile ${AWS_PROFILE}
fi



echo "Cleanup build resources"
rm packaged-template.yaml
rm -rf .aws-sam/*