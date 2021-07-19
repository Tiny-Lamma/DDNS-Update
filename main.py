import time
import yaml
from datetime import datetime
from cloudflare_dns import *


def dynamic_ip_update():
    tiny_cellar_zone = domains[config['dynamic-dns-zone']]
    dynamic_ip_domain = config['dynamic-domain']
    dns_record = list_dns_records(header=header, zone_id=tiny_cellar_zone, set_debug=debug, name=dynamic_ip_domain)
    dns_record_id = dns_record['result'][0]['id']

    while True:
        ip_address = get_wan_ip(set_debug=debug)

        result = patch_dns_record(
            header=header,
            zone_id=tiny_cellar_zone,
            dns_record_id=dns_record_id,
            set_debug=debug,
            dns_type='A',
            name=dynamic_ip_domain,
            content=ip_address,
            ttl=120
        )
        time_stamp = datetime.now()
        if result['success']:
            if not config['quiet']:
                print('[{0}] Successfully updated {1} with ip address {2}.'.format(
                    time_stamp,
                    dynamic_ip_domain,
                    ip_address)
                )
        else:
            print('[{0}] Failed to update. \n{1}'.format(time_stamp, result))
        time.sleep(config['update-time'])


if __name__ == '__main__':
    # Load config

    try:
        config = yaml.safe_load(open(file='config.yml', mode='r'))
    except FileNotFoundError:
        config = None
        print('Error: Ensure config.yml is located in the current path.')
        exit()

    debug = config['debug']

    # Header details
    api_token = config['api-token']
    header = dict([('Authorization', 'Bearer {0}'.format(api_token)), ('Content-Type', 'application/json')])
    authentication_header = dict([('Authorization', 'Bearer {0}'.format(api_token))])

    # Cloudflare accounts details
    account_id = config['account-id']

    # Fetch zone_id's
    domains = get_zone_ids(header=header, account_id=account_id)

    # Update IP for dynamic IP
    dynamic_ip_update()