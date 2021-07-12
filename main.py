import time
from datetime import datetime

from cloudflare_dns import *
import yaml


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
        print('Error: Ensure config.yml is located in the current path.')
        exit()

    debug = config['debug']

    # Header details
    api_token = config['api-token']
    header = dict([('Authorization', 'Bearer {0}'.format(api_token)), ('Content-Type', 'application/json')])
    authenication_header = dict([('Authorization', 'Bearer {0}'.format(api_token))])

    # Cloudflare accounts details
    account_id = config['account-id']

    # Fetch zone_id's
    domains = get_zone_ids(header=header, account_id=account_id)

    # Update IP for dynamic IP
    dynamic_ip_update()

    # ##################
    # #### Examples ####
    # ##################
    #
    # example_type = 'A'
    # example_domain = 'wan.tinycellar.com'
    # zone_file_example = 'tinycellar.com.txt'
    #
    # list_dns_records(
    #     # REQUIRED: auth, zone_id
    #     # OPTIONAL a search term: name, content or type
    #     header=header,
    #     zone_id=tiny_cellar_zone,
    #     set_debug=debug,
    #     dns_type='txt'
    #     )
    #
    # create_dns_records(
    #         # REQUIRED: auth, zone_id, type, name, content, ttl
    #         header=header,
    #         zone_id=tiny_cellar_zone,
    #         set_debug=debug,
    #         dns_type=example_type,
    #         name=example_domain,
    #         content=get_wan_ip(set_debug=debug),
    #         ttl=1  # ttl of one sets TTL to AUTO
    #     )
    #
    # dns_records_details(
    #         # GET zones/:zone_id/dns_records/:identifier
    #         header=header,
    #         zone_id=tiny_cellar_zone,
    #         dns_record_id=list_dns_records(header=header,
    #                                        zone_id=tiny_cellar_zone,
    #                                        set_debug=debug,
    #                                        name=example_domain)['result'][0]['id'],
    #         set_debug=debug
    #     )
    #
    # update_dns_record(
    #         # PUT zones/:zone_id/dns_records/:identifier
    #         # REQUIRED: auth, zone_id, dns_record_id, type, name, content, ttl
    #
    #         header=header,
    #         zone_id=tiny_cellar_zone,
    #         dns_record_id=list_dns_records(header=header,
    #                                        zone_id=tiny_cellar_zone,
    #                                        set_debug=debug,
    #                                        name=example_domain)['result'][0]['id'],
    #         set_debug=debug,
    #         dns_type='A',
    #         name='wan.tinycellar.com',
    #         content=get_wan_ip(set_debug=debug),
    #         ttl=1  # ttl of one sets TTL to AUTO
    #     )
    #
    # patch_dns_record(
    #         # PATCH zones/:zone_id/dns_records/:identifier
    #         # REQUIRED: N/A
    #         # OPTIONAL: type, name, content, ttl, proxied
    #         header=header,
    #         zone_id=tiny_cellar_zone,
    #         dns_record_id=list_dns_records(header=header,
    #                                        zone_id=tiny_cellar_zone,
    #                                        set_debug=debug,
    #                                        name=example_domain)['result'][0]['id'],
    #         set_debug=debug,
    #         dns_type='A',
    #         name='wan.tinycellar.com',
    #         content=get_wan_ip(set_debug=debug),
    #         ttl=1  # ttl of one sets TTL to AUTO
    #     )
    #
    # delete_dns_record(
    #         # DELETE zones/:zone_id/dns_records/:identifier
    #         header=header,
    #         zone_id=tiny_cellar_zone,
    #         dns_record_id=list_dns_records(header=header,
    #                                        zone_id=tiny_cellar_zone,
    #                                        set_debug=debug,
    #                                        name=example_domain)['result'][0]['id'],
    #         set_debug=debug
    #     )
    #
    # import_dns_records(
    #     # POST zones/:zone_id/dns_records/import
    #     authenication_header=authenication_header,
    #     zone_id=tiny_cellar_zone,
    #     zone_file=zone_file_example,
    #     set_debug=debug
    # )
    #
    # export_dns_records(
    #     # GET zones/:zone_id/dns_records/export
    #     header=header,
    #     zone_id=tiny_cellar_zone,
    #     zone_file=zone_file_example,
    #     set_debug=debug
    # )
