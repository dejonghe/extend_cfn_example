#!/usr/bin/env python2.7
import json
import boto3
import urllib2
from cfnresponse import send, SUCCESS, FAILED
import logging
from optparse import OptionParser


logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class zone_attach(object):
    reason = None
    response_data = None

    def __init__(self, event, context):
        self.event = event
        self.context = context
        logger.info("Event: %s" % self.event)
        logger.info("Context: %s" % self.context)
        if self.context != None:
           self.route53 = boto3.session.Session().client('route53')
        else:
           self.route53 = boto3.session.Session(profile_name=event['ResourceProperties']['Profile']).client('route53')
        try:
            self.vpc_id = event['ResourceProperties']['VpcId']
            self.hosted_zone_id = event['ResourceProperties']['HostedZoneId']
            self.region = event['ResourceProperties']['Region']
        except KeyError as e:
            self.reason = "Missing required property %s" % e
            logger.error(self.reason)
            if self.context:
                self.send_status(FAILED)
            return

    def create(self, updating=False):
        try:
            response = self.route53.associate_vpc_with_hosted_zone(
                HostedZoneId=self.hosted_zone_id,
                VPC={
                    'VPCRegion': self.region,
                    'VPCId': self.vpc_id
                }
            )
            logger.info("Response: %s" % response)
            if not updating:
                self.send_status(SUCCESS)
        except Exception as e:
            self.reason = "Create Vpc Hosted Zone association call Failed %s" % e
            logger.error(self.reason)
            if self.context:
                self.send_status(FAILED)
            return

    def delete(self, updating=False):
        if updating:
            hosted_zone = self.event['OldResourceProperties']['HostedZoneId']
            vpc_id = self.event['OldResourceProperties']['VpcId']
            region = self.event['OldResourceProperties']['Region']
            logger.info("Update dissociate: %s from %s" % (vpc_id,hosted_zone))
        else:
            hosted_zone = self.hosted_zone_id
            vpc_id = self.vpc_id
            region = self.region
            logger.info("Dissociate: %s from %s" % (vpc_id,hosted_zone))
        try: 
            self.route53.disassociate_vpc_from_hosted_zone(
                HostedZoneId=hosted_zone,
                VPC={
                    'VPCRegion': region,
                    'VPCId': vpc_id
                }
            )
            if not updating:
                self.send_status(SUCCESS)
        except Exception as e:
            self.reason = "Delete Vpc Hosted Zone association call Failed %s" % e
            logger.error(self.reason)
            if self.context:
                self.send_status(FAILED)
            return

    def update(self):
        self.create(updating=True)
        self.delete(updating=True)
        self.send_status(SUCCESS)

    def send_status(self, PASS_OR_FAIL):
        send(
            self.event,
            self.context,
            PASS_OR_FAIL,
            reason=self.reason,
            response_data=self.response_data
        )

def lambda_handler(event, context):
    attachment = zone_attach(event, context)
    if event['RequestType'] == 'Delete':
        attachment.delete()
        return
    if event['RequestType'] == 'Create':
        attachment.create()
        return
    if event['RequestType'] == 'Update':
        attachment.update()
        return
    logger.info("Received event: " + json.dumps(event, indent=2))
    if context:
        send(event, context, FAILED, reason="Unknown Request Type %s" % event['RequestType'])


if __name__ == "__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-r","--region", help="Region in which to run.")
    parser.add_option("-q","--old_region", help="Region in which it was ran.")
    parser.add_option("-z","--hosted_zone_id", help="Hosted Zone to attach.")
    parser.add_option("-y","--old_hosted_zone_id", help="Hosted Zone to detach.")
    parser.add_option("-v","--vpc_id", help="VPC to attach to Hosted zone.")
    parser.add_option("-u","--old_vpc_id", help="Old VPC to disassociate to Hosted zone.")
    parser.add_option("-p","--profile", help="Profile name to use when connecting to aws.", default="default")
    parser.add_option("-x","--execute", help="Execute an update create or delete.", default="create")
    (opts, args) = parser.parse_args()

    options_broken = False
    if not opts.vpc_id:
        logger.error("Must Specify VPC")
        options_broken = True
    if not opts.hosted_zone_id:
        logger.error("Must Specify Hosted Zone ID")
        options_broken = True
    if options_broken:
        parser.print_help()
        exit(1) 
    if opts.execute != 'Update':
        event = { 'RequestType': opts.execute, 'ResourceProperties': { 'HostedZoneId': opts.hosted_zone_id, 'VpcId': opts.vpc_id, 'Profile': opts.profile, 'Region': opts.region } }
    else:
        event = { 'RequestType': opts.execute, 'ResourceProperties': { 'HostedZoneId': opts.hosted_zone_id, 'VpcId': opts.vpc_id, 'Profile': opts.profile, 'Region': opts.region }, 'OldResourceProperties': { 'HostedZoneId': opts.old_hosted_zone_id, 'VpcId': opts.old_vpc_id, 'Profile': opts.profile, 'Region': opts.region } }
    lambda_handler(event, None)
