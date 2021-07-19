import time
import yaml
from datetime import datetime
from cloudflare_dns import *

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

    ##################
    #### Examples ####
    ##################

    example_zone = domains[config['dynamic-dns-zone']]

    example_type = 'A'
    example_domain = 'wan.example.com'
    zone_file_example = 'example.com.txt'

    dns_records = list_dns_records(
        # REQUIRED: auth, zone_id
        # OPTIONAL a search term: name, content or type
        header=header,
        zone_id=example_zone,
        set_debug=debug,
        dns_type='txt'
        )

    created_record = create_dns_records(
            # REQUIRED: auth, zone_id, type, name, content, ttl
            header=header,
            zone_id=example_zone,
            set_debug=debug,
            dns_type=example_type,
            name=example_domain,
            content=get_wan_ip(set_debug=debug),
            ttl=1  # ttl of one sets TTL to AUTO
        )

    record_details = dns_records_details(
            # GET zones/:zone_id/dns_records/:identifier
            header=header,
            zone_id=example_zone,
            dns_record_id=list_dns_records(header=header,
                                           zone_id=example_zone,
                                           set_debug=debug,
                                           name=example_domain)['result'][0]['id'],
            set_debug=debug
        )

    updated_dns_records = update_dns_record(
            # PUT zones/:zone_id/dns_records/:identifier
            # REQUIRED: auth, zone_id, dns_record_id, type, name, content, ttl

            header=header,
            zone_id=example_zone,
            dns_record_id=list_dns_records(header=header,
                                           zone_id=example_zone,
                                           set_debug=debug,
                                           name=example_domain)['result'][0]['id'],
            set_debug=debug,
            dns_type='A',
            name='wan.example.com',
            content=get_wan_ip(set_debug=debug),
            ttl=1  # ttl of one sets TTL to AUTO
        )

    patched_dns_records = patch_dns_record(
            # PATCH zones/:zone_id/dns_records/:identifier
            # REQUIRED: N/A
            # OPTIONAL: type, name, content, ttl, proxied
            header=header,
            zone_id=example_zone,
            dns_record_id=list_dns_records(header=header,
                                           zone_id=example_zone,
                                           set_debug=debug,
                                           name=example_domain)['result'][0]['id'],
            set_debug=debug,
            dns_type='A',
            name='wan.example.com',
            content=get_wan_ip(set_debug=debug),
            ttl=1  # ttl of one sets TTL to AUTO
        )

    deleted_record = delete_dns_record(
            # DELETE zones/:zone_id/dns_records/:identifier
            header=header,
            zone_id=example_zone,
            dns_record_id=list_dns_records(header=header,
                                           zone_id=example_zone,
                                           set_debug=debug,
                                           name=example_domain)['result'][0]['id'],
            set_debug=debug
        )

    import_dns_records = import_dns_records(
        # POST zones/:zone_id/dns_records/import
        authentication_header=authentication_header,
        zone_id=example_zone,
        zone_file=zone_file_example,
        set_debug=debug
    )

    export_dns_records = export_dns_records(
        # GET zones/:zone_id/dns_records/export
        header=header,
        zone_id=example_zone,
        zone_file=zone_file_example,
        set_debug=debug
    )
