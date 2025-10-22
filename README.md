# RagaSpace Authentication Project

This Django project implements the requested email/password registration and login experience plus optional OAuth sign-in via Google, Facebook, and Apple using **django-allauth**.

## Getting Started

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
   ```
2. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply database migrations and create a superuser if desired:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # optional
   ```
4. Provide OAuth credentials (optional) by setting the following environment variables before running the server:
   - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
   - `FACEBOOK_CLIENT_ID`, `FACEBOOK_CLIENT_SECRET`
   - `APPLE_CLIENT_ID`, `APPLE_CLIENT_SECRET`, `APPLE_TEAM_ID`

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

Once dependencies are installed you can visit the register and login pages at `http://localhost:8000/accounts/register/` and `http://localhost:8000/accounts/login/` respectively. The "Create new account" link points to the registration form, and the dashboard page provides a logout link as requested.

## Troubleshooting

If you encounter `ModuleNotFoundError: No module named 'allauth'`, it means the dependencies have not been installed yet. Run `pip install -r requirements.txt` inside your activated virtual environment to resolve the error.
