#!/bin/bash 

# Set variables
function usage()
{
  echo "ERROR: Incorrect arguments provided."
  echo "Usage: $0 {args}"
  echo "Where valid args are: "
  echo "  -p <profile> (REQUIRED) -- Profile to use for AWS commands"
  echo "  -b <bucket> (REQUIRED) -- bucket name to sync to"
  exit 1
}

# Parse args
if [[ "$#" -lt 2 ]] ; then
  echo 'parse error'
  usage
fi
PROFILE=default
while getopts "p:r:b:" opt; do
  case $opt in
    p)
      PROFILE=$OPTARG
    ;;
    b)
      BUCKET=$OPTARG
    ;;
    \?)
      echo "Invalid option: -$OPTARG"
      usage
    ;;
  esac
done
CWD=$(echo $PWD | rev | cut -d'/' -f1 | rev)
if [ $CWD != "extend_cfn_example" ]
then
  echo "These tools are expecting to be ran from the base of the aws-tools repo."
  exit 1
fi

####
# Need to replace any / in release with . 
######

aws s3 sync ./cloudformation/ s3://$BUCKET/cloudformation/ --profile $PROFILE --exclude *.git/* --exclude *.swp
aws s3 sync ./builds/ s3://$BUCKET/builds/ --profile $PROFILE --exclude *.git/* --exclude *.swp
