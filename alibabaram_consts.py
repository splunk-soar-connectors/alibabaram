# File: alibabaram_consts.py
# Copyright (c) 2019 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
# Define your constants here

ALIBABARAM_JSON_KEY = "json"
ALIBABARAM_JSON_MARKER = "Marker"
ALIBABARAM_JSON_IS_TRUNCATED = "IsTruncated"
ALIBABARAM_JSON_ACCESS_KEY = "access_key"
ALIBABARAM_JSON_SECRET_KEY = "secret_key"
ALIBABARAM_JSON_REGION_ID = "region_id"
ALIBABARAM_JSON_LIMIT = "limit"
ALIBABARAM_JSON_USERS = "Users"
ALIBABARAM_JSON_ROLES = "Roles"
ALIBABARAM_JSON_GROUPS = "Groups"
ALIBABARAM_JSON_POLICIES = "Policies"
ALIBABARAM_JSON_GROUP_NAME = "group_name"
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
        "US West 1": "us-west-1"
}
ALIBABARAM_JSON_ACTIONS_RESPONSE_MAPPING = {
        "Users": "User",
        "Roles": "Role",
        "Groups": "Group",
        "Policies": "Policy"
}
ALIBABARAM_INVALID_INTEGER = 'Please provide non-zero positive integer in {parameter}'
ALIBABARAM_ERROR_CREATING_REQUEST = 'Error occurred while creating request for fetching the {item_name} associated with the given RAM group. Error: {error}'
