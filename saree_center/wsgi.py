import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv  # Import dotenv for .env support

# Load environment variables
project_folder = os.path.expanduser('~/saree_center')  # Update this with your project path
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saree_center.settings')

application = get_wsgi_application()
