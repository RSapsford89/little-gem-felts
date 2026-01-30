from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from order.models import Order


class Command(BaseCommand):

    def handle(self, *args, **options):
        time_elapsed = timezone.now() - timedelta(minutes=15)

        old_orders = Order.objects.filter(is_paid=False, date__lt=time_elapsed)
        count = old_orders.count()

        if count == 0:
            self.stdout.write("no orders to remove")
            return

        self.stdout.write(f"old orders found: {count}")

        for order in old_orders:
            try:
                order.clean_up()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error running clean up on order: {order.order_id}: {e}"))
        self.stdout.write(self.style.SUCCESS(f"processed {count} orders"))
