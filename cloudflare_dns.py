import requests
import json


def get_wan_ip(set_debug: bool = False) -> str:
    ip_address = requests.get('https://api.ipify.org').text
    if set_debug:
        print('WAN IP ADDRESS: {0}'.format(ip_address))
    return ip_address


def get_zone_ids(header: dict, account_id: str) -> dict:  #
    url = 'https://api.cloudflare.com/client/v4/zones?status=active&account.id={0}'.format(account_id)
    json_response = json.loads(requests.get(url=url, headers=header).text)
    dns_records = json_response['result']
    domains = {}
    for dns_record in dns_records:
        domains[dns_record['name']] = dns_record['id']
    return domains


def list_dns_records(
        header: dict,
        zone_id: str,
        set_debug: bool = False,
        match: str = 'all',
        name: str = '',
        order: str = 'type',
        page: int = 1,
        per_page: int = 100,
        content: str = '',
        dns_type: str = '',
        proxied: bool = '',
        direction: str = 'desc'
) -> json:
    # GET zones/:zone_identifier/dns_records
    # REQUIRED: N/A
    # OPTIONAL: match, name, order, page, per_page, content, type, proxied, direction

    custom_values = ''

    if dns_type:
        custom_values += 'type={0}&'.format(dns_type)
    if name:
        custom_values += 'name={0}&'.format(name)
    if proxied:
        custom_values += 'proxied={0}&'.format(proxied)

    dns_query: str = '{7}match={0}&order={1}&page={2}&per_page={3}&content={4}&proxied={5}&direction={6}'.format(
        match, order, page, per_page, content, proxied, direction, custom_values
    )

    url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records?{1}'.format(zone_id, dns_query)
    json_response = json.loads(requests.get(url=url, headers=header).text)

    if set_debug:
        print('URL:\n{0}\nRESPONSE:\n{1}'.format(url, json_response))

    return json_response


def create_dns_records(
        header: dict,
        zone_id: str,
        dns_type: str,
        name: str,
        content: str,
        set_debug: bool = False,
        ttl: int = 1,
        priority: int = 1,
        proxied: bool = False
) -> json:
    # POST zones/:zone_identifier/dns_records
    # REQUIRED: type, name, content, ttl
    # OPTIONAL: priority, proxied
    data = json.dumps(  # convert from dictionary to json.
        {
            'type': dns_type,
            'name': name,
            'content': content,
            'ttl': ttl,
            'priority': priority,
            'proxied': proxied
        }
    )
    url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records'.format(zone_id)
    json_response = json.loads(requests.post(url=url, headers=header, data=data).text)
    if set_debug:
        print('URL:\n{0}\nRESPONSE:\n{1}'.format(url, json_response))
    return json_response


def dns_records_details(
        header: dict,
        zone_id: str,
        dns_record_id: str,
        set_debug: bool = False
) -> json:
    # GET zones/:zone_identifier/dns_records/:identifier
    url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records/{1}'.format(zone_id, dns_record_id)
    json_response = json.loads(requests.get(url=url, headers=header).text)
    if set_debug:
        print('URL:\n{0}\nRESPONSE:\n{1}'.format(url, json_response))
    return json_response


def update_dns_record(
        header: dict,
        zone_id: str,
        dns_record_id: str,
        dns_type: str,
        name: str,
        content: str,
        set_debug: bool = False,
        ttl: int = 1,
        proxied: bool = False
) -> json:
    # PUT zones/:zone_identifier/dns_records/:identifier
    # REQUIRED: type, name, content, ttl
    # OPTIONAL: proxied
    data = json.dumps(  # convert from dictionary to json.
        {
            'type': dns_type,
            'name': name,
            'content': content,
            'ttl': ttl,
            'proxied': proxied
        }
    )
    url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records/{1}'.format(zone_id, dns_record_id)
    json_response = json.loads(requests.put(url=url, headers=header, data=data).text)
    if set_debug:
        print('URL:\n{0}\nRESPONSE:\n{1}'.format(url, json_response))
    return json_response


def patch_dns_record(
        header: dict,
        zone_id: str,
        dns_record_id: str,
        dns_type: str,
        name: str,
        content: str,
        set_debug: bool = False,
        ttl: int = 1,
        proxied: bool = False
) -> json:
    # PATCH zones/:zone_identifier/dns_records/:identifier
    # REQUIRED: N/A
    # OPTIONAL: type, name, content, ttl, proxied
    # PUT zones/:zone_identifier/dns_records/:identifier
    # REQUIRED: type, name, content, ttl
    # OPTIONAL: proxied
    data = json.dumps(  # convert from dictionary to json.
        {
            'type': dns_type,
            'name': name,
            'content': content,
            'ttl': ttl,
            'proxied': proxied
        }
    )
    url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records/{1}'.format(zone_id, dns_record_id)
    json_response = json.loads(requests.patch(url=url, headers=header, data=data).text)
    if set_debug:
        print('URL:\n{0}\nRESPONSE:\n{1}'.format(url, json_response))
    return json_response


def delete_dns_record(
        header: dict,
        zone_id: str,
        dns_record_id: str,
        set_debug: bool = False
) -> json:
    # DELETE zones/:zone_identifier/dns_records/:identifier
    # REQUIRED: N/A

    url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records/{1}'.format(zone_id, dns_record_id)
    json_response = json.loads(requests.delete(url=url, headers=header).text)
    if set_debug:
        print('URL:\n{0}\nRESPONSE:\n{1}'.format(url, json_response))
    return json_response


def import_dns_records(
        authenication_header: dict,
        zone_id: str,
        zone_file: str,
        proxied: bool = False,
        set_debug: bool = False
) -> json:
    # POST zones/:zone_identifier/dns_records/import
    # REQUIRED: file
    # OPTIONAL: proxied
    url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records/import'.format(zone_id)
    json_response = json.loads(requests.post(
        url=url,
        headers=authenication_header,  # first item only, removed content-type
        files={'file': open(file=zone_file, mode='rb').read(), 'proxied':  proxied}
    ).text)

    if set_debug:
        print('URL:\n{0}\nRESPONSE:\n{1}'.format(url, json_response))
    return json_response


def export_dns_records(
        header: dict,
        zone_id: str,
        zone_file: str,
        set_debug: bool = False
) -> bool:
    # GET zones/:zone_identifier/dns_records/export
    url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records/export'.format(zone_id)
    response = requests.get(url=url, headers=header)
    zone_export_file = open(file=zone_file, mode='w+')
    print(zone_export_file.write(response.text))
    zone_export_file.close()
    if set_debug:
        print('URL:\n{0}\nRESPONSE:\n{1}'.format(url, response))
    return True
