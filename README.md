# data_classification

Dataset Tagging System

This project provides a REST API for managing datasets and tags, designed for a text-tagging system where operators can categorize texts within various datasets. Operators and administrators have different access permissions and can perform specific actions based on their roles. The system supports Dockerization for simplified deployment and includes daily logging of operator activities.

### Features

    Dataset Management:
        Create datasets (e.g., sentiment analysis datasets).
        Define categories (tags) within datasets (e.g., happiness, sadness, anger).
        Enable or disable tags within each dataset.

    Tagging Process:
        Operators can add one or multiple tags to each text.
        Full-text search capability within dataset entries.

    Reporting:
        Daily logging of operator activities in text tagging.
        Generate a daily report at 00:00 of the previous day's operator activities.

    Access Control:
        Role-based access (admin and operator).
        Admins can assign or restrict dataset access to operators.

    CSV Data Import: Upload a CSV file to add text data to a specific dataset.

    Dockerization: The project is Dockerized for easy deployment.


### Tech Stack

    Backend: Django REST Framework
    Database: SQLite (configurable)
    Task Queue: Celery with Redis as the broker
    Deployment: Docker, Gunicorn, and Nginx


### Setup
#### Prerequisites

Docker & Docker Compose installed on your system.

#### Installation

Clone the repository:
```
$ git clone <repository-url>
$ cd <project-directory>
```

#### Environment Setup:

Create a .env file for environment variables (e.g., database settings, Redis configuration).
Example .env file:
```
DJANGO_SECRET_KEY=your_secret_key
DEBUG=1
```

#### Build and Run the Containers:
```
$ docker-compose up --build
```

Run Migrations: Migrations will automatically run on startup.


### Create superuser (admin):
```
$ docker-compose exec web sh -c "echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python manage.py shell"
```


### Accessing the Application
    API Endpoints: Hosted at http://localhost:80/api/
    Accounts Endpoints: Hosted at http://localhost:80/account/
    Admin Panel: Accessible for superuser/admin at http://localhost:80/admin/


### API Documentation
Once the project is running, navigate to the /swagger/ endpoint in your web browser to view the API documentation and learn how to use the project endpoints.

> [!NOTE]
whenever you wnat to make a post request you should send the CSRF token in the header

for example if you're using ubuntu commandline to make request you can make post request like this

```
curl -X POST http://localhost:8000/api/your-endpoint/ \
    -H "Content-Type: application/json" \
    -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
    -b "sessionid=YOUR_SESSIONID; csrftoken=YOUR_CSRF_TOKEN" \
    -d '{"name": "abcd"}'
```

### Uploading CSV file to import data in database
In the http://localhost:8000/api/UploadCSVFile/ Endpoint admin can upload a
csv file to import data in database.
file content example:


| dataset_name  | tags_name         | text_content                            |
| ------------- | ----------------- | --------------------------------------- | 
| Dataset A     | Tag1 Tag2         | This is the content of the first text.  |
| Dataset A     | Tag2 Tag3         | This is the content of the second text. |
| Dataset B     | Tag4              | text content for a different dataset.   |
| Dataset C     | Tag1 Tag5 Tag6    | Some more content for a new dataset.    |

If dataset or tags or texts exist in the database the imported data will update them and if they don't the instances will create in the database.