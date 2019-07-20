# File: alibabaram_connector.py
# Copyright (c) 2019 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

import requests
import json
from bs4 import BeautifulSoup
from alibabaram_consts import *
from aliyunsdkcore.client import AcsClient
from aliyunsdkram.request.v20150501.ListUsersRequest import ListUsersRequest
from aliyunsdkram.request.v20150501.ListRolesRequest import ListRolesRequest
from aliyunsdkram.request.v20150501.ListGroupsRequest import ListGroupsRequest
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

    def _process_empty_response(self, response, action_result):

        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, "Empty response and no information in the header"), None)

    def _process_html_response(self, response, action_result):

        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code,
                error_text)

        message = message.replace(u'{', '{{').replace(u'}', '}}')

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):

        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(str(e))), None)

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace(u'{', '{{').replace(u'}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):

        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if 'json' in r.headers.get('Content-Type', ''):
            return self._process_json_response(r, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace('{', '{{').replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), resp_json)

        # Create a URL to connect to
        url = self._base_url + endpoint

        try:
            r = request_func(
                            url,
                            # auth=(username, password),  # basic authentication
                            verify=config.get('verify_server_cert', False),
                            **kwargs)
        except Exception as e:
            return RetVal(action_result.set_status( phantom.APP_ERROR, "Error Connecting to server. Details: {0}".format(str(e))), resp_json)

        return self._process_response(r, action_result)

    def _paginator(self, item_name, ram_request, limit, action_result, set_max_items=True):

        list_items = list()
        next_token = None

        if set_max_items:
            ram_request.set_MaxItems("100")

        while True:
            try:
                if next_token:
                    ram_request.set_Marker(next_token)
                    next_token = None

                response = self._client.do_action_with_exception(ram_request)
            except Exception as e:
                action_result.set_status(phantom.APP_ERROR, 'Error occurred while fetching the list of all the RAM {0}. Error: {1}'.format(item_name, str(e)))
                return None

            try:
                resp_json = json.loads(response)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, 'Error occurred while parsing the response JSON. Error: {0}'.format(str(e)))

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
            return action_result.set_status(phantom.APP_ERROR, 'Client could not be initialized. Please check credentials and region in the asset configuration parameters.')

        self.save_progress("Connecting the endpoint for fetching all the users")
        try:
            ram_request = ListUsersRequest()
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)

            self._client.do_action_with_exception(ram_request)
        except Exception as e:
            self.save_progress("Test Connectivity Failed")
            return action_result.set_status(phantom.APP_ERROR, 'Error occurred while fetching the list of all the users. Error: {0}'.format(str(e)))

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
            return action_result.set_status(phantom.APP_ERROR, 'Error occurred while creating request for fetching list of all the RAM users. Error: {0}'.format(str(e)))

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
            return action_result.set_status(phantom.APP_ERROR, 'Error occurred while creating request for fetching list of all the RAM roles. Error: {0}'.format(str(e)))

        roles = self._paginator(ALIBABARAM_JSON_ROLES, ram_request, limit, action_result)

        if roles is None:
            return action_result.get_status()

        for role in roles:
            action_result.add_data(role)

        summary = action_result.update_summary({})
        summary['total_roles'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_groups(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))
        limit = param.get(ALIBABARAM_JSON_LIMIT)

        if (limit and not str(limit).isdigit()) or limit == 0:
            return action_result.set_status(phantom.APP_ERROR, ALIBABARAM_INVALID_INTEGER.format(parameter=ALIBABARAM_JSON_LIMIT))

        try:
            ram_request = ListGroupsRequest()
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, 'Error occurred while creating request for fetching list of all the RAM groups. Error: {0}'.format(str(e)))

        groups = self._paginator(ALIBABARAM_JSON_GROUPS, ram_request, limit, action_result)

        if groups is None:
            return action_result.get_status()

        for group in groups:
            action_result.add_data(group)

        summary = action_result.update_summary({})
        summary['total_groups'] = action_result.get_data_size()

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
            return action_result.set_status(phantom.APP_ERROR, "Error occurred while adding user: {0} to the group: {1}. Error: {2}".format(user_name, group_name, str(e)))

        if not response:
            return action_result.set_status(phantom.APP_ERROR, "Unknown error occurred while adding user: {0} to the group: {1}".format(user_name, group_name))

        return action_result.set_status(phantom.APP_SUCCESS, "User: {0} is successfully added to the group: {1}".format(user_name, group_name))

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
            return action_result.set_status(phantom.APP_ERROR, "Error occurred while removing user: {0} from the group: {1}. Error: {2}".format(user_name, group_name, str(e)))

        if not response:
            return action_result.set_status(phantom.APP_ERROR, "Unknown error occurred while removing user: {0} from the group: {1}".format(user_name, group_name))

        return action_result.set_status(phantom.APP_SUCCESS, "User: {0} is successfully removed from the group: {1}".format(user_name, group_name))

    def _attach_detach_policy(self, policy_name, policy_type, item, item_name, action_result, is_attach=True):
        try:
            ram_request = None
            if not is_attach:
                process_name = ALIBABARAM_PROCESS_DETACHING
            else:
                process_name = ALIBABARAM_PROCESS_ATTACHING

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
            action_result.set_status(phantom.APP_ERROR, ALIBABARAM_ERROR_ATTACH_DETACH_POLICY.format(pr=process_name, pol=policy_name, itn=item_name, it=item, err=str(e)))
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

        if not (user_name and group_name and role_name):
            return action_result.set_status(phantom.APP_ERROR, 'Please provide at least one of the user_name, group_name, or role_name parameters')

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

        return action_result.set_status(phantom.APP_SUCCESS, ALIBABARAM_ATTACH_POLICY_MSG.format(pol=policy_name, user=user_name, grp=group_name, role=role_name))

    def _handle_detach_policy(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        user_name = param.get(ALIBABARAM_JSON_USER_NAME)
        group_name = param.get(ALIBABARAM_JSON_GROUP_NAME)
        role_name = param.get(ALIBABARAM_JSON_ROLE_NAME)
        policy_name = param.get(ALIBABARAM_JSON_POLICY_NAME)
        policy_type = param.get(ALIBABARAM_JSON_POLICY_TYPE)

        if not (user_name and group_name and role_name):
            return action_result.set_status(phantom.APP_ERROR, 'Please provide at least one of the user_name, group_name, or role_name parameters')

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

        return action_result.set_status(phantom.APP_SUCCESS, ALIBABARAM_DETACH_POLICY_MSG.format(pol=policy_name, user=user_name, grp=group_name, role=role_name))

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
            return action_result.set_status(phantom.APP_ERROR, ALIBABARAM_ERROR_CREATING_REQUEST.format(item_name=ALIBABARAM_JSON_POLICIES.lower(), error=str(e)))

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
            return action_result.set_status(phantom.APP_ERROR, ALIBABARAM_ERROR_CREATING_REQUEST.format(item_name=ALIBABARAM_JSON_USERS.lower(), error=str(e)))

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
            return action_result.set_status(phantom.APP_ERROR, "Error occurred while creating request for fetching details of the user: {0}. Error: {1}".format(user_name, str(e)))

        try:
            resp_json = json.loads(response)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, 'Error occurred while parsing the response JSON. Error: {0}'.format(str(e)))

        if resp_json and resp_json.get(ALIBABARAM_JSON_USER):
            user_details.update(resp_json.get(ALIBABARAM_JSON_USER))
        else:
            return action_result.set_status(phantom.APP_ERROR, "Unknown error occurred while fetching the general details of the user: {0}".format(user_name))

        # 2. Fetch the groups details for the given user
        # This API call of the SDM does not support the pagination
        try:
            ram_request = ListGroupsForUserRequest()
            ram_request.set_UserName(user_name)
            ram_request.set_accept_format(ALIBABARAM_JSON_KEY)
            response = self._client.do_action_with_exception(ram_request)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error occurred while creating request for fetching groups of the user: {0}. Error: {1}".format(user_name, str(e)))

        try:
            resp_json = json.loads(response)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, 'Error occurred while parsing the response JSON. Error: {0}'.format(str(e)))

        if resp_json and resp_json.get(ALIBABARAM_JSON_GROUPS) and resp_json.get(ALIBABARAM_JSON_GROUPS).get(ALIBABARAM_JSON_ACTIONS_RESPONSE_MAPPING.get(ALIBABARAM_JSON_GROUPS)):
            user_details.update({ALIBABARAM_JSON_USER_GROUPS: resp_json.get(ALIBABARAM_JSON_GROUPS).get(ALIBABARAM_JSON_ACTIONS_RESPONSE_MAPPING.get(ALIBABARAM_JSON_GROUPS))})
        else:
            user_details.update({ALIBABARAM_JSON_USER_GROUPS: []})

        action_result.add_data(user_details)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully fetched the details of the user: {0}".format(user_name))

    def _handle_list_user_groups(self, param):

        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # For now return Error with a message, in case of success we don't set the message, but use the summary
        return action_result.set_status(phantom.APP_ERROR, "Action not yet implemented")

    def _handle_update_user(self, param):

        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # For now return Error with a message, in case of success we don't set the message, but use the summary
        return action_result.set_status(phantom.APP_ERROR, "Action not yet implemented")

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
            'add_user': self._handle_add_user,
            'remove_user': self._handle_remove_user,
            'describe_user': self._handle_describe_user,
            'describe_group': self._handle_describe_group,
            'list_user_groups': self._handle_list_user_groups,
            'attach_policy': self._handle_attach_policy,
            'detach_policy': self._handle_detach_policy,
            'update_user': self._handle_update_user
        }

        if action_id in action_mapping.keys():
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

            print ("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print ("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print ("Unable to get session id from the platform. Error: " + str(e))
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
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
