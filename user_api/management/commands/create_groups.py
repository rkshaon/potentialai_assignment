from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission



class Command(BaseCommand):
    help = 'Create groups and assign permissions'


    def handle(self, *args, **options):
        # Create Vendor Group
        vendor_group, created = Group.objects.get_or_create(name='Vendor')

        # Create Customer Group
        customer_group, created = Group.objects.get_or_create(name='Customer')

        # Assign permissions to Vendor Group (customize based on your needs)
        vendor_permissions = Permission.objects.filter(content_type__app_label='user_api')
        vendor_group.permissions.set(vendor_permissions)

        # Assign permissions to Customer Group (customize based on your needs)
        customer_permissions = Permission.objects.filter(content_type__app_label='user_api')
        customer_group.permissions.set(customer_permissions)

        self.stdout.write(self.style.SUCCESS('Groups and permissions created successfully.'))
