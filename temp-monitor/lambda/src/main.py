import boto3

client = boto3.client('cloudwatch')


def lambda_handler(event, context):
    dimensions = [
        {
            'Name': 'Device',
            'Value': 'Heatstore'
        },
    ]

    try:
        client.put_metric_data(
            Namespace='House/Monitoring',
            MetricData=[
                {
                    'MetricName': 'HeatstoreTop',
                    'Dimensions': dimensions,
                    'Value': event['top'],
                },
                {
                    'MetricName': 'HeatstoreMiddle',
                    'Dimensions': dimensions,
                    'Value': event['middle'],
                },
                {
                    'MetricName': 'HeatstoreBottom',
                    'Dimensions': dimensions,
                    'Value': event['bottom'],
                },
            ]
        )
    except Exception as e:
        print(e)
        raise e
