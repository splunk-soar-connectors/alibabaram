[comment]: # "Auto-generated SOAR connector documentation"
# Alibaba RAM

Publisher: Splunk  
Connector Version: 2\.0\.5  
Product Vendor: Alibaba  
Product Name: Alibaba Resource Access Management  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.1\.0  

This app integrates with Alibaba Resource Access Management \(Alibaba RAM\) to support various containment, corrective, and investigate actions

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Alibaba Resource Access Management asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access\_key** |  required  | password | Access Key ID
**secret\_key** |  required  | password | Secret Access key
**region\_id** |  required  | string | Region ID

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[list users](#action-list-users) - List the RAM users  
[list roles](#action-list-roles) - List the RAM roles  
[list groups](#action-list-groups) - List the RAM user groups  
[list policies](#action-list-policies) - List the RAM policies  
[add user](#action-add-user) - Add a user to the provided group  
[remove user](#action-remove-user) - Remove a user from the provided group  
[attach policy](#action-attach-policy) - Attach a policy to the provided user, group, or role  
[detach policy](#action-detach-policy) - Detach a policy from the provided user, group, or role  
[describe user](#action-describe-user) - Fetch the user details, details of the associated user groups, and user policies  
[describe group](#action-describe-group) - List all policies and users details for the provided group name  
[replace groups](#action-replace-groups) - Replace all the existing groups of the user with the provided groups  
[replace policies](#action-replace-policies) - Replace all the existing policies of the user or the group with the provided policies  
[remove policies](#action-remove-policies) - Remove all the existing policies of the provided user  
[remove groups](#action-remove-groups) - Remove all the associations of the groups from the provided user  
[update user](#action-update-user) - Updates the basic information of the RAM user  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list users'
List the RAM users

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**limit** |  optional  | Maximum number of RAM users to be fetched | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.data\.\*\.Comments | string | 
action\_result\.data\.\*\.CreateDate | string | 
action\_result\.data\.\*\.DisplayName | string |  `alibabaram user display name` 
action\_result\.data\.\*\.UpdateDate | string | 
action\_result\.data\.\*\.UserId | string | 
action\_result\.data\.\*\.UserName | string |  `alibabaram user name` 
action\_result\.summary\.total\_users | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list roles'
List the RAM roles

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**limit** |  optional  | Maximum number of RAM roles to be fetched | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.data\.\*\.Arn | string | 
action\_result\.data\.\*\.CreateDate | string | 
action\_result\.data\.\*\.Description | string | 
action\_result\.data\.\*\.MaxSessionDuration | numeric | 
action\_result\.data\.\*\.RoleId | string | 
action\_result\.data\.\*\.RoleName | string |  `alibabaram role name` 
action\_result\.data\.\*\.UpdateDate | string | 
action\_result\.summary\.total\_roles | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list groups'
List the RAM user groups

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**limit** |  optional  | Maximum number of RAM user groups to be fetched | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.data\.\*\.Comments | string | 
action\_result\.data\.\*\.CreateDate | string | 
action\_result\.data\.\*\.GroupId | string | 
action\_result\.data\.\*\.GroupName | string |  `alibabaram group name` 
action\_result\.data\.\*\.UpdateDate | string | 
action\_result\.summary\.total\_groups | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list policies'
List the RAM policies

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**limit** |  optional  | Maximum number of RAM policies to be fetched | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.data\.\*\.AttachmentCount | numeric | 
action\_result\.data\.\*\.CreateDate | string | 
action\_result\.data\.\*\.DefaultVersion | string | 
action\_result\.data\.\*\.Description | string | 
action\_result\.data\.\*\.PolicyName | string |  `alibabaram policy name` 
action\_result\.data\.\*\.PolicyType | string |  `alibabaram policy type` 
action\_result\.data\.\*\.UpdateDate | string | 
action\_result\.summary\.total\_policies | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add user'
Add a user to the provided group

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user\_name** |  required  | Username of the user | string |  `alibabaram user name` 
**group\_name** |  required  | Name of the group | string |  `alibabaram group name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.group\_name | string |  `alibabaram group name` 
action\_result\.parameter\.user\_name | string |  `alibabaram user name` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove user'
Remove a user from the provided group

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user\_name** |  required  | Username of the user | string |  `alibabaram user name` 
**group\_name** |  required  | Name of the group | string |  `alibabaram group name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.group\_name | string |  `alibabaram group name` 
action\_result\.parameter\.user\_name | string |  `alibabaram user name` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'attach policy'
Attach a policy to the provided user, group, or role

Type: **generic**  
Read only: **False**

User can either attach the System or the Custom policies of the required entity one at a time but not both together\. If the user provides user\_name, group\_name, and role\_name parameters, the policies will be attached for all three entities, first it will attach for user\_name then group\_name followed by role\_name\. If the action fails at an intermediate stage, the policies attachment process until that point of time cannot be undone\. i\.e\. if the policy attachment process is successful for the given user\_name, group\_name but fails while attaching policies for the role\_name, then, policies already attached to the user and the group, in the earlier steps cannot be undone\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**policy\_name** |  required  | Name of the policy | string |  `alibabaram policy name` 
**policy\_type** |  required  | Type of the policy | string |  `alibabaram policy type` 
**user\_name** |  optional  | Username of the user | string |  `alibabaram user name` 
**group\_name** |  optional  | Name of the group | string |  `alibabaram group name` 
**role\_name** |  optional  | Name of the role | string |  `alibabaram role name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.group\_name | string |  `alibabaram group name` 
action\_result\.parameter\.policy\_name | string |  `alibabaram policy name` 
action\_result\.parameter\.policy\_type | string |  `alibabaram policy type` 
action\_result\.parameter\.role\_name | string |  `alibabaram role name` 
action\_result\.parameter\.user\_name | string |  `alibabaram user name` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'detach policy'
Detach a policy from the provided user, group, or role

Type: **generic**  
Read only: **False**

User can either detach the System or the Custom policies of the required entity one at a time but not both together\. If the user provides user\_name, group\_name, and role\_name parameters, the policies will be detached for all three entities, first it will detach for user\_name then group\_name followed by role\_name\. If the action fails at an intermediate stage, the policies detachment process until that point of time cannot be undone\. i\.e\. if the policy detachment process is successful for the given user\_name, group\_name but fails while detaching policies for the role\_name, then, policies already detached from the user and the group, in the earlier steps cannot be undone\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**policy\_name** |  required  | Name of the policy | string |  `alibabaram policy name` 
**policy\_type** |  required  | Type of the policy | string |  `alibabaram policy type` 
**user\_name** |  optional  | Username of the user | string |  `alibabaram user name` 
**group\_name** |  optional  | Name of the group | string |  `alibabaram group name` 
**role\_name** |  optional  | Name of the role | string |  `alibabaram role name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.group\_name | string |  `alibabaram group name` 
action\_result\.parameter\.policy\_name | string |  `alibabaram policy name` 
action\_result\.parameter\.policy\_type | string |  `alibabaram policy type` 
action\_result\.parameter\.role\_name | string |  `alibabaram role name` 
action\_result\.parameter\.user\_name | string |  `alibabaram user name` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'describe user'
Fetch the user details, details of the associated user groups, and user policies

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user\_name** |  required  | Username of the user | string |  `alibabaram user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.user\_name | string |  `alibabaram user name` 
action\_result\.data\.\*\.Comments | string | 
action\_result\.data\.\*\.CreateDate | string | 
action\_result\.data\.\*\.DisplayName | string |  `alibabaram user display name` 
action\_result\.data\.\*\.Email | string |  `email` 
action\_result\.data\.\*\.LastLoginDate | string | 
action\_result\.data\.\*\.MobilePhone | string | 
action\_result\.data\.\*\.UpdateDate | string | 
action\_result\.data\.\*\.UserId | string | 
action\_result\.data\.\*\.UserName | string |  `alibabaram user name` 
action\_result\.data\.\*\.user\_groups\.\*\.Comments | string | 
action\_result\.data\.\*\.user\_groups\.\*\.GroupName | string |  `alibabaram group name` 
action\_result\.data\.\*\.user\_groups\.\*\.JoinDate | string | 
action\_result\.data\.\*\.user\_policies\.\*\.AttachDate | string | 
action\_result\.data\.\*\.user\_policies\.\*\.DefaultVersion | string | 
action\_result\.data\.\*\.user\_policies\.\*\.Description | string | 
action\_result\.data\.\*\.user\_policies\.\*\.PolicyName | string | 
action\_result\.data\.\*\.user\_policies\.\*\.PolicyType | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'describe group'
List all policies and users details for the provided group name

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**group\_name** |  required  | Name of the group | string |  `alibabaram group name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.group\_name | string |  `alibabaram group name` 
action\_result\.data\.\*\.policies\.\*\.AttachDate | string | 
action\_result\.data\.\*\.policies\.\*\.DefaultVersion | string | 
action\_result\.data\.\*\.policies\.\*\.Description | string | 
action\_result\.data\.\*\.policies\.\*\.PolicyName | string |  `alibabaram policy name` 
action\_result\.data\.\*\.policies\.\*\.PolicyType | string |  `alibabaram policy type` 
action\_result\.data\.\*\.users\.\*\.DisplayName | string |  `alibabaram user display name` 
action\_result\.data\.\*\.users\.\*\.JoinDate | string | 
action\_result\.data\.\*\.users\.\*\.UserName | string |  `alibabaram user name` 
action\_result\.summary\.total\_policies | numeric | 
action\_result\.summary\.total\_users | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'replace groups'
Replace all the existing groups of the user with the provided groups

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user\_name** |  required  | Username of the user | string |  `alibabaram user name` 
**groups** |  required  | Comma\-separated list of group names | string |  `alibabaram groups` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.groups | string |  `alibabaram groups` 
action\_result\.parameter\.user\_name | string |  `alibabaram user name` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'replace policies'
Replace all the existing policies of the user or the group with the provided policies

Type: **generic**  
Read only: **False**

User can either replace the System or the Custom policies of the required entity one at a time but not both together\. If the user provides both the user\_name and the group\_name parameters, the policies will be replaced for both the entities\. If the action fails at an intermediate stage, the policies replacement process until that point of time cannot be undone\. i\.e\. if the policy replacement process is successful for the given user\_name and fails while replacing policies for the group\_name, then, policies already replaced for the users in the earlier steps cannot be undone\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user\_name** |  optional  | Username of the user | string |  `alibabaram user name` 
**group\_name** |  optional  | Name of the group | string |  `alibabaram group name` 
**policies** |  required  | Comma\-separated list of policy names | string |  `alibabaram policies` 
**policy\_type** |  required  | Type of the policy | string |  `alibabaram policy type` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.group\_name | string |  `alibabaram group name` 
action\_result\.parameter\.policies | string |  `alibabaram policies` 
action\_result\.parameter\.policy\_type | string |  `alibabaram policy type` 
action\_result\.parameter\.user\_name | string |  `alibabaram user name` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove policies'
Remove all the existing policies of the provided user

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user\_name** |  required  | Username of the user | string |  `alibabaram user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.user\_name | string |  `alibabaram user name` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove groups'
Remove all the associations of the groups from the provided user

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user\_name** |  required  | Username of the user | string |  `alibabaram user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.user\_name | string |  `alibabaram user name` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'update user'
Updates the basic information of the RAM user

Type: **generic**  
Read only: **False**

As per the API document of Alibaba RAM, the parameter new\_username is not mandatory for running the action update user and hence, it has been kept optional in the action\. But, the API used here still gives an error mentioning that new\_username is mandatory if we do not provide the value for new\_username\. The mobile\_number parameter should follow the format <International Area Code>\-<Mobile Phone Number> e\.g\. 86\-18600001234\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user\_name** |  required  | Username of the user | string |  `alibabaram user name` 
**comment** |  optional  | The comment for updating the RAM user details | string | 
**email** |  optional  | Updated email of the RAM user | string |  `email` 
**mobile\_number** |  optional  | Updated mobile number of the RAM user | string | 
**new\_username** |  optional  | Updated username of the RAM user | string |  `alibabaram user name` 
**display\_name** |  optional  | Updated display name of the RAM user | string |  `alibabaram user display name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.comment | string | 
action\_result\.parameter\.display\_name | string |  `alibabaram user display name` 
action\_result\.parameter\.email | string |  `email` 
action\_result\.parameter\.mobile\_number | string | 
action\_result\.parameter\.new\_username | string |  `alibabaram user name` 
action\_result\.parameter\.user\_name | string |  `alibabaram user name` 
action\_result\.data\.\*\.Comments | string | 
action\_result\.data\.\*\.CreateDate | string | 
action\_result\.data\.\*\.DisplayName | string |  `alibabaram user display name` 
action\_result\.data\.\*\.Email | string |  `email` 
action\_result\.data\.\*\.MobilePhone | string | 
action\_result\.data\.\*\.UpdateDate | string | 
action\_result\.data\.\*\.UserId | string | 
action\_result\.data\.\*\.UserName | string |  `alibabaram user name` 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 