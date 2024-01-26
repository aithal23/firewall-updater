import os
import requests
from google.oauth2 import service_account
from googleapiclient import discovery

def get_public_ip():
    return requests.get('https://ifconfig.me/ip').text

def load_env_variables(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                name, value = line.strip().split('=', 1)
                os.environ[name] = value

def replace_last_byte_with_zero(ip_address):
    # Split the IP address into its octets
    octets = ip_address.split('.')

    # Replace the last octet with '0'
    octets[-1] = '0'

    # Join the octets back into a string
    new_ip = '.'.join(octets)

    return new_ip


def update_firewall_rule(project_id, firewall_rule_name, network_name, source_ranges, compute):
    
    try:
        compute.firewalls().get(project=project_id, firewall=firewall_rule_name).execute()
        print(f"Firewall rule '{firewall_rule_name}' already exists. Updating...")
    except Exception as e:
        # Create the firewall rule if it doesn't exist
        print(f"Firewall rule '{firewall_rule_name}' doesn't exist. Creating...")
        firewall_body = {
            "name": firewall_rule_name,
            "allowed": [{"IPProtocol": "all"}],  # Customize allowed protocols and ports
            "sourceRanges": [f"{source_ranges}/24"],
            "direction": "INGRESS",
            "priority": 1000,  # Customize priority
            "network": f"projects/{project_id}/global/networks/{network_name}",  # Customize network
            "description": "Allow traffic from the host's public IP",
        }
        compute.firewalls().insert(project=project_id, body=firewall_body).execute()
        print(f"Firewall rule '{firewall_rule_name}' created.")
    # Update the source IP range of the firewall rule
    update_body = {"sourceRanges": [f"{source_ranges}/24"]}
    compute.firewalls().patch(project=project_id, firewall=firewall_rule_name, body=update_body).execute()
    print(f"Firewall rule '{firewall_rule_name}' updated with the new public IP address: {source_ranges}")

def main():
    project_id = os.environ.get("PROJECT_ID")
    firewall_rule_name = os.environ.get('FIREWALL_RULE_NAME')
    network_name = os.environ.get('NETWORK_NAME')
    public_ip = get_public_ip()
    # Authenticate using a service account key file
    credentials = service_account.Credentials.from_service_account_file(
        os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    # Create a Google Cloud Compute Engine service client
    compute = discovery.build('compute', 'v1', credentials=credentials)
    public_ip = replace_last_byte_with_zero(public_ip)
    update_firewall_rule(project_id, firewall_rule_name, network_name, public_ip, compute)

if __name__ == '__main__':
    load_env_variables(".env")
    main()
