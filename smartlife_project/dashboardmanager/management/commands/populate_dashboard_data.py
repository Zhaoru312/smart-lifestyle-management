from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboardmanager.models import (
    UserProfile, DashboardBookmark, DashboardNote, DashboardReminder, DashboardShortcut,
    HeroSection, Feature, Testimonial, FAQ, ContactMessage, Newsletter
)
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the database with initial data for testing and demonstration purposes.'

    def handle(self, *args, **kwargs):
        # Create users for demonstration
        users = [
            {'username': 'demo_user1', 'email': 'demo1@example.com'},
            {'username': 'demo_user2', 'email': 'demo2@example.com'},
            {'username': 'demo_user3', 'email': 'demo3@example.com'}
        ]
        for user_data in users:
            user, created = User.objects.get_or_create(**user_data)
            if created:
                user.set_password('password123')
                user.save()

        # Create UserProfiles
        profiles = [
            {'bio': 'This is a demo user profile.', 'birth_date': '1990-01-01', 'phone_number': '1234567890',
             'address': '123 Demo Street', 'website': 'https://example.com', 'interests': 'Coding, Music, Art',
             'profession': 'Software Developer', 'company': 'Demo Company', 'location': 'Demo City', 'preferred_currency': 'USD'},
            {'bio': 'Another demo profile.', 'birth_date': '1985-05-15', 'phone_number': '0987654321',
             'address': '456 Another St', 'website': 'https://anotherexample.com', 'interests': 'Reading, Traveling',
             'profession': 'Data Scientist', 'company': 'Another Company', 'location': 'Another City', 'preferred_currency': 'EUR'},
            {'bio': 'Yet another profile.', 'birth_date': '1995-07-20', 'phone_number': '1122334455',
             'address': '789 Yet St', 'website': 'https://yetanotherexample.com', 'interests': 'Sports, Cooking',
             'profession': 'Project Manager', 'company': 'Yet Another Company', 'location': 'Yet Another City', 'preferred_currency': 'GBP'}
        ]
        for i, profile_data in enumerate(profiles):
            UserProfile.objects.get_or_create(user=User.objects.get(username=f'demo_user{i+1}'), **profile_data)

        # Create DashboardBookmarks
        bookmarks = [
            {'title': 'Django Documentation', 'url': 'https://docs.djangoproject.com/',
             'description': 'Official Django documentation site.', 'category': 'Documentation',
             'tags': 'django,python,web', 'is_favorite': True},
            {'title': 'Python Official Site', 'url': 'https://www.python.org/',
             'description': 'The official home of the Python Programming Language.', 'category': 'Programming',
             'tags': 'python,programming,language', 'is_favorite': False},
            {'title': 'Stack Overflow', 'url': 'https://stackoverflow.com/',
             'description': 'A platform for asking and answering programming questions.', 'category': 'Community',
             'tags': 'questions,answers,community', 'is_favorite': True}
        ]
        for bookmark_data in bookmarks:
            DashboardBookmark.objects.get_or_create(user=user, **bookmark_data)

        # Create DashboardNotes
        notes = [
            {'title': 'Meeting Notes', 'content': 'Discuss project milestones and deadlines.',
             'category': 'Meetings', 'tags': 'work,meeting,notes', 'is_pinned': True},
            {'title': 'Project Ideas', 'content': 'Brainstorming session for new project ideas.',
             'category': 'Brainstorming', 'tags': 'ideas,project,brainstorm', 'is_pinned': False},
            {'title': 'Daily Log', 'content': 'Record of daily activities and tasks.',
             'category': 'Daily', 'tags': 'log,daily,activities', 'is_pinned': True}
        ]
        for note_data in notes:
            DashboardNote.objects.get_or_create(user=user, **note_data)

        # Create DashboardReminders
        reminders = [
            {'title': 'Project Deadline', 'description': 'Complete the project by the end of the month.',
             'reminder_type': 'monthly', 'due_date': timezone.now() + timezone.timedelta(days=30),
             'repeat_interval': 30, 'is_completed': False},
            {'title': 'Weekly Meeting', 'description': 'Attend the weekly team meeting.',
             'reminder_type': 'weekly', 'due_date': timezone.now() + timezone.timedelta(days=7),
             'repeat_interval': 7, 'is_completed': False},
            {'title': 'Daily Standup', 'description': 'Participate in the daily standup call.',
             'reminder_type': 'daily', 'due_date': timezone.now() + timezone.timedelta(days=1),
             'repeat_interval': 1, 'is_completed': False}
        ]
        for reminder_data in reminders:
            DashboardReminder.objects.get_or_create(user=user, **reminder_data)

        # Create DashboardShortcuts
        shortcuts = [
            {'title': 'Open Dashboard', 'icon': 'fa-dashboard', 'shortcut_key': 'Ctrl+D',
             'action': '/dashboard/', 'description': 'Shortcut to open the dashboard.', 'is_active': True},
            {'title': 'New Task', 'icon': 'fa-tasks', 'shortcut_key': 'Ctrl+T',
             'action': '/tasks/new/', 'description': 'Shortcut to create a new task.', 'is_active': True},
            {'title': 'View Calendar', 'icon': 'fa-calendar', 'shortcut_key': 'Ctrl+C',
             'action': '/calendar/', 'description': 'Shortcut to view the calendar.', 'is_active': False}
        ]
        for shortcut_data in shortcuts:
            DashboardShortcut.objects.get_or_create(user=user, **shortcut_data)

        # Create HeroSections
        hero_sections = [
            {'title': 'Welcome to Smart Lifestyle Management', 'subtitle': 'Manage your lifestyle efficiently.',
             'call_to_action_text': 'Get Started', 'call_to_action_url': 'https://example.com/start', 'is_active': True},
            {'title': 'Discover New Features', 'subtitle': 'Explore the latest updates and features.',
             'call_to_action_text': 'Learn More', 'call_to_action_url': 'https://example.com/features', 'is_active': True},
            {'title': 'Join Our Community', 'subtitle': 'Connect with like-minded individuals.',
             'call_to_action_text': 'Sign Up', 'call_to_action_url': 'https://example.com/signup', 'is_active': False}
        ]
        for hero_data in hero_sections:
            HeroSection.objects.get_or_create(**hero_data)

        # Create Features
        features = [
            {'title': 'task', 'description': 'Manage your daily tasks and to-do list.',
             'icon': 'fa-tasks', 'order': 1, 'is_active': True},
            {'title': 'finance', 'description': 'Manage your finances and track expenses.',
             'icon': 'fa-chart-line', 'order': 2, 'is_active': True},
            {'title': 'fitness', 'description': 'Track your workouts and fitness goals.',
             'icon': 'fa-dumbbell', 'order': 3, 'is_active': True},
            {'title': 'habit', 'description': 'Build and track your habits.',
             'icon': 'fa-check-circle', 'order': 4, 'is_active': True},
            {'title': 'meal', 'description': 'Log and plan your meals.',
             'icon': 'fa-utensils', 'order': 5, 'is_active': True},
            {'title': 'mental', 'description': 'Track your mental health and mood.',
             'icon': 'fa-brain', 'order': 6, 'is_active': True}
        ]
        for feature_data in features:
            Feature.objects.get_or_create(**feature_data)

        # Create Testimonials
        testimonials = [
            {'name': 'John Doe', 'role': 'CEO',
             'content': 'This app has transformed the way I manage my daily activities.', 'rating': 5, 'is_active': True,
             'image': 'testimonials/john_doe.jpg'},
            {'name': 'Jane Smith', 'role': 'CTO',
             'content': 'A must-have tool for anyone looking to improve their productivity.', 'rating': 4, 'is_active': True,
             'image': 'testimonials/jane_smith.jpg'},
            {'name': 'Alice Johnson', 'role': 'Product Manager',
             'content': 'The features are intuitive and easy to use.', 'rating': 4, 'is_active': False,
             'image': 'testimonials/alice_johnson.jpg'}
        ]
        for testimonial_data in testimonials:
            Testimonial.objects.get_or_create(**testimonial_data)

        # Create FAQs
        faqs = [
            {'question': 'How do I reset my password?', 'answer': 'Go to the login page and click on "Forgot Password".',
             'category': 'Account', 'order': 1, 'is_active': True},
            {'question': 'How can I contact support?', 'answer': 'You can reach us via the contact form on our website.',
             'category': 'Support', 'order': 2, 'is_active': True},
            {'question': 'What features are available?', 'answer': 'We offer a wide range of features including task management and financial tracking.',
             'category': 'Features', 'order': 3, 'is_active': False}
        ]
        for faq_data in faqs:
            FAQ.objects.get_or_create(**faq_data)

        # Create ContactMessages
        contact_messages = [
            {'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'subject': 'Inquiry about features',
             'message': 'Can you provide more details about the task management feature?', 'is_read': False},
            {'name': 'Bob Brown', 'email': 'bob.brown@example.com', 'subject': 'Account issue',
             'message': 'I am unable to access my account. Can you help?', 'is_read': True},
            {'name': 'Charlie Green', 'email': 'charlie.green@example.com', 'subject': 'Feedback',
             'message': 'Great app! Looking forward to more features.', 'is_read': False}
        ]
        for message_data in contact_messages:
            ContactMessage.objects.get_or_create(**message_data)

        # Create Newsletters
        newsletters = [
            {'email': 'subscriber@example.com', 'is_active': True},
            {'email': 'user2@example.com', 'is_active': False},
            {'email': 'user3@example.com', 'is_active': True}
        ]
        for newsletter_data in newsletters:
            Newsletter.objects.get_or_create(**newsletter_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with initial data.'))
