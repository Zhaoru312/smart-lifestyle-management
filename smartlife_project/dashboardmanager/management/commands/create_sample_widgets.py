from django.core.management.base import BaseCommand
from dashboardmanager.models import DashboardWidget
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample dashboard widgets for user ID 3'

    def handle(self, *args, **options):
        try:
            # Get user ID 3
            user = User.objects.get(id=3)
            
            # Create sample widgets
            sample_widgets = [
                {
                    'title': 'Daily Expenses',
                    'widget_type': 'stats',
                    'position_x': 0,
                    'position_y': 0,
                    'width': 6,
                    'height': 4,
                    'config': {
                        'data': 150.75,
                        'description': 'Total expenses today'
                    }
                },
                {
                    'title': 'Workout Progress',
                    'widget_type': 'chart',
                    'position_x': 6,
                    'position_y': 0,
                    'width': 6,
                    'height': 4,
                    'config': {
                        'chart_type': 'line',
                        'data': {
                            'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                            'datasets': [{
                                'label': 'Minutes',
                                'data': [30, 45, 0, 60, 40, 35, 50]
                            }]
                        }
                    }
                },
                {
                    'title': 'Task List',
                    'widget_type': 'list',
                    'position_x': 0,
                    'position_y': 4,
                    'width': 12,
                    'height': 4,
                    'config': {
                        'items': [
                            'Complete project report',
                            'Schedule team meeting',
                            'Review budget proposal',
                            'Update project timeline'
                        ]
                    }
                }
            ]
            
            # Create widgets in the database
            for widget_data in sample_widgets:
                DashboardWidget.objects.create(
                    user=user,
                    title=widget_data['title'],
                    widget_type=widget_data['widget_type'],
                    position_x=widget_data['position_x'],
                    position_y=widget_data['position_y'],
                    width=widget_data['width'],
                    height=widget_data['height'],
                    config=widget_data['config'],
                    is_active=True
                )
            
            self.stdout.write(
                self.style.SUCCESS('Successfully created sample widgets for user ID 3')
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('User with ID 3 does not exist')
            )
