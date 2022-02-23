# File: alibabaram_connector.py
#
# Copyright (c) 2019-2021 Splunk Inc.
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
# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

import requests
import json
from alibabaram_consts import *
from aliyunsdkcore.client import AcsClient
from aliyunsdkram.request.v20150501.UpdateUserRequest import UpdateUserRequest
from aliyunsdkram.request.v20150501.ListUsersRequest import ListUsersRequest
from aliyunsdkram.request.v20150501.ListRolesRequest import ListRolesRequest
from aliyunsdkram.request.v20150501.ListGroupsRequest import ListGroupsRequest
from aliyunsdkram.request.v20150501.ListPoliciesRequest import ListPoliciesRequest
from aliyunsdkram.request.v20150501.ListUsersForGroupRequest import ListUsersForGroupRequest
from aliyunsdkram.request.v20150501.ListPoliciesForGroupRequest import ListPoliciesForGroupRequest
from aliyunsdkram.request.v20150501.AddUserToGroupRequest import AddUserToGroupRequest
from aliyunsdkram.request.v20150501.RemoveUserFromGroupRequest import RemoveUserFromGroupRequest
from aliyunsdkram.request.v20150501.AttachPolicyToGroupRequest import AttachPolicyToGroupRequest
from aliyunsdkram.request.v20150501.AttachPolicyToRoleRequest import AttachPolicyToRoleRequest
from aliyunsdkram.request.v20150501.AttachPolicyToUserRequest import AttachPolicyToUserRequest
from aliyunsdkram.request.v20150501.DetachPolicyFromUserRequest import DetachPolicyFromUserRequest
from aliyunsdkram.request.v20150501.DetachPolicyFromGroupRequest import DetachPolicyFromGroupRequest
from aliyunsdkram.request.v20150501.DetachPolicyFromRoleRequest import DetachPolicyFromRoleRequest
from aliyunsdkram.request.v20150501.GetUserRequest import GetUserRequest
from aliyunsdkram.request.v20150501.ListGroupsForUserRequest import ListGroupsForUserRequest
from aliyunsdkram.request.v20150501.ListPoliciesForUserRequest import ListPoliciesForUserRequest


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class AlibabaRamConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(AlibabaRamConnector, self).__init__()

        self._state = None
        self._access_key = None
        self._secret_key = None
        self._region_id = None
        self._client = None

    def _paginator(self, item_name, ram_request, limit, action_result, set_max_items=True):

        list_items = list()
        next_token = None

        if set_max_items:
            ram_request.set_MaxItems(ALIBABARAM_MAX_ITEMS)

        while True:
            try:
                if next_token:
                    ram_request.set_Marker(next_token)
                    next_token = None

                response = self._client.do_action_with_exception(ram_request)
            except Exception as e:
                action_result.set_status(phantom.APP_ERROR,
                    'Error occurred while fetching the list of all the RAM {0}. Error: {1}'.format(item_name, str(e)))
                return None

            try:
                resp_json = json.loads(response)
            except Exception as e:
                action_result.set_status(phantom.APP_ERROR, 'Error occurred while parsing the response JSON. Error: {0}'.format(str(e)))
                return None

            if resp_json and resp_json.get(item_name) and resp_json.get(item_name).get(ALIBABARAM_JSON_ACTIONS_RESPONSE_MAPPING.get(item_name)):
                list_items.extend(resp_json.get(item_name).get(ALIBABARAM_JSON_ACTIONS_RESPONSE_MAPPING.get(item_name)))

            if limit and len(list_items) >= limit:
                return list_items[:limit]

            is_truncated = resp_json.get(ALIBABARAM_JSON_IS_TRUNCATED)
            next_token = resp_json.get(ALIBABARAM_JSON_MARKER)
            if not is_truncated:
                break

        return list_items

    def _handle_test_connectivity(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        if not self._client:
            return action_result.set_status(phantom.APP_ERROR,
                'Client could not be initialized. Please check credentials and region in the asset configuration parameters.')

        self.save_progress("Connecting the endpoint for fetching all the users")
        try:
            ram_request = ListUsersRequest()
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)

            self._client.do_action_with_exception(ram_request)
        except Exception as e:
            self.save_progress("Test Connectivity Failed")
            return action_result.set_status(phantom.APP_ERROR,
                'Error occurred while fetching the list of all the users. Error: {0}'.format(str(e)))

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_users(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))
        limit = param.get(ALIBABARAM_JSON_LIMIT)

        if (limit and not str(limit).isdigit()) or limit == 0:
            return action_result.set_status(phantom.APP_ERROR, ALIBABARAM_INVALID_INTEGER.format(parameter=ALIBABARAM_JSON_LIMIT))

        try:
            ram_request = ListUsersRequest()
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR,
                'Error occurred while creating request for fetching list of all the RAM users. Error: {0}'.format(str(e)))

        users = self._paginator(ALIBABARAM_JSON_USERS, ram_request, limit, action_result)

        if users is None:
            return action_result.get_status()

        for user in users:
            action_result.add_data(user)

        summary = action_result.update_summary({})
        summary['total_users'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_roles(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))
        limit = param.get(ALIBABARAM_JSON_LIMIT)

        if (limit and not str(limit).isdigit()) or limit == 0:
            return action_result.set_status(phantom.APP_ERROR, ALIBABARAM_INVALID_INTEGER.format(parameter=ALIBABARAM_JSON_LIMIT))

        try:
            ram_request = ListRolesRequest()
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR,
                'Error occurred while creating request for fetching list of all the RAM roles. Error: {0}'.format(str(e)))

        roles = self._paginator(ALIBABARAM_JSON_ROLES, ram_request, limit, action_result)

        if roles is None:
            return action_result.get_status()

        for role in roles:
            action_result.add_data(role)

        summary = action_result.update_summary({})
        summary['total_roles'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _list_all_groups(self, limit, action_result):
        try:
            ram_request = ListGroupsRequest()
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            action_result.set_status(phantom.APP_ERROR,
                'Error occurred while creating request for fetching list of all the RAM groups. Error: {0}'.format(str(e)))
            return None

        return self._paginator(ALIBABARAM_JSON_GROUPS, ram_request, limit, action_result)

    def _handle_list_groups(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))
        limit = param.get(ALIBABARAM_JSON_LIMIT)

        if (limit and not str(limit).isdigit()) or limit == 0:
            return action_result.set_status(phantom.APP_ERROR, ALIBABARAM_INVALID_INTEGER.format(parameter=ALIBABARAM_JSON_LIMIT))

        groups = self._list_all_groups(limit, action_result)

        if groups is None:
            return action_result.get_status()

        for group in groups:
            action_result.add_data(group)

        summary = action_result.update_summary({})
        summary['total_groups'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _list_all_policies(self, limit, action_result):
        try:
            ram_request = ListPoliciesRequest()
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            action_result.set_status(phantom.APP_ERROR,
                'Error occurred while creating request for fetching list of all the RAM policies. Error: {0}'.format(str(e)))
            return None

        return self._paginator(ALIBABARAM_JSON_POLICIES, ram_request, limit, action_result)

    def _handle_list_policies(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))
        limit = param.get(ALIBABARAM_JSON_LIMIT)

        if (limit and not str(limit).isdigit()) or limit == 0:
            return action_result.set_status(phantom.APP_ERROR, ALIBABARAM_INVALID_INTEGER.format(parameter=ALIBABARAM_JSON_LIMIT))

        policies = self._list_all_policies(limit, action_result)

        if policies is None:
            return action_result.get_status()

        for policy in policies:
            action_result.add_data(policy)

        summary = action_result.update_summary({})
        summary['total_policies'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_add_user(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))
        user_name = param.get(ALIBABARAM_JSON_USER_NAME)
        group_name = param.get(ALIBABARAM_JSON_GROUP_NAME)

        try:
            ram_request = AddUserToGroupRequest()
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
            ram_request.set_UserName(user_name)
            ram_request.set_GroupName(group_name)
            response = self._client.do_action_with_exception(ram_request)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR,
                "Error occurred while adding user: {0} to the group: {1}. Error: {2}".format(user_name, group_name, str(e)))

        if not response:
            return action_result.set_status(phantom.APP_ERROR,
                "Unknown error occurred while adding user: {0} to the group: {1}".format(user_name, group_name))

        return action_result.set_status(phantom.APP_SUCCESS,
            "User: {0} is successfully added to the group: {1}".format(user_name, group_name))

    def _handle_remove_user(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))
        user_name = param.get(ALIBABARAM_JSON_USER_NAME)
        group_name = param.get(ALIBABARAM_JSON_GROUP_NAME)

        try:
            ram_request = RemoveUserFromGroupRequest()
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
            ram_request.set_UserName(user_name)
            ram_request.set_GroupName(group_name)
            response = self._client.do_action_with_exception(ram_request)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR,
                "Error occurred while removing user: {0} from the group: {1}. Error: {2}".format(user_name, group_name, str(e)))

        if not response:
            return action_result.set_status(phantom.APP_ERROR,
                "Unknown error occurred while removing user: {0} from the group: {1}".format(user_name, group_name))

        return action_result.set_status(phantom.APP_SUCCESS,
            "User: {0} is successfully removed from the group: {1}".format(user_name, group_name))

    def _attach_detach_policy(self, policy_name, policy_type, item, item_name, action_result, is_attach=True):
        try:
            ram_request = None
            if not is_attach:
                process_name = ALIBABARAM_PROCESS_DETACHING
                process_op = ALIBABARAM_JSON_FROM
            else:
                process_name = ALIBABARAM_PROCESS_ATTACHING
                process_op = ALIBABARAM_JSON_TO

            if ALIBABARAM_JSON_USER_NAME == item_name:
                if not is_attach:
                    ram_request = DetachPolicyFromUserRequest()
                else:
                    ram_request = AttachPolicyToUserRequest()

                ram_request.set_UserName(item)
            elif ALIBABARAM_JSON_GROUP_NAME == item_name:
                if not is_attach:
                    ram_request = DetachPolicyFromGroupRequest()
                else:
                    ram_request = AttachPolicyToGroupRequest()

                ram_request.set_GroupName(item)
            else:
                if not is_attach:
                    ram_request = DetachPolicyFromRoleRequest()
                else:
                    ram_request = AttachPolicyToRoleRequest()

                ram_request.set_RoleName(item)

            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
            ram_request.set_PolicyName(policy_name)
            ram_request.set_PolicyType(policy_type)

            response = self._client.do_action_with_exception(ram_request)
        except Exception as e:
            action_result.set_status(
                    phantom.APP_ERROR, ALIBABARAM_ERROR_ATTACH_DETACH_POLICY.format(
                        pr=process_name, pol='{0} {1}'.format(policy_name, process_op), itn=item_name, it=item, err=str(e)))
            return None

        return response

    def _handle_attach_policy(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        user_name = param.get(ALIBABARAM_JSON_USER_NAME)
        group_name = param.get(ALIBABARAM_JSON_GROUP_NAME)
        role_name = param.get(ALIBABARAM_JSON_ROLE_NAME)
        policy_name = param.get(ALIBABARAM_JSON_POLICY_NAME)
        policy_type = param.get(ALIBABARAM_JSON_POLICY_TYPE)

        if not (user_name or group_name or role_name):
            return action_result.set_status(phantom.APP_ERROR,
                'Please provide at least one of the user_name, group_name, or role_name parameters')

        if user_name:
            result = self._attach_detach_policy(policy_name, policy_type, user_name, ALIBABARAM_JSON_USER_NAME, action_result)

            if not result:
                return action_result.get_status()

        if group_name:
            result = self._attach_detach_policy(policy_name, policy_type, group_name, ALIBABARAM_JSON_GROUP_NAME, action_result)

            if not result:
                return action_result.get_status()

        if role_name:
            result = self._attach_detach_policy(policy_name, policy_type, role_name, ALIBABARAM_JSON_ROLE_NAME, action_result)

            if not result:
                return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS,
            ALIBABARAM_ATTACH_POLICY_MSG.format(pol=policy_name, user=user_name, grp=group_name, role=role_name))

    def _handle_detach_policy(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        user_name = param.get(ALIBABARAM_JSON_USER_NAME)
        group_name = param.get(ALIBABARAM_JSON_GROUP_NAME)
        role_name = param.get(ALIBABARAM_JSON_ROLE_NAME)
        policy_name = param.get(ALIBABARAM_JSON_POLICY_NAME)
        policy_type = param.get(ALIBABARAM_JSON_POLICY_TYPE)

        if not (user_name or group_name or role_name):
            return action_result.set_status(phantom.APP_ERROR,
                'Please provide at least one of the user_name, group_name, or role_name parameters')

        if user_name:
            result = self._attach_detach_policy(policy_name, policy_type, user_name, ALIBABARAM_JSON_USER_NAME, action_result, False)

            if not result:
                return action_result.get_status()

        if group_name:
            result = self._attach_detach_policy(policy_name, policy_type, group_name, ALIBABARAM_JSON_GROUP_NAME, action_result, False)

            if not result:
                return action_result.get_status()

        if role_name:
            result = self._attach_detach_policy(policy_name, policy_type, role_name, ALIBABARAM_JSON_ROLE_NAME, action_result, False)

            if not result:
                return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS,
            ALIBABARAM_DETACH_POLICY_MSG.format(pol=policy_name, user=user_name, grp=group_name, role=role_name))

    def _validate_policy_types(self, policies_list, policy_type, action_result):
        all_policies = self._list_all_policies(None, action_result)

        if all_policies is None:
            action_result.set_status(phantom.APP_ERROR,
                "Error occurred while fetching all the policies for validating the type of the provided policies")
            return None

        count = 0

        for policy in all_policies:
            if policy.get(ALIBABARAM_POLICY_NAME) in policies_list and policy.get(ALIBABARAM_POLICY_TYPE) == policy_type:
                count += 1
            elif policy.get(ALIBABARAM_POLICY_NAME) in policies_list and not policy.get(ALIBABARAM_POLICY_TYPE) == policy_type:
                action_result.set_status(
                    phantom.APP_ERROR, ALIBABARAM_INVALID_POLICY_TYPES.format(
                        pol=policy.get(ALIBABARAM_POLICY_NAME), curr_type=policy.get(ALIBABARAM_POLICY_TYPE), prov_type=policy_type))
                return False

        if count != len(policies_list):
            action_result.set_status(phantom.APP_ERROR,
                "Please check the provided policies. One or more policies of the provided policy names do not exist on the server.")
            return False

        return True

    def _strip_all_user_policies(self, user_name, action_result):
        # 1. List all the current policies of the user
        try:
            ram_request = ListPoliciesForUserRequest()
            ram_request.set_UserName(user_name)
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            action_result.set_status(
                    phantom.APP_ERROR, ALIBABARAM_ERROR_CREATING_REQUEST.format(
                        item_name=ALIBABARAM_JSON_POLICIES.lower(), target_item=ALIBABARAM_JSON_USER.lower(), error=str(e)))
            return None

        user_policies = self._paginator(ALIBABARAM_JSON_POLICIES, ram_request, None, action_result, False)

        if user_policies is None:
            return None

        # 2. Remove the existing policies of the user
        for policy in user_policies:
            result = self._attach_detach_policy(
                            policy.get(ALIBABARAM_POLICY_NAME),
                            policy.get(ALIBABARAM_POLICY_TYPE), user_name, ALIBABARAM_JSON_USER_NAME, action_result, False)

            if not result:
                return None

        return True

    def _handle_replace_policies(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        user_name = param.get(ALIBABARAM_JSON_USER_NAME)
        group_name = param.get(ALIBABARAM_JSON_GROUP_NAME)

        policies = param.get(ALIBABARAM_JSON_POLICIES.lower())
        policies_list = [x.strip() for x in policies.split(',')]
        policies_list = ' '.join(policies_list).split()

        policy_type = param.get(ALIBABARAM_JSON_POLICY_TYPE)

        if not (user_name or group_name):
            return action_result.set_status(phantom.APP_ERROR,
                'Please provide at least one of the user_name or group_name parameters')

        valid_policy_types = self._validate_policy_types(policies_list, policy_type, action_result)

        if not valid_policy_types:
            return action_result.get_status()

        if user_name:
            # 1. Remove all the existing user policies
            result = self._strip_all_user_policies(user_name, action_result)

            if result is None:
                return action_result.get_status()

            # 2. Add the provided policies to the user
            for policy in policies_list:
                result = self._attach_detach_policy(policy, policy_type, user_name, ALIBABARAM_JSON_USER_NAME, action_result)

                if not result:
                    return action_result.get_status()

        if group_name:
            # 3. List all the current policies of the group
            try:
                ram_request = ListPoliciesForGroupRequest()
                ram_request.set_GroupName(group_name)
                ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
            except Exception as e:
                return action_result.set_status(
                        phantom.APP_ERROR, ALIBABARAM_ERROR_CREATING_REQUEST.format(
                            item_name=ALIBABARAM_JSON_POLICIES.lower(), target_item=ALIBABARAM_JSON_GROUP.lower(), error=str(e)))

            group_policies = self._paginator(ALIBABARAM_JSON_POLICIES, ram_request, None, action_result, False)

            if group_policies is None:
                return action_result.get_status()

            # 4. Remove the existing policies of the group
            for policy in group_policies:
                result = self._attach_detach_policy(
                                policy.get(ALIBABARAM_POLICY_NAME),
                                policy.get(ALIBABARAM_POLICY_TYPE), group_name, ALIBABARAM_JSON_GROUP_NAME, action_result, False)

                if not result:
                    return action_result.get_status()

            # 5. Add the provided policies to the group
            for policy in policies_list:
                result = self._attach_detach_policy(policy, policy_type, group_name, ALIBABARAM_JSON_GROUP_NAME, action_result)

                if not result:
                    return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS, ALIBABARAM_REPLACE_POLICY_MSG.format(user=user_name, grp=group_name))

    def _validate_groups(self, groups_list, action_result):
        all_groups = self._list_all_groups(None, action_result)

        if all_groups is None:
            action_result.set_status(phantom.APP_ERROR,
                "Error occurred while fetching all the groups for validating the provided group names")
            return None

        count = 0

        for group in all_groups:
            if group.get(ALIBABARAM_GROUP_NAME) in groups_list:
                count += 1

        if count != len(groups_list):
            action_result.set_status(phantom.APP_ERROR,
                "Please check the provided groups. One or more groups of the provided group names do not exist on the server.")
            return False

        return True

    def _strip_all_user_groups(self, user_name, action_result):
        # 1. List all the current groups of the user
        try:
            ram_request = ListGroupsForUserRequest()
            ram_request.set_UserName(user_name)
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            action_result.set_status(
                    phantom.APP_ERROR, ALIBABARAM_ERROR_CREATING_REQUEST.format(
                        item_name=ALIBABARAM_JSON_GROUPS.lower(), target_item=ALIBABARAM_JSON_USER.lower(), error=str(e)))
            return None

        user_groups = self._paginator(ALIBABARAM_JSON_GROUPS, ram_request, None, action_result, False)

        if user_groups is None:
            return None

        # 2. Remove the user from the existing groups
        for group in user_groups:
            try:
                ram_request = RemoveUserFromGroupRequest()
                ram_request.set_UserName(user_name)
                ram_request.set_GroupName(group.get(ALIBABARAM_GROUP_NAME))
                ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
            except Exception as e:
                action_result.set_status(
                        phantom.APP_ERROR, ALIBABARAM_ERROR_ADD_REMOVE_GROUP.format(
                            pr=ALIBABARAM_JSON_REMOVING, user='{0} {1}'.format(user_name, ALIBABARAM_JSON_FROM),
                            group=group.get(ALIBABARAM_GROUP_NAME), error=str(e)))
                return None

            try:
                response = self._client.do_action_with_exception(ram_request)
            except Exception as e:
                self.debug_print("Error occurred while removing user: {0} from the group: {1}. Error: {2}".format(
                            user_name, group.get(ALIBABARAM_GROUP_NAME), str(e)))
                action_result.set_status(
                        phantom.APP_ERROR, "Error occurred while removing user: {0} from the group: {1}".format(
                            user_name, group.get(ALIBABARAM_GROUP_NAME)))
                return None

            if not response:
                action_result.set_status(
                        phantom.APP_ERROR,
                        "Unknown error occurred while removing user: {0} from the group: {1}".format(user_name,
                            group.get(ALIBABARAM_GROUP_NAME)))
                return None

        return True

    def _handle_replace_groups(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        user_name = param.get(ALIBABARAM_JSON_USER_NAME)

        groups = param.get(ALIBABARAM_JSON_GROUPS.lower())
        groups_list = [x.strip() for x in groups.split(',')]
        groups_list = ' '.join(groups_list).split()

        valid_groups = self._validate_groups(groups_list, action_result)

        if not valid_groups:
            return action_result.get_status()

        # 1. Remove all the existing user groups
        result = self._strip_all_user_groups(user_name, action_result)

        if result is None:
            return action_result.get_status()

        # 2. Add the user to the provided groups
        for group in groups_list:
            try:
                ram_request = AddUserToGroupRequest()
                ram_request.set_UserName(user_name)
                ram_request.set_GroupName(group)
                ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
            except Exception as e:
                return action_result.set_status(
                        phantom.APP_ERROR, ALIBABARAM_ERROR_ADD_REMOVE_GROUP.format(
                            pr=ALIBABARAM_JSON_ADDING, user='{0} {1}'.format(user_name,
                                ALIBABARAM_JSON_TO), group=group.get(ALIBABARAM_GROUP_NAME), error=str(e)))

            try:
                response = self._client.do_action_with_exception(ram_request)
            except Exception as e:
                self.debug_print("Error occurred while adding user: {0} to the group: {1}. Error: {2}".format(user_name, group, str(e)))
                return action_result.set_status(phantom.APP_ERROR, "Error occurred while adding user: {0} to the group: {1}".format(user_name, group))

            if not response:
                return action_result.set_status(phantom.APP_ERROR,
                    "Unknown error occurred while adding user: {0} to the group: {1}".format(user_name, group))

        return action_result.set_status(phantom.APP_SUCCESS, ALIBABARAM_REPLACE_GROUP_MSG.format(user=user_name))

    def _handle_strip_policies(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        user_name = param.get(ALIBABARAM_JSON_USER_NAME)

        result = self._strip_all_user_policies(user_name, action_result)

        if result is None:
            return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully removed all the policies from the user: {0}".format(user_name))

    def _handle_strip_groups(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        user_name = param.get(ALIBABARAM_JSON_USER_NAME)

        result = self._strip_all_user_groups(user_name, action_result)

        if result is None:
            return action_result.get_status()

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully removed user: {0} from all the groups".format(user_name))

    def _handle_describe_group(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))
        group_name = param[ALIBABARAM_JSON_GROUP_NAME]
        group_details = dict()

        # 1. Fetch the policies details for the given group
        try:
            ram_request = ListPoliciesForGroupRequest()
            ram_request.set_GroupName(group_name)
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            return action_result.set_status(
                    phantom.APP_ERROR, ALIBABARAM_ERROR_CREATING_REQUEST.format(
                        item_name=ALIBABARAM_JSON_POLICIES.lower(), target_item=ALIBABARAM_JSON_GROUP.lower(), error=str(e)))

        policies = self._paginator(ALIBABARAM_JSON_POLICIES, ram_request, None, action_result, False)

        if policies is None:
            return action_result.get_status()

        group_details['policies'] = policies

        # 2. Fetch the users details for the given group
        try:
            ram_request = ListUsersForGroupRequest()
            ram_request.set_GroupName(group_name)
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            return action_result.set_status(
                    phantom.APP_ERROR, ALIBABARAM_ERROR_CREATING_REQUEST.format(
                        item_name=ALIBABARAM_JSON_USERS.lower(), target_item=ALIBABARAM_JSON_GROUP.lower(), error=str(e)))

        users = self._paginator(ALIBABARAM_JSON_USERS, ram_request, None, action_result)

        if users is None:
            return action_result.get_status()

        group_details['users'] = users

        action_result.add_data(group_details)

        summary = action_result.update_summary({})
        summary['total_policies'] = len(group_details['policies'])
        summary['total_users'] = len(group_details['users'])

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_describe_user(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))
        user_name = param[ALIBABARAM_JSON_USER_NAME]
        user_details = dict()

        # 1. Fetch the general details for the given user
        try:
            ram_request = GetUserRequest()
            ram_request.set_UserName(user_name)
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
            response = self._client.do_action_with_exception(ram_request)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR,
                "Error occurred while creating request for fetching details of the user: {0}. Error: {1}".format(user_name, str(e)))

        try:
            resp_json = json.loads(response)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR,'Error occurred while parsing the response JSON. Error: {0}'.format(str(e)))

        if resp_json and resp_json.get(ALIBABARAM_JSON_USER):
            user_details.update(resp_json.get(ALIBABARAM_JSON_USER))
        else:
            return action_result.set_status(phantom.APP_ERROR,
                "Unknown error occurred while fetching the general details of the user: {0}".format(user_name))

        # 2. Fetch the groups details for the given user
        # This API call of the SDK does not support the pagination
        try:
            ram_request = ListGroupsForUserRequest()
            ram_request.set_UserName(user_name)
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            action_result.set_status(
                    phantom.APP_ERROR, ALIBABARAM_ERROR_CREATING_REQUEST.format(
                        item_name=ALIBABARAM_JSON_GROUPS.lower(), target_item=ALIBABARAM_JSON_USER.lower(), error=str(e)))
            return None

        user_groups = self._paginator(ALIBABARAM_JSON_GROUPS, ram_request, None, action_result, False)

        if user_groups is None:
            return None

        user_details.update({ALIBABARAM_JSON_USER_GROUPS: user_groups})

        # 3. Fetch the policies details for the given user
        # This API call of the SDK does not support the pagination
        try:
            ram_request = ListPoliciesForUserRequest()
            ram_request.set_UserName(user_name)
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            action_result.set_status(
                    phantom.APP_ERROR, ALIBABARAM_ERROR_CREATING_REQUEST.format(
                        item_name=ALIBABARAM_JSON_POLICIES.lower(), target_item=ALIBABARAM_JSON_USER.lower(), error=str(e)))
            return None

        user_policies = self._paginator(ALIBABARAM_JSON_POLICIES, ram_request, None, action_result, False)

        if user_policies is None:
            return None

        user_details.update({ALIBABARAM_JSON_USER_POLICIES: user_policies})

        action_result.add_data(user_details)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully fetched the details of the user: {0}".format(user_name))

    def _handle_update_user(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))
        user_name = param.get(ALIBABARAM_JSON_USER_NAME)
        display_name = param.get(ALIBABARAM_JSON_DISPLAY_NAME)
        comment = param.get(ALIBABARAM_JSON_COMMENT)
        email = param.get(ALIBABARAM_JSON_EMAIL)
        mobile_number = param.get(ALIBABARAM_JSON_MOBILE_NUMBER)
        new_username = param.get(ALIBABARAM_JSON_NEW_USER_NAME)

        try:
            ram_request = UpdateUserRequest()
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
            ram_request.set_UserName(user_name)

            if comment:
                ram_request.set_NewComments(comment)

            if email:
                ram_request.set_NewEmail(email)

            if mobile_number:
                ram_request.set_NewMobilePhone(mobile_number)

            if display_name:
                ram_request.set_NewDisplayName(display_name)

            if new_username:
                ram_request.set_NewUserName(new_username)

            response = self._client.do_action_with_exception(ram_request)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR,
                "Error occurred while updating provided details for the user: {0}. Error: {1}".format(user_name, str(e)))

        if not response:
            return action_result.set_status(phantom.APP_ERROR,
                "Unknown error occurred while updating provided details for the user: {0}".format(user_name))

        try:
            resp_json = json.loads(response)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, 'Error occurred while parsing the response JSON. Error: {0}'.format(str(e)))

        if resp_json and resp_json.get(ALIBABARAM_JSON_USER):
            action_result.add_data(resp_json.get(ALIBABARAM_JSON_USER))
        else:
            return action_result.set_status(phantom.APP_ERROR,
                "User: {0} updated successfully, but the API did not return the updated user details".format(user_name))

        return action_result.set_status(phantom.APP_SUCCESS,
            "Successfully updated the details for the User: {0}".format(user_name))

    def handle_action(self, param):

        action_execution_status = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        action_mapping = {
            'test_connectivity': self._handle_test_connectivity,
            'list_users': self._handle_list_users,
            'list_roles': self._handle_list_roles,
            'list_groups': self._handle_list_groups,
            'list_policies': self._handle_list_policies,
            'add_user': self._handle_add_user,
            'remove_user': self._handle_remove_user,
            'describe_user': self._handle_describe_user,
            'describe_group': self._handle_describe_group,
            'attach_policy': self._handle_attach_policy,
            'detach_policy': self._handle_detach_policy,
            'replace_groups': self._handle_replace_groups,
            'strip_policies': self._handle_strip_policies,
            'strip_groups': self._handle_strip_groups,
            'replace_policies': self._handle_replace_policies,
            'update_user': self._handle_update_user
        }

        if action_id in list(action_mapping.keys()):
            action_function = action_mapping[action_id]
            action_execution_status = action_function(param)

        return action_execution_status

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()

        self._access_key = config[ALIBABARAM_JSON_ACCESS_KEY]
        self._secret_key = config[ALIBABARAM_JSON_SECRET_KEY]
        self._region_id = ALIBABARAM_REGIONS_MAPPING.get(config[ALIBABARAM_JSON_REGION_ID], ALIBABARAM_DEFAULT_REGION)

        try:
            self._client = AcsClient(self._access_key, self._secret_key, self._region_id)
        except Exception as e:
            self.save_progress('Error occurred while creating client. Error: {0}'.format(str(e)))
            return phantom.APP_ERROR

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        try:
            login_url = AlibabaRamConnector._get_phantom_base_url() + '/login'

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = AlibabaRamConnector()
        connector.print_progress_message = True

        if (session_id is not None):
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)
