import requests
import json

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class Kuma:

    def __init__(self, address, port, token):
        self.session = requests.Session()
        self.session.verify = False
        self.address = address
        self.port = port
        self.token = token
        self.headers = {'Authorization': 'Bearer ' + token}
        self.session.headers.update(self.headers)

    def _make_request(self, method, route, params=None, data=None, files=None, resp_status_code_expected=200, response_type='json'):
        url = 'https://{}:{}/api/v1/{}'.format(self.address, self.port, route)

        response = self.session.request(
            method, url,
            params=params,
            data=data,
            files=files
        )
        if response.status_code != resp_status_code_expected:
            raise Exception("Wrong result status code " + str(response.status_code) + str(response.text))
        if response_type == 'json':
            return response.json()
        if response_type == 'text':
            return response.text
        if response_type == 'content':
            return response.content

    def make_post_request(self, *args, **kwargs):
        return self._make_request('post', *args, **kwargs)

    def make_get_request(self, *args, **kwargs):
        return self._make_request('get', *args, **kwargs)

    # public API for KUMA 2.0

    def whoami(self):
        return self.make_get_request('users/whoami')

    def get_tenants(self, *args, **kwargs):
        return self.make_get_request('tenants', *args, **kwargs)

    def get_assets(self, page: int = None, id=None, tenantID=None, name=None, fqdn=None, ip=None, mac=None):
        params = {
            "page": page,
            "id": id,
            "tenantID": tenantID,
            "name": name,
            "fqdn": fqdn,
            "ip": ip,
            "mac": mac
        }
        return self.make_get_request('assets', params)

    def import_assets(self, tenantID: str, assets: list):
        data = {
            "tenantID": tenantID,
            "assets": assets}
        return self.make_post_request('assets/import', data=json.dumps(data))

    def delete_assets(self, tenantID: str, ids: list):
        data = {
            "tenantID": tenantID,
            "ids": ids}
        return self.make_post_request('assets/delete', data=json.dumps(data))

    def get_alerts(self, page: int = None, id=None, tenantID=None, name=None, timestampField='lastSeen',
                   _from=None, to=None, status=None, withEvents: bool = False, withAffected: bool = False):
        params = {
            "page": page,
            "id": id,
            "tenantID": tenantID,
            "name": name,
            "timestampField": timestampField,
            "from": _from,
            "to": to,
            "status": status,
        }
        if withEvents:
            params['withEvents'] = ""
        if withAffected:
            params['withAffected'] = ""
        return self.make_get_request('alerts/', params)

    def close_alerts(self, id: str, reason: str = 'responded'):
        if reason not in ['responded', 'incorrect data', 'incorrect correlation rule']:
            raise Exception("Incorrect reason. Available reasons for closing the alert: responded, incorrect data, "
                            "incorrect correlation rule.")
        data = {
            "id": id,
            "reason": reason
        }
        return self.make_post_request('alerts/close', data=json.dumps(data))

    def get_resources(self, page: int = None, id=None, tenantID=None, kind=None, name=None):
        params = {
            "page": page,
            "id": id,
            "tenantID": tenantID,
            "kind": kind,
            "name": name,
        }
        return self.make_get_request('resources', params)

    def get_services(self, page: int = None, id=None, tenantID=None, name=None, kind=None,
                     fqdn=None, paired: bool = False):
        params = {
            "page": page,
            "id": id,
            "tenantID": tenantID,
            "name": name,
            "kind": kind,
            "fqdn": fqdn,
        }
        if paired:
            params['paired'] = ""
        return self.make_get_request('services', params)

    def get_active_lists(self, correlatorID = None):
        if not correlatorID:
            raise Exception("No correlator's id provided. Correlator's id is mandatory parameter.")
        params = {
            "correlatorID": correlatorID
        }
        return self.make_get_request('activeLists/', params)

    def import_active_list_records(self, data, correlatorID=None, activeListID=None, activeListName=None,
                                   format='csv', keyField=None, clear=False):
        if not correlatorID:
            raise Exception("No correlator id provided. Correlator id is mandatory parameter.")
        if not (activeListID or activeListName):
            raise Exception("No active list name or id provided. Active list id or name is mandatory parameter.")
        if format not in ('internal', 'csv', 'tsv'):
            raise Exception("Unsupported format. Format should be 'internal', 'csv' or 'tsv'.")
        if format in ('csv', 'tsv') and not keyField:
            raise Exception("Empty keyField. KeyField is mandatory parameter for csv and tsv formats.")
        params = {
            "correlatorID" : correlatorID,
            "activeListID" : activeListID,
            "activeListName" : activeListName,
            "format" : format,
            "keyField" : keyField
        }
        if clear:
            params.update({"clear" : ""})
        return self.make_post_request('activeLists/import', data=data, params=params,
                                      resp_status_code_expected=204, response_type='text')

    def get_cluster(self, page: int = None, id=None, tenantID=None, name=None):
        params = {
            "page": page,
            "id": id,
            "tenantID": tenantID,
            "name": name
        }
        return self.make_get_request('events/clusters', params)

    def get_dictionary(self, dictionaryID=None):
        if not dictionaryID:
            raise Exception("No dictionary id provided. Dictionary id is mandatory parameter.")
        params = {
            "dictionaryID": dictionaryID
        }
        return self.make_get_request('dictionaries', params, response_type='text')

    # only for KUMA 2.1+
    def update_dictionary(self, dictionaryID=None, files=None):
        if not dictionaryID:
            raise Exception("No dictionary id provided. Dictionary id is mandatory parameter.")
        params = {
            "dictionaryID": dictionaryID
        }
        headers = {'Content-Type': 'multipart/form-data'}
        return self.make_post_request('dictionaries/update', params, files=files)

    def search_events(self, _from, to, sql, clusterID, rawTimestamps=False, emptyFields=False):
        data = {
            "period": {
                "from": _from,
                "to": to
            },
            "sql": sql,
            "clusterID": clusterID,
            "rawTimestamps": rawTimestamps,
            "emptyFields": emptyFields
        }
        return self.make_post_request('events', data=json.dumps(data))

    # export_resources, download_resources, view_resource_file_content, import_resources

    # public API for KUMA 2.1
    def get_asset_custom_fields(self, settings_id: str):
        return self.make_get_request('settings/id/' + settings_id)

    def core_backup(self, path=None):
        if not path:
            raise Exception("No path provided. Path is mandatory parameter for saving backup.")
        backup = self.make_get_request('system/backup', response_type='content')
        with open(path, mode='wb') as file:
            file.write(backup)

    def core_restore(self, path=None):
        if not path:
            raise Exception("No path provided. Path is mandatory parameter for restoring backup.")
        with open(path, mode='rb') as file:
            backup = file.read()
        self.make_post_request('system/restore', data=backup ,response_type='text')

    # custom requests
    def get_tenant_by_name(self, tenant_name='Main'):
        return self.get_tenants(params={"name": tenant_name})