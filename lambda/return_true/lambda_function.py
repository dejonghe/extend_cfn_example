from cfnresponse import send, SUCCESS, FAILED

def lambda_handler(event, context):
    print event
    send(event, context, SUCCESS)
     
