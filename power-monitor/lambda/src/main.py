import boto3

client = boto3.client('cloudwatch')


def lambda_handler(event, context):
    dimensions = [
        {
            'Name': 'Device',
            'Value': 'EnergyMonitor'
        },
    ]

    try:
        client.put_metric_data(
            Namespace='House/Monitoring',
            MetricData=[
                {
                    'MetricName': 'Grid',
                    'Dimensions': dimensions,
                    'Value': event['i1'],
                },
                {
                    'MetricName': 'Solar',
                    'Dimensions': dimensions,
                    'Value': event['i2'],
                },
                {
                    'MetricName': 'WaterImmersion',
                    'Dimensions': dimensions,
                    'Value': event['i3'],
                },
                {
                    'MetricName': 'ASHP',
                    'Dimensions': dimensions,
                    'Value': event['i4'],
                },
                {
                    'MetricName': 'BufferImmersion',
                    'Dimensions': dimensions,
                    'Value': event['i5'],
                },
                {
                    'MetricName': 'Voltage',
                    'Dimensions': dimensions,
                    'Value': event['Vrms'],
                },
            ]
        )
    except Exception as e:
        print(e)
        raise e
