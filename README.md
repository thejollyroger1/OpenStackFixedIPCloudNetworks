# OpenStackFixedIPCloudNetworks

Usage:

python ipadd.py --instance \<instance_uuid\> --network \<network_uuid\> --ipaddr \<desired ip\> --ddi \<account number\> --region \<region\> --user \<api user\> --apikey \<api-key\>

Successful return example

{"port": {"status": "ACTIVE", "name": "", "admin_state_up": true, "network_id": \<network_uuid\>, "tenant_id": \<ddi\>, "device_owner": null, "mac_address": \<mac-address\>, "fixed_ips": [{"subnet_id": \<subnet_id\>, "ip_address": \<chosen_ip\>}], "id": \<port_id\>, "security_groups": [], "device_id": \<device_id\>}}


{"virtual_interfaces": [{"ip_addresses": [{"network_id": \<network_uuid\>, "network_label": \<network_label\>, "address": \<chosen_ip\>}], "id": \<virtual_interface_uuid\>, "mac_address": \<mac_address\>}]}
