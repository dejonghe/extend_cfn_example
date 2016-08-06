# Return True
All this lambda does is return success to CloudFormation, useful for sticky situations. 
If ever you mess up your Custom Resource and your CloudFormation stack hangs, build this lambda, manually upload the code over your lambda that is not returning, and re run your rollback or delete. 
