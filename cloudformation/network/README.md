# [CloudFormation](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)

## Terminology
1. **Template**: The descriptive syntax json files describing the resources to be built. 
2. **Stack**: Collection of resources built from a Template. 
3. **Top-Level Stack**: A stack that contains or controls other stacks. 
4. **Resource**: Any "thing" in aws. 
5. **Parameter**: Input to a Template or Stack. 
6. **Mapping**: Two Level hash map or dictionary containing static information 
7. **Conditional**: Binary logic within the Template. 
8. **Outputs**: Data output by stack after completion, useful for tying outputs from one stack to inputs of another in a nested template. 
9. **Intrinsic Functions**: Functions evaluated by the template, like references to other resources. [Intrinsic Functions Docs](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html)
10. **Pseudo Parameters**: Parameters provided from AWS like Environment parameters to the stack these are things like Region being ran in etc. [Pseudo Parameter Docs](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html)
   [Template Anatomy](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html)

## CloudFormation Layout
The Top.json files are top level nested stacks that allow us to build stacks off different CloudFromation templates. Parameters or input to this stack determine how the template is evaluated and what resources the template creates. 
[Nested Stacks RBN Blog](http://www.rightbrainnetworks.com/blog/cloudformation-zen-nested-stacks/)

In side the Top.json stack you will find all of child stacks that make up the Network. Each of these stacks references a template within your repository. The name of the template is descriptive of what's it will build. This is a modular template that will build like infrastructure for stacks. These templates are used as building blocks for the Top Template to manipulate and build the Network.

## Making Changes
This Repository follows [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).

**Branch before you make any changes.**

[AWS Resource Reference](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)
