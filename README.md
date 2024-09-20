# GCP Firewall rule updater

* Uses GCP service account with Compute Network Admin role
* Creates a new firewall rule if it doesn't exist
* Allows all traffic between your public IP /24 subnet and GCP account. 
* Runs as cron job to periodically update the firewall

## Required variables

```
GOOGLE_APPLICATION_CREDENTIALS=/mnt/secrets/gcp-service-account.json
PROJECT_ID=personal-1101
FIREWALL_RULE_NAME=allow-home-ip
NETWORK_NAME=default
CRON_EXPRESSION='30 4 * * *'
```

* For local testing, modify `docker_run` and execute it
