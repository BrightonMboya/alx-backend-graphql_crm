#!/bin/bash

# Run Django shell command to delete inactive customers
deleted_count=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer
from orders.models import Order

cutoff_date = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(id__in=Order.objects.filter(created_at__gte=cutoff_date).values_list('customer_id', flat=True))
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the result with timestamp
echo \"[\$(date)] Deleted \$deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
