#!/bin/bash
# clean_inactive_customers.sh
# This script removes customers who have not made any orders in the past year
# and logs the results to /tmp/customer_cleanup_log.txt.

LOG_FILE="/tmp/customer_cleanup_log.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting cleanup of inactive customers..." >> "$LOG_FILE"

# Run Django shell command
python3 manage.py shell <<EOF >> "$LOG_FILE" 2>&1
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

# Find customers who have no orders in the last year
inactive_customers = Customer.objects.filter(
    orders__date__lt=one_year_ago
).distinct()

count = inactive_customers.count()
inactive_customers.delete()

print(f"[INFO] Deleted {count} inactive customers who haven't ordered since {one_year_ago.date()}.")
EOF

echo "[$TIMESTAMP] Cleanup complete." >> "$LOG_FILE"
echo "Cleanup complete! Log written to $LOG_FILE"
