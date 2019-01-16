# --
# File: malshare_connector.py
#
# Copyright (c) 2017-2019 Splunk Inc.

# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
#
# --


# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
from phantom.vault import Vault

import requests
import json
import uuid
import os
import shutil
from bs4 import BeautifulSoup


class RetVal(tuple):
    def __new__(cls, val1, val2):
        return tuple.__new__(RetVal, (val1, val2))


class MalshareConnector(BaseConnector):

    def __init__(self):

        super(MalshareConnector, self).__init__()

        self._state = None
        self._api_key = None

        self._base_url = "https://malshare.com/api.php?"

    def _process_empty_reponse(self, response, action_result):

        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, "Empty response and no information in the header"), None)

    def _process_test_hash_list(self, r, action_result):

        split_response = r.text.split()

        # If the first item in the split is 32 characters and we're expecting a hash, proceed
        if len(split_response[0]) == 32:
            return RetVal(phantom.APP_SUCCESS, split_response)

        else:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Did not receive expected hash list: " + r.text), None)

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

        message = message.replace('{', '{{').replace('}', '}}')

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):

        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        if r.status_code == 200:

            # get_file_info and get_file can return this message in a 200 if a hash isn't found
            if self.get_action_identifier() == "get_file_info" or self.get_action_identifier() == "get_file":
                if 'sample not found by hash' in r.text.lower():
                    return RetVal(phantom.APP_SUCCESS, None)

            # When downloading samples we need to accept basically anything
            if self.get_action_identifier() == "get_file":
                return RetVal(phantom.APP_SUCCESS, r.content)

            # Responses for list_hashes (when a file type is supplied) and get_file_info will come back as JSON
            elif self.get_action_identifier() == "list_hashes" or self.get_action_identifier() == "get_file_info":
                if r.text[:1] == "{" or r.text[:1] == "[":
                    return RetVal(phantom.APP_SUCCESS, json.loads(r.text))

            # Responses for list_urls will just be an ascii list of URLs separated by spaces
            elif self.get_action_identifier() == "list_urls":
                if r.text[:4] == "http":
                    return RetVal(phantom.APP_SUCCESS, r.text.split())

            # Responses for list_hashes will just be an ascii list of MD5 separated by spaces
            if self.get_action_identifier() == "list_hashes" or self.get_action_identifier() == "test_connectivity":
                hashlist_test = self._process_test_hash_list(r, action_result)
                if hashlist_test[0] == phantom.APP_SUCCESS:
                    return hashlist_test

        # Process an HTML resonse, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_reponse(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace('{', '{{').replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, get_string, action_result):

        resp_json = None

        request_func = getattr(requests, "get")

        # Malshare does not have a valid SSL certificate but still better than nothing
        try:
            r = request_func(self._api_url + get_string)

        except Exception as e:
            return RetVal(action_result.set_status( phantom.APP_ERROR, "Error Connecting to server. Details: {0}".format(str(e))), resp_json)

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress("Connecting to endpoint")

        # Test connectivity by retrieving and validating a list of hashes
        ret_val, response = self._make_rest_call('getlistraw', action_result)

        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed")
            return action_result.get_status()

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_hashes(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Connecting to endpoint")

        if "file_type" in param and param["file_type"]:
            ret_val, response = self._make_rest_call('type&type=' + param["file_type"], action_result)

        else:
            ret_val, response = self._make_rest_call('getlistraw', action_result)

        if phantom.is_fail(ret_val):
            self.save_progress("Hash List request failed. Error: {0}".format(action_result.get_message()))
            return action_result.get_status()

        hash_count = 0

        for hash_entry in response:
            action_result.add_data({"md5": hash_entry})
            hash_count += 1

        action_result.update_summary({'hash_count': hash_count})

        if hash_count <= 0:
            self.save_progress("Unable to extract any hashes from the hash list response")
            return action_result.set_status(phantom.APP_SUCCESS, "No hashes processed from hash list.")
        else:
            self.save_progress(str(hash_count) + " hashes found in hash list")
            return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_urls(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Connecting to endpoint")
        ret_val, response = self._make_rest_call('getsourcesraw', action_result)

        if phantom.is_fail(ret_val):
            self.save_progress("Sources List request failed. Error: {0}".format(action_result.get_message()))
            return action_result.get_status()

        source_count = 0

        for url in response:
            if url[:4] == "http":
                action_result.add_data({"source": url})
                source_count += 1

        action_result.update_summary({'source_count': source_count})

        if source_count <= 0:
            self.save_progress("Unable to extract any sources from the source list")
            return action_result.set_status(phantom.APP_ERROR, "No sources processed from the source list.")
        else:
            self.save_progress(str(source_count) + " sources found in the source list")
            return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_file_info(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Connecting to endpoint")
        ret_val, response = self._make_rest_call('details&hash=' + str(param["hash"]), action_result)

        if phantom.is_fail(ret_val):
            self.save_progress("File Info request failed. Error: {0}".format(action_result.get_message()))
            return action_result.get_status()

        if response is None:
            action_result.update_summary({'file_info_found': False})
            self.save_progress("Unable to find info for hash: " + str(param["hash"]))
            return action_result.set_status(phantom.APP_SUCCESS, "Sample not found by hash " + str(param["hash"]))

        action_result.update_summary({'file_info_found': True})

        action_result.add_data(response)

        self.save_progress("Info found for hash: " + str(param["hash"]))
        return action_result.set_status(phantom.APP_SUCCESS)

    def _save_file_to_vault(self, action_result, response_attachment, sample_hash):

        # Create a tmp directory on the vault partition
        guid = uuid.uuid4()

        if hasattr(Vault, 'get_vault_tmp_dir'):
            temp_dir = Vault.get_vault_tmp_dir()
        else:
            temp_dir = '/vault/tmp'

        local_dir = temp_dir + '/{}'.format(guid)
        self.save_progress("Using temp directory: {0}".format(guid))

        try:
            os.makedirs(local_dir)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Unable to create temporary folder {0}.".format(temp_dir), e)

        file_path = "{0}/{1}".format(local_dir, sample_hash)

        # open and download the file
        with open(file_path, 'wb') as f:
            f.write(response_attachment)

        file_name = '{}'.format(sample_hash)

        # move the file to the vault
        vault_ret_dict = Vault.add_attachment(file_path, self.get_container_id(), file_name=file_name)
        curr_data = {}

        if (vault_ret_dict['succeeded']):
            curr_data[phantom.APP_JSON_VAULT_ID] = vault_ret_dict[phantom.APP_JSON_HASH]
            curr_data[phantom.APP_JSON_NAME] = file_name
            action_result.add_data(curr_data)
            wanted_keys = [phantom.APP_JSON_VAULT_ID, phantom.APP_JSON_NAME]
            summary = {x: curr_data[x] for x in wanted_keys}
            action_result.update_summary(summary)
            action_result.set_status(phantom.APP_SUCCESS)
        else:
            action_result.set_status(phantom.APP_ERROR, phantom.APP_ERR_FILE_ADD_TO_VAULT)
            action_result.append_to_message(vault_ret_dict['message'])

        # remove the /tmp/<> temporary directory
        shutil.rmtree(local_dir)

        return action_result.get_status()

    def _handle_get_file(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Connecting to endpoint")
        ret_val, response = self._make_rest_call('getfile&hash=' + str(param["hash"]), action_result)

        if phantom.is_fail(ret_val):
            self.save_progress("File Info request failed. Error: {0}".format(action_result.get_message()))
            return action_result.get_status()

        if response is None:
            action_result.update_summary({'file_found': False})
            self.save_progress("Unable to find sample for hash: " + str(param["hash"]))
            action_result.add_data({param["hash"]: False})
            return action_result.set_status(phantom.APP_SUCCESS, "Sample not found by hash")

        self._save_file_to_vault(action_result, response, param["hash"])

        action_result.update_summary({'file_found': True})
        self.save_progress("Sample retrieved for hash: " + str(param["hash"]))
        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'list_hashes':
            ret_val = self._handle_list_hashes(param)

        elif action_id == 'list_urls':
            ret_val = self._handle_list_urls(param)

        elif action_id == 'get_file_info':
            ret_val = self._handle_get_file_info(param)

        elif action_id == 'get_file':
            ret_val = self._handle_get_file(param)

        return ret_val

    def initialize(self):
        self._state = self.load_state()

        config = self.get_config()

        self._api_key = config["api_key"]
        self._api_url = self._base_url + "api_key=" + str(self._api_key) + "&action="

        return phantom.APP_SUCCESS

    def finalize(self):
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':
    import sys
    import pudb
    pudb.set_trace()

    if len(sys.argv) < 2:
        print "No test json specified as input"
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = MalshareConnector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
