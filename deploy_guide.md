# Deploy Guide — Gezira College Student ID Lookup

This guide deploys the app **for free** on [PythonAnywhere](https://www.pythonanywhere.com).

## Why PythonAnywhere (and not Render/Railway free tier)

You upload student photos manually through Django Admin, and they need to
**stay** on the server. Render's and Railway's free tiers use an ephemeral
filesystem — any file saved to disk (your `media/` folder, your SQLite file)
is wiped every time the app restarts or redeploys. PythonAnywhere's free
tier gives you a real persistent disk, no credit card required, and it
serves static/media files natively — no extra libraries needed (you only
have Django + Pillow, which is exactly what PythonAnywhere expects).

---

## 1. Push your project to GitHub (recommended)

```bash
git add .
git commit -m "Prepare for deployment"
git push
```

If you'd rather not use GitHub, you can upload a zip in step 3 instead.

## 2. Create your PythonAnywhere account

1. Go to https://www.pythonanywhere.com/registration/register/beginner/
2. Sign up for the **Beginner (Free)** account.

## 3. Get the code onto PythonAnywhere

Open a **Bash console** from the PythonAnywhere dashboard ("Consoles" tab → "Bash") and run:

```bash
git clone https://github.com/<your-username>/<your-repo>.git student_id_app
```

(No GitHub? Use the "Files" tab to upload a zip, then `unzip it.zip -d student_id_app`.)

## 4. Create a virtual environment

Still in the Bash console:

```bash
cd student_id_app
python3.10 -m venv venv
source venv/bin/activate
pip install django pillow
```

## 5. Configure the Web app

1. Go to the **Web** tab → **Add a new web app**.
2. Choose **Manual configuration** (not the Django wizard) → pick the same Python version as your venv (e.g. 3.10).
3. In the **Code** section, set:
   - **Source code**: `/home/<your-username>/student_id_app`
   - **Working directory**: `/home/<your-username>/student_id_app`
4. In the **Virtualenv** section, set:
   - `/home/<your-username>/student_id_app/venv`
5. Open the **WSGI configuration file** link and replace its contents with:

   ```python
   import os
   import sys

   path = '/home/<your-username>/student_id_app'
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_id.settings')
   os.environ.setdefault('DJANGO_ALLOWED_HOSTS', '<your-username>.pythonanywhere.com')
   os.environ.setdefault('DJANGO_DEBUG', 'False')
   # Generate one real secret key and paste it below (see step 6).
   os.environ.setdefault('DJANGO_SECRET_KEY', 'REPLACE_WITH_A_REAL_SECRET_KEY')

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

## 6. Generate a production secret key

Back in the Bash console:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copy the output into `DJANGO_SECRET_KEY` in the WSGI file from step 5.

## 7. Run migrations and create your admin login

```bash
cd ~/student_id_app
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 8. Map static and media files

On the **Web** tab, scroll to **Static files** and add two mappings:

| URL           | Directory                                              |
|---------------|---------------------------------------------------------|
| `/static/`    | `/home/<your-username>/student_id_app/staticfiles`      |
| `/media/`     | `/home/<your-username>/student_id_app/media`            |

## 9. Reload and test

Click the green **Reload** button at the top of the **Web** tab, then visit:

```
https://<your-username>.pythonanywhere.com
```

## 10. Add your students

Go to `https://<your-username>.pythonanywhere.com/admin/`, log in with the
superuser you created in step 7, and add students with their photo, name,
ID, college, batch, and semester. The homepage search accepts the ID typed
in either English or Arabic-Indic numerals (e.g. `11-3335` or `١١-٣٣٣٥`).

---

## Updating the app later

```bash
cd ~/student_id_app
git pull
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

Then hit **Reload** on the **Web** tab.

## Free tier limits to know

- The free PythonAnywhere account gives you a subdomain
  (`<your-username>.pythonanywhere.com`) — no custom domain on the free plan.
- Outbound internet access from free accounts is restricted to an allowlist,
  which doesn't matter here since this app makes no outbound requests.
- Disk quota is limited (~512MB) — plenty for SQLite + a modest number of
  student photos, but resize/compress photos before uploading if you have
  hundreds of students.
