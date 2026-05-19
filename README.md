# EventHub – Event Management System

A medium-level Django project with MySQL, Django REST Framework, and Bootstrap 5.

---

## Tech Stack
- Python 3.11+
- Django 4.2
- Django REST Framework
- MySQL
- Bootstrap 5
- Pillow

---

## Setup Instructions

### 1. Create MySQL Database
Open MySQL and run:
```sql
CREATE DATABASE event_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Configure Database Password
Open `event_management/settings.py` and update:
```python
'PASSWORD': 'your_mysql_password',  # ← put your MySQL password here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load Sample Data
```bash
python manage.py seed_data
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run the Server
```bash
python manage.py runserver
```

### 8. Open in Browser
- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## Test Accounts (after seed_data)
| Role | Username | Password |
|---|---|---|
| Organizer | organizer1 | organizer123 |
| Attendee | attendee1 | attendee123 |

---

## User Roles

### Attendee
- Register / Login
- Browse & search events
- Book tickets
- Cancel bookings
- Write reviews

### Organizer
- Register as organizer
- Create / Edit / Delete events
- Upload event banners
- View bookings & revenue

### Admin
- Access /admin/ panel
- Manage all users, events, bookings, categories

---

## API Endpoints
| Method | URL | Description |
|---|---|---|
| POST | /api/auth/register/ | Register user |
| POST | /api/auth/login/ | Get auth token |
| GET | /api/events/ | List all events |
| GET | /api/events/<id>/ | Event detail |
| GET/POST | /api/bookings/ | My bookings / Create booking |
| PUT | /api/bookings/<id>/cancel/ | Cancel booking |

---

## Project Structure
```
event_management/
├── event_management/    # Project settings
├── accounts/            # User & Organizer auth
├── events/              # Events, Bookings, Reviews
├── templates/           # HTML templates
├── static/              # CSS, JS
├── media/               # Uploaded images
└── manage.py
```
