[comment]: # "Auto-generated SOAR connector documentation"
# Alibaba RAM

Publisher: Splunk  
Connector Version: 2.0.7  
Product Vendor: Alibaba  
Product Name: Alibaba Resource Access Management  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 6.2.1  

This app integrates with Alibaba Resource Access Management (Alibaba RAM) to support various containment, corrective, and investigate actions

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Alibaba Resource Access Management asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access_key** |  required  | password | Access Key ID
**secret_key** |  required  | password | Secret Access key
**region_id** |  required  | string | Region ID

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
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.limit | numeric |  |   100 
action_result.data.\*.Comments | string |  |   Test Comment 
action_result.data.\*.CreateDate | string |  |   2019-07-19T04:28:48Z 
action_result.data.\*.DisplayName | string |  `alibabaram user display name`  |   test1 
action_result.data.\*.UpdateDate | string |  |   2019-07-19T04:28:48Z 
action_result.data.\*.UserId | string |  |   291581163510528087 
action_result.data.\*.UserName | string |  `alibabaram user name`  |   test1 
action_result.summary.total_users | numeric |  |   3 
action_result.message | string |  |   Total users: 3 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list roles'
List the RAM roles

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**limit** |  optional  | Maximum number of RAM roles to be fetched | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.limit | numeric |  |   100 
action_result.data.\*.Arn | string |  |   acs:ram::5211362082633686:role/test 
action_result.data.\*.CreateDate | string |  |   2019-07-19T04:32:18Z 
action_result.data.\*.Description | string |  |   This is created for testing 
action_result.data.\*.MaxSessionDuration | numeric |  |  
action_result.data.\*.RoleId | string |  |   386284258992406563 
action_result.data.\*.RoleName | string |  `alibabaram role name`  |   test 
action_result.data.\*.UpdateDate | string |  |  
action_result.summary.total_roles | numeric |  |   2 
action_result.message | string |  |   Total roles: 2 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list groups'
List the RAM user groups

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**limit** |  optional  | Maximum number of RAM user groups to be fetched | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.limit | numeric |  |   100 
action_result.data.\*.Comments | string |  |   Test group for Alibaba 
action_result.data.\*.CreateDate | string |  |   2019-07-02T20:39:17Z 
action_result.data.\*.GroupId | string |  |  
action_result.data.\*.GroupName | string |  `alibabaram group name`  |   alibaba-test-group 
action_result.data.\*.UpdateDate | string |  |   2019-07-02T20:39:17Z 
action_result.summary.total_groups | numeric |  |   3 
action_result.message | string |  |   Total groups: 3 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list policies'
List the RAM policies

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**limit** |  optional  | Maximum number of RAM policies to be fetched | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.limit | numeric |  |   15 
action_result.data.\*.AttachmentCount | numeric |  |   2 
action_result.data.\*.CreateDate | string |  |   2015-04-28T16:15:44Z 
action_result.data.\*.DefaultVersion | string |  |   v1 
action_result.data.\*.Description | string |  |   This is test description 
action_result.data.\*.PolicyName | string |  `alibabaram policy name`  |   AdministratorAccess 
action_result.data.\*.PolicyType | string |  `alibabaram policy type`  |   System 
action_result.data.\*.UpdateDate | string |  |   2017-04-27T16:48:07Z 
action_result.summary.total_policies | numeric |  |   15 
action_result.message | string |  |   Total policies: 15 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'add user'
Add a user to the provided group

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_name** |  required  | Username of the user | string |  `alibabaram user name` 
**group_name** |  required  | Name of the group | string |  `alibabaram group name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.group_name | string |  `alibabaram group name`  |   test1 
action_result.parameter.user_name | string |  `alibabaram user name`  |   test1 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   User: test1 is successfully added to the group: test1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'remove user'
Remove a user from the provided group

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_name** |  required  | Username of the user | string |  `alibabaram user name` 
**group_name** |  required  | Name of the group | string |  `alibabaram group name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.group_name | string |  `alibabaram group name`  |   test1 
action_result.parameter.user_name | string |  `alibabaram user name`  |   test1 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   User: test1 is successfully removed from the group: test1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'attach policy'
Attach a policy to the provided user, group, or role

Type: **generic**  
Read only: **False**

User can either attach the System or the Custom policies of the required entity one at a time but not both together. If the user provides user_name, group_name, and role_name parameters, the policies will be attached for all three entities, first it will attach for user_name then group_name followed by role_name. If the action fails at an intermediate stage, the policies attachment process until that point of time cannot be undone. i.e. if the policy attachment process is successful for the given user_name, group_name but fails while attaching policies for the role_name, then, policies already attached to the user and the group, in the earlier steps cannot be undone.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**policy_name** |  required  | Name of the policy | string |  `alibabaram policy name` 
**policy_type** |  required  | Type of the policy | string |  `alibabaram policy type` 
**user_name** |  optional  | Username of the user | string |  `alibabaram user name` 
**group_name** |  optional  | Name of the group | string |  `alibabaram group name` 
**role_name** |  optional  | Name of the role | string |  `alibabaram role name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.group_name | string |  `alibabaram group name`  |   test1 
action_result.parameter.policy_name | string |  `alibabaram policy name`  |   AliyunMTSFullAccess 
action_result.parameter.policy_type | string |  `alibabaram policy type`  |   System 
action_result.parameter.role_name | string |  `alibabaram role name`  |   test 
action_result.parameter.user_name | string |  `alibabaram user name`  |   test1 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   Policy: AliyunMTSFullAccess is successfully attached to the user: test1, group: test1, and role: test 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'detach policy'
Detach a policy from the provided user, group, or role

Type: **generic**  
Read only: **False**

User can either detach the System or the Custom policies of the required entity one at a time but not both together. If the user provides user_name, group_name, and role_name parameters, the policies will be detached for all three entities, first it will detach for user_name then group_name followed by role_name. If the action fails at an intermediate stage, the policies detachment process until that point of time cannot be undone. i.e. if the policy detachment process is successful for the given user_name, group_name but fails while detaching policies for the role_name, then, policies already detached from the user and the group, in the earlier steps cannot be undone.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**policy_name** |  required  | Name of the policy | string |  `alibabaram policy name` 
**policy_type** |  required  | Type of the policy | string |  `alibabaram policy type` 
**user_name** |  optional  | Username of the user | string |  `alibabaram user name` 
**group_name** |  optional  | Name of the group | string |  `alibabaram group name` 
**role_name** |  optional  | Name of the role | string |  `alibabaram role name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.group_name | string |  `alibabaram group name`  |   test1 
action_result.parameter.policy_name | string |  `alibabaram policy name`  |   AliyunMTSFullAccess 
action_result.parameter.policy_type | string |  `alibabaram policy type`  |   System 
action_result.parameter.role_name | string |  `alibabaram role name`  |   test 
action_result.parameter.user_name | string |  `alibabaram user name`  |   test1 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   Policy: AliyunMTSFullAccess is successfully detached from the user: test1, group: test1, and role: test 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'describe user'
Fetch the user details, details of the associated user groups, and user policies

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_name** |  required  | Username of the user | string |  `alibabaram user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.user_name | string |  `alibabaram user name`  |   test1 
action_result.data.\*.Comments | string |  |   This is test comment 
action_result.data.\*.CreateDate | string |  |   2019-07-19T04:28:48Z 
action_result.data.\*.DisplayName | string |  `alibabaram user display name`  |   test1 
action_result.data.\*.Email | string |  `email`  |   test1@5211362082633686.onaliyun.com 
action_result.data.\*.LastLoginDate | string |  |   2019-07-18T04:28:48Z 
action_result.data.\*.MobilePhone | string |  |   1-4153203200 
action_result.data.\*.UpdateDate | string |  |   2019-07-19T04:28:48Z 
action_result.data.\*.UserId | string |  |   291581163510528087 
action_result.data.\*.UserName | string |  `alibabaram user name`  |   test1 
action_result.data.\*.user_groups.\*.Comments | string |  |   This group is created for testing purpose 
action_result.data.\*.user_groups.\*.GroupName | string |  `alibabaram group name`  |   test_1 
action_result.data.\*.user_groups.\*.JoinDate | string |  |   2019-07-19T04:29:13Z 
action_result.data.\*.user_policies.\*.AttachDate | string |  |   2019-07-22T07:57:36Z 
action_result.data.\*.user_policies.\*.DefaultVersion | string |  |   v1 
action_result.data.\*.user_policies.\*.Description | string |  |   This is sample testing description 
action_result.data.\*.user_policies.\*.PolicyName | string |  |   AdministratorAccess 
action_result.data.\*.user_policies.\*.PolicyType | string |  |   System 
action_result.summary | string |  |  
action_result.message | string |  |   Successfully fetched the details of the user: test1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'describe group'
List all policies and users details for the provided group name

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**group_name** |  required  | Name of the group | string |  `alibabaram group name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.group_name | string |  `alibabaram group name`  |   test1 
action_result.data.\*.policies.\*.AttachDate | string |  |   2019-07-19T04:29:45Z 
action_result.data.\*.policies.\*.DefaultVersion | string |  |   v2 
action_result.data.\*.policies.\*.Description | string |  |   This is test description 
action_result.data.\*.policies.\*.PolicyName | string |  `alibabaram policy name`  |   ReadOnlyAccess 
action_result.data.\*.policies.\*.PolicyType | string |  `alibabaram policy type`  |   System 
action_result.data.\*.users.\*.DisplayName | string |  `alibabaram user display name`  |   test_1 
action_result.data.\*.users.\*.JoinDate | string |  |   2019-07-19T04:29:03Z 
action_result.data.\*.users.\*.UserName | string |  `alibabaram user name`  |   test_1 
action_result.summary.total_policies | numeric |  |   2 
action_result.summary.total_users | numeric |  |   2 
action_result.message | string |  |   Total policies: 2, Total users: 2 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'replace groups'
Replace all the existing groups of the user with the provided groups

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_name** |  required  | Username of the user | string |  `alibabaram user name` 
**groups** |  required  | Comma-separated list of group names | string |  `alibabaram groups` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.groups | string |  `alibabaram groups`  |   test1,test_blank 
action_result.parameter.user_name | string |  `alibabaram user name`  |   test1 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   Provided groups are successfully replaced for the user: test1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'replace policies'
Replace all the existing policies of the user or the group with the provided policies

Type: **generic**  
Read only: **False**

User can either replace the System or the Custom policies of the required entity one at a time but not both together. If the user provides both the user_name and the group_name parameters, the policies will be replaced for both the entities. If the action fails at an intermediate stage, the policies replacement process until that point of time cannot be undone. i.e. if the policy replacement process is successful for the given user_name and fails while replacing policies for the group_name, then, policies already replaced for the users in the earlier steps cannot be undone.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_name** |  optional  | Username of the user | string |  `alibabaram user name` 
**group_name** |  optional  | Name of the group | string |  `alibabaram group name` 
**policies** |  required  | Comma-separated list of policy names | string |  `alibabaram policies` 
**policy_type** |  required  | Type of the policy | string |  `alibabaram policy type` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.group_name | string |  `alibabaram group name`  |   test1 
action_result.parameter.policies | string |  `alibabaram policies`  |   AliyunOSSFullAccess,AliyunRDSFullAccess 
action_result.parameter.policy_type | string |  `alibabaram policy type`  |   System 
action_result.parameter.user_name | string |  `alibabaram user name`  |   test1 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   Provided policies are successfully replaced for the user: test1 and group: test1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'remove policies'
Remove all the existing policies of the provided user

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_name** |  required  | Username of the user | string |  `alibabaram user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.user_name | string |  `alibabaram user name`  |   test1 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   Successfully removed all the policies from the user: test1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'remove groups'
Remove all the associations of the groups from the provided user

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_name** |  required  | Username of the user | string |  `alibabaram user name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.user_name | string |  `alibabaram user name`  |   test1 
action_result.data | string |  |  
action_result.summary | string |  |  
action_result.message | string |  |   Successfully removed all the group associations of the user: test1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'update user'
Updates the basic information of the RAM user

Type: **generic**  
Read only: **False**

As per the API document of Alibaba RAM, the parameter new_username is not mandatory for running the action update user and hence, it has been kept optional in the action. But, the API used here still gives an error mentioning that new_username is mandatory if we do not provide the value for new_username. The mobile_number parameter should follow the format <International Area Code>-<Mobile Phone Number> e.g. 86-18600001234.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**user_name** |  required  | Username of the user | string |  `alibabaram user name` 
**comment** |  optional  | The comment for updating the RAM user details | string | 
**email** |  optional  | Updated email of the RAM user | string |  `email` 
**mobile_number** |  optional  | Updated mobile number of the RAM user | string | 
**new_username** |  optional  | Updated username of the RAM user | string |  `alibabaram user name` 
**display_name** |  optional  | Updated display name of the RAM user | string |  `alibabaram user display name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.comment | string |  |   This is a test comment for updating existing user 
action_result.parameter.display_name | string |  `alibabaram user display name`  |   Test1_New 
action_result.parameter.email | string |  `email`  |   test1_new@5211362082633686.onaliyun.com 
action_result.parameter.mobile_number | string |  |   1-4155096996 
action_result.parameter.new_username | string |  `alibabaram user name`  |   test1_new 
action_result.parameter.user_name | string |  `alibabaram user name`  |   test1 
action_result.data.\*.Comments | string |  |   This is a test comment for updating existing user 
action_result.data.\*.CreateDate | string |  |   2019-07-19T04:28:48Z 
action_result.data.\*.DisplayName | string |  `alibabaram user display name`  |   Test1_New 
action_result.data.\*.Email | string |  `email`  |   test1_new@5211362082633686.onaliyun.com 
action_result.data.\*.MobilePhone | string |  |   1-4155096996 
action_result.data.\*.UpdateDate | string |  |   2019-07-22T02:36:18Z 
action_result.data.\*.UserId | string |  |   291581163510528087 
action_result.data.\*.UserName | string |  `alibabaram user name`  |   test1_new 
action_result.summary | string |  |  
action_result.message | string |  |   Successfully updated the details for the User: test1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 