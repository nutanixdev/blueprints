# region headers
# * author:     igor.zecevic@nutanix.com
# * version:    v1.0 - initial version
# * date:       11/03/2020
# task_name:    VeeamGetHierarchyRoots
# description:  Get the hierarchyRoot UID
#               The script retreives the hierarchyRoots UID
# input vars:   veeam_session_cookie, vc_server, api_server
# output vars:  veeam_hierarchyRoot_uid
# endregion

# region capture Calm variables
veeam_session_cookie = "@@{veeam_session_cookie}@@"
api_server = "@@{veeam_endpoint}@@"
vc_server = "@@{vc_endpoint}@@"
# endregion

# region prepare api call
api_server_port = "9398"
api_server_endpoint = "/api/hierarchyRoots"
method = "GET"
url = "https://{}:{}{}".format(api_server, api_server_port, api_server_endpoint)
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-RestSvcSessionId': veeam_session_cookie}
# endregion

# region API call function
def process_request(url, method, headers, payload=None):
    if (payload is not None):
        payload = json.dumps(payload)
    r = urlreq(url, verb=method, params=payload, verify=False, headers=headers)
    if r.ok:
        print("Request was successful")
        print("Status code: {}".format(r.status_code))
    else:
        print("Request failed")
        print('Status code: {}'.format(r.status_code))
        print("Headers: {}".format(headers))
        print("Payload: {}".format(json.dumps(payload)))
        print('Response: {}'.format(json.dumps(json.loads(r.content), indent=4)))
        exit(1)
    return r
# endregion

# region login
print("Making a {} API call to {}".format(method, url))
resp = process_request(url, method, headers)
# endregion

# pass the repo_uid so that it may be captured by Calm.
obj_uid = ""
resp_parse = json.loads(resp.content)
for obj in resp_parse['Refs']:
    if obj['Name'] == vc_server:
                obj_uid = obj['UID']               
if obj_uid:
    print ("veeam_hierarchyroot_uid={}".format(obj_uid.rsplit(':', 1)[1]))
    exit(0)
else:
    print("Error: Managed Server "+vc_server+" doesn't is not present ..")
    exit(1)