from django.core.management.base import BaseCommand
from dashboardmanager.models import DashboardLayout
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample dashboard layouts for user ID 3'

    def handle(self, *args, **options):
        try:
            # Get user ID 3
            user = User.objects.get(id=3)
            
            # Delete existing layouts for this user
            DashboardLayout.objects.filter(user=user).delete()
            
            # Create sample layouts
            sample_layouts = [
                {
                    'name': 'Default Layout',
                    'description': 'Standard 3x2 grid layout',
                    'is_default': True,
                    'layout_data': {
                        'widgets': [
                            {'id': 1, 'x': 0, 'y': 0, 'w': 6, 'h': 4},
                            {'id': 2, 'x': 6, 'y': 0, 'w': 6, 'h': 4},
                            {'id': 3, 'x': 0, 'y': 4, 'w': 12, 'h': 4}
                        ]
                    }
                },
                {
                    'name': 'Wide Layout',
                    'description': 'Two wide widgets layout',
                    'layout_data': {
                        'widgets': [
                            {'id': 1, 'x': 0, 'y': 0, 'w': 8, 'h': 4},
                            {'id': 2, 'x': 8, 'y': 0, 'w': 4, 'h': 4},
                            {'id': 3, 'x': 0, 'y': 4, 'w': 12, 'h': 4}
                        ]
                    }
                },
                {
                    'name': 'Tall Layout',
                    'description': 'Three tall widgets layout',
                    'layout_data': {
                        'widgets': [
                            {'id': 1, 'x': 0, 'y': 0, 'w': 4, 'h': 6},
                            {'id': 2, 'x': 4, 'y': 0, 'w': 4, 'h': 6},
                            {'id': 3, 'x': 8, 'y': 0, 'w': 4, 'h': 6}
                        ]
                    }
                },
                {
                    'name': 'Compact Layout',
                    'description': 'Four compact widgets layout',
                    'layout_data': {
                        'widgets': [
                            {'id': 1, 'x': 0, 'y': 0, 'w': 6, 'h': 3},
                            {'id': 2, 'x': 6, 'y': 0, 'w': 6, 'h': 3},
                            {'id': 3, 'x': 0, 'y': 3, 'w': 6, 'h': 3},
                            {'id': 4, 'x': 6, 'y': 3, 'w': 6, 'h': 3}
                        ]
                    }
                },
                {
                    'name': 'Full Width Layout',
                    'description': 'Three full width widgets layout',
                    'layout_data': {
                        'widgets': [
                            {'id': 1, 'x': 0, 'y': 0, 'w': 12, 'h': 3},
                            {'id': 2, 'x': 0, 'y': 3, 'w': 12, 'h': 3},
                            {'id': 3, 'x': 0, 'y': 6, 'w': 12, 'h': 3}
                        ]
                    }
                }
            ]
            
            # Create layouts in the database
            for layout_data in sample_layouts:
                DashboardLayout.objects.create(
                    user=user,
                    name=layout_data['name'],
                    description=layout_data['description'],
                    is_default=layout_data.get('is_default', False),
                    layout_data=layout_data['layout_data']
                )
            
            self.stdout.write(
                self.style.SUCCESS('Successfully created sample layouts for user ID 3')
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('User with ID 3 does not exist')
            )
