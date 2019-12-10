# coding: utf-8
import boto3
import logging

logger=logging.getLogger()
logger.setLevel(logging.INFO)

ec2client = boto3.client("ec2")
route53client = boto3.client("route53")

def lambda_handler(event,context):
    main(event)
    
    return "OK"

def main(event):
    instid = event['instance-id']
    response = ec2client.describe_instances(
                    InstanceIds=[
                        instid
                    ]
                )
    ipaddress = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

    for tag in response['Reservations'][0]['Instances'][0]['Tags']:
        if( tag['Key'] == 'DNSname' ):
            dnsname = tag['Value']
        if( tag['Key'] == 'HostZoneID' ):
            zoneid = tag['Value']

    params = {
        'HostedZoneId': zoneid,
        'ChangeBatch': {
            'Comment':'Record update from LamdaFunction',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet':{
                        'Name': dnsname,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': ipaddress
                            }
                        ]
                    }
                }
            ]
        }
    }
    route53client.change_resource_record_sets(**params)
    logger.info( "InstanceID:{0}を{1} {2}でRoute53へ登録しました".format(instid,dnsname,ipaddress) )

