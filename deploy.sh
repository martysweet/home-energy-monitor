#!/usr/bin/env bash
set -e

# Import custom variables
source env.sh

# Build the functions with dependancies --use-container \
echo "If the next follows, setup a virtual environment for Python 2.7"
echo "Ensure libbluetooth-dev is installed for pybluez compilation"
sam build \
    --template template.yaml \
    --profile ${AWS_PROFILE}

# Deploy the functions
sam package \
    --template-file .aws-sam/build/template.yaml \
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

#rm packaged-template.yaml
#rm -rf .aws-sam/*