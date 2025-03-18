# File: alibabaram_consts.py
#
# Copyright (c) 2019-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Define your constants here
ALIBABARAM_MAX_ITEMS = 1000
ALIBABARAM_JSON_KEY = "json"
ALIBABARAM_JSON_FROM = "from"
ALIBABARAM_JSON_TO = "to"
ALIBABARAM_JSON_MARKER = "Marker"
ALIBABARAM_JSON_IS_TRUNCATED = "IsTruncated"
ALIBABARAM_JSON_ACCESS_KEY = "access_key"
ALIBABARAM_JSON_SECRET_KEY = "secret_key"  # pragma: allowlist secret
ALIBABARAM_JSON_REGION_ID = "region_id"
ALIBABARAM_JSON_LIMIT = "limit"
ALIBABARAM_JSON_USERS = "Users"
ALIBABARAM_JSON_USER = "User"
ALIBABARAM_JSON_GROUP = "Group"
ALIBABARAM_JSON_ROLES = "Roles"
ALIBABARAM_JSON_GROUPS = "Groups"
ALIBABARAM_JSON_POLICIES = "Policies"
ALIBABARAM_JSON_USER_NAME = "user_name"
ALIBABARAM_JSON_GROUP_NAME = "group_name"
ALIBABARAM_JSON_ROLE_NAME = "role_name"
ALIBABARAM_JSON_POLICY_NAME = "policy_name"
ALIBABARAM_JSON_POLICY_TYPE = "policy_type"
ALIBABARAM_JSON_DISPLAY_NAME = "display_name"
ALIBABARAM_JSON_COMMENT = "comment"
ALIBABARAM_JSON_EMAIL = "email"
ALIBABARAM_JSON_MOBILE_NUMBER = "mobile_number"
ALIBABARAM_JSON_NEW_USER_NAME = "new_username"
ALIBABARAM_POLICY_NAME = "PolicyName"
ALIBABARAM_POLICY_TYPE = "PolicyType"
ALIBABARAM_GROUP_NAME = "GroupName"
ALIBABARAM_JSON_USER_GROUPS = "user_groups"
ALIBABARAM_JSON_USER_POLICIES = "user_policies"
ALIBABARAM_PROCESS_ATTACHING = "attaching"
ALIBABARAM_PROCESS_DETACHING = "detaching"
ALIBABARAM_JSON_ADDING = "adding"
ALIBABARAM_JSON_REMOVING = "removing"
ALIBABARAM_DEFAULT_REGION = "cn-hangzhou"
ALIBABARAM_REGIONS_MAPPING = {
    "Asia Pacific NE 1": "ap-northeast-1",
    "Asia Pacific SE 1": "ap-southeast-1",
    "Asia Pacific SE 2": "ap-southeast-2",
    "Asia Pacific SE 3": "ap-southeast-3",
    "Asia Pacific SE 5": "ap-southeast-5",
    "Asia Pacific SOU 1": "ap-south-1",
    "China East 1": "cn-hangzhou",
    "China East 2": "cn-shanghai",
    "China North 1": "cn-qingdao",
    "China North 2": "cn-beijing",
    "China North 3": "cn-zhangjiakou",
    "China North 5": "cn-huhehaote",
    "China South 1": "cn-shenzhen",
    "China SW 1": "cn-chengdu",
    "EU Central 1": "eu-central-1",
    "Hong Kong": "cn-hongkong",
    "Middle East 1": "me-east-1",
    "UK (London)": "eu-west-1",
    "US East 1": "us-east-1",
    "US West 1": "us-west-1",
}
ALIBABARAM_JSON_ACTIONS_RESPONSE_MAPPING = {"Users": "User", "Roles": "Role", "Groups": "Group", "Policies": "Policy"}
DEFAULT_REQUEST_TIMEOUT = 30  # in seconds
ALIBABARAM_INVALID_INTEGER = "Please provide non-zero positive integer in {parameter}"
ALIBABARAM_ERROR_CREATING_REQUEST = (
    "Error occurred while creating request for fetching the {item_name} associated with the given RAM {target_item}. Error: {error}"
)
ALIBABARAM_ERROR_ATTACH_DETACH_POLICY = "Error occurred while {pr} policy: {pol} the {itn}: {it}. Error: {err}"
ALIBABARAM_ERROR_ADD_REMOVE_GROUP = "Error occurred while {pr} user: {user} the group: {group}. Error: {err}"
ALIBABARAM_ATTACH_POLICY_MSG = "Policy: {pol} is successfully attached to the user: {user}, group: {grp}, and role: {role}"
ALIBABARAM_DETACH_POLICY_MSG = "Policy: {pol} is successfully detached from the user: {user}, group: {grp}, and role: {role}"
ALIBABARAM_REPLACE_POLICY_MSG = "Provided policies are successfully replaced for the user: {user} and group: {grp}"
ALIBABARAM_REPLACE_GROUP_MSG = "Provided groups are successfully replaced for the user: {user}"
ALIBABARAM_INVALID_POLICY_TYPES = (
    "Mis-match in type of the policy: {pol}. Original policy type is: {curr_type} and "
    "the provided policy type in action parameters is: {prov_type}"
)
