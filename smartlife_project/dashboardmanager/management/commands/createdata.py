from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboardmanager.models import UserProfile, DashboardWidget, UserPreference, DashboardNotification, DashboardLayout
import json
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Create sample data for the dashboard'

    def handle(self, *args, **options):
        # Create sample user
        try:
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpassword123'
            )
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                bio='Sample user for testing the dashboard',
                birth_date='1990-01-01',
                phone_number='+1234567890',
                address='123 Test Street',
                preferred_currency='USD'
            )

            # Create user preferences
            UserPreference.objects.create(
                user=user,
                theme='light',
                layout='grid'
            )

            # Create sample widgets
            widgets = [
                {
                    'title': 'Statistics Overview',
                    'widget_type': 'stats',
                    'position_x': 0,
                    'position_y': 0,
                    'width': 6,
                    'height': 4,
                    'config': {
                        'stats': [
                            {'label': 'Total Expenses', 'value': 1234.56},
                            {'label': 'Workout Streak', 'value': 14},
                            {'label': 'Active Habits', 'value': 5},
                            {'label': 'Pending Tasks', 'value': 3}
                        ]
                    }
                },
                {
                    'title': 'Expense Chart',
                    'widget_type': 'chart',
                    'position_x': 6,
                    'position_y': 0,
                    'width': 6,
                    'height': 4,
                    'config': {
                        'type': 'line',
                        'data': {
                            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                            'datasets': [{
                                'label': 'Monthly Expenses',
                                'data': [123, 156, 198, 234, 278, 321]
                            }]
                        }
                    }
                },
                {
                    'title': 'Recent Activity',
                    'widget_type': 'list',
                    'position_x': 0,
                    'position_y': 4,
                    'width': 12,
                    'height': 4,
                    'config': {
                        'items': [
                            {'date': '2025-05-09', 'activity': 'Completed morning workout'},
                            {'date': '2025-05-08', 'activity': 'Paid monthly bills'},
                            {'date': '2025-05-07', 'activity': 'Updated budget plan'},
                            {'date': '2025-05-06', 'activity': 'Started new habit tracking'}
                        ]
                    }
                }
            ]

            # Create widgets in database
            for widget_data in widgets:
                DashboardWidget.objects.create(
                    user=user,
                    title=widget_data['title'],
                    widget_type=widget_data['widget_type'],
                    position_x=widget_data['position_x'],
                    position_y=widget_data['position_y'],
                    width=widget_data['width'],
                    height=widget_data['height'],
                    config=widget_data['config']
                )

            # Create sample notifications
            for i in range(5):
                DashboardNotification.objects.create(
                    user=user,
                    title=f'Notification {i+1}',
                    message=f'This is notification {i+1}',
                    category=random.choice(['info', 'warning', 'success']),
                    is_read=False
                )

            # Create sample layouts
            layouts = [
                {
                    'name': 'Default Layout',
                    'description': 'The default dashboard layout',
                    'layout_data': {
                        'widgets': [
                            {'id': 1, 'x': 0, 'y': 0, 'w': 6, 'h': 4},
                            {'id': 2, 'x': 6, 'y': 0, 'w': 6, 'h': 4},
                            {'id': 3, 'x': 0, 'y': 4, 'w': 12, 'h': 4}
                        ]
                    },
                    'is_default': True
                },
                {
                    'name': 'Compact Layout',
                    'description': 'A more compact dashboard layout',
                    'layout_data': {
                        'widgets': [
                            {'id': 1, 'x': 0, 'y': 0, 'w': 4, 'h': 3},
                            {'id': 2, 'x': 4, 'y': 0, 'w': 4, 'h': 3},
                            {'id': 3, 'x': 8, 'y': 0, 'w': 4, 'h': 3}
                        ]
                    },
                    'is_default': False
                }
            ]

            # Create layouts in database
            for layout_data in layouts:
                DashboardLayout.objects.create(
                    user=user,
                    name=layout_data['name'],
                    description=layout_data['description'],
                    layout_data=layout_data['layout_data'],
                    is_default=layout_data['is_default'],
                    is_public=True  # Make layouts public for testing
                )

            self.stdout.write(self.style.SUCCESS('Successfully created sample data'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating sample data: {str(e)}'))
