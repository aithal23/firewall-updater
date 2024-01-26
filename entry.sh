#!/bin/bash

# Start the cron daemon
service cron start

printenv > /etc/cron.d/my-cron-job
# Set the provided cron expression
echo "$CRON_EXPRESSION /usr/local/bin/python /usr/src/app/src/main.py >> /var/log/bot.log 2>&1" >> /etc/cron.d/my-cron-job

# Apply cron jobs
crontab /etc/cron.d/my-cron-job

# Keep the container running
tail -f /dev/null
