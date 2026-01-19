"""
Management command to populate initial complaint categories
Run: python manage.py populate_categories
"""
from django.core.management.base import BaseCommand
from complaints.models import Category


class Command(BaseCommand):
    help = 'Populate initial complaint categories for AI classification'

    def handle(self, *args, **kwargs):
        categories_data = [
            {
                'name': 'Electricity',
                'description': 'Issues related to power supply, street lights, transformers, and electrical infrastructure'
            },
            {
                'name': 'Water Supply',
                'description': 'Problems with water supply, pipelines, drainage, sewage, and water quality'
            },
            {
                'name': 'Road & Transport',
                'description': 'Road conditions, potholes, traffic signals, footpaths, and transportation issues'
            },
            {
                'name': 'Cleanliness',
                'description': 'Garbage collection, waste management, sanitation, and hygiene concerns'
            },
            {
                'name': 'Noise',
                'description': 'Noise pollution, loud music, construction noise, and sound disturbances'
            },
            {
                'name': 'Other',
                'description': 'General complaints and issues not covered by other categories'
            }
        ]

        created_count = 0
        updated_count = 0

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'[+] Created category: {category.name}')
                )
            else:
                # Update description if different
                if category.description != cat_data['description']:
                    category.description = cat_data['description']
                    category.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'[~] Updated category: {category.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.NOTICE(f'[-] Category exists: {category.name}')
                    )

        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS(
                f'Complete! Created: {created_count}, Updated: {updated_count}'
            )
        )
