# ISMS - IUT Student Management System

## 1. Project Overview

ISMS (IUT Student Management System) is a web-based application built using Django as the backend framework and MySQL as the database. The system is designed to manage various aspects of student information, admissions, faculty, and staff activities within the context of the Islamic University of Technology (IUT).

# 2. Project Structure
## Project Root
- **.gitignore**
- **README.md**
- **manage.py**

## `admin_app` App
- **init.py**
- **admin.py**
- **apps.py**
- **filters.py**
- **forms.py**
- **models.py**
- **tests.py**
- **views.py**

## `isms` App
- **init.py**
- **asgi.py**
- **settings.py**
- **urls.py**
- **wsgi.py**

## `main` App
- **init.py**
- **admin.py**
- **admission_models.py**
- **admission_forms.py**
- **apps.py**
- **facultyViews.py**
- **forms.py**
- **models.py**
- **staff_libViews.py**
- **staff_medViews.py**
- **studentViews.py**
- **tests.py**
- **urls.py**
- **views.py**

## `static` Directory
### css
- **style.css**
### images
- **logo.png**
### pdf

## `templates` Directory
### admin_temp
### admission_temp
### faculty_temp
### staff_lib_temp
### staff_med_temp
### student_temp
- **baselogin.html**
- **general_login.html**
- **homepage.html**
- **logError.html**
- **signinFaculty.html**
- **signinStaff.html**
- **signinStudent.html**

## 3. Project Components

### 3.1. `admin_app`

- **Description:** This app manages administrative functionalities.
- **Key Files:**
  - `admin.py`: Handles admin-related configurations.
  - `filters.py`: Manages filters for admin views.
  - `forms.py`: Defines forms used in admin views.
  - `models.py`: Defines models specific to the admin app.
  - `tests.py`: Contains test cases.
  - `views.py`: Implements views for the admin app.

### 3.2. `isms`

- **Description:** The core app containing project settings and configurations.
- **Key Files:**
  - `settings.py`: Includes project-wide settings and configurations.
  - `urls.py`: Defines URL patterns for the entire project.

### 3.3. `main`

- **Description:** Manages main functionalities including student, faculty, and staff views.
- **Key Files:**
  - `admin.py`: Handles admin-related configurations for the main app.
  - `admission_models.py`: Defines models related to student admissions.
  - `admission_forms.py`: Defines forms related to student admissions.
  - `facultyViews.py`: Implements views related to faculty.
  - `forms.py`: Defines general forms used in the main app.
  - `models.py`: Defines models for the main app.
  - `staff_libViews.py`: Implements views related to library staff.
  - `staff_medViews.py`: Implements views related to medical staff.
  - `studentViews.py`: Implements views related to students.
  - `urls.py`: Defines URL patterns specific to the main app.
  - `views.py`: Implements generic views.

### 3.4. `static`

- **Description:** Contains static files such as stylesheets, images, and PDFs.
- **Key Subdirectories:**
  - `css`: Contains CSS stylesheets.
  - `images`: Stores image files.
  - `pdf`: Stores PDF documents.

### 3.5. `templates`

- **Description:** Holds HTML templates organized by functional categories.
- **Key Subdirectories:**
  - `admin_temp`: Templates related to admin functionalities.
  - `admission_temp`: Templates related to student admission.
  - `faculty_temp`: Templates related to faculty functionalities.
  - `staff_lib_temp`: Templates related to library staff functionalities.
  - `staff_med_temp`: Templates related to medical staff functionalities.
  - `student_temp`: Templates related to student functionalities.




## 4. Usage
- Clone the repository.
- Install dependencies with `pip install -r requirements.txt`.
- Configure Django settings in `settings.py`.
- Migrations for sql `python manage.py makemigrations`
- Run migrations: `python manage.py migrate`.
- Start the development server: `python manage.py runserver`.

## 5. Contributing

- Fork the repository.
- Create a new branch: `git checkout -b feature_branch`.
- Commit changes: `git commit -m 'Add new feature'`.
- Push to the branch: `git push origin feature_branch`.
- Submit a pull request.

## 6. License

This project is licensed under the [MIT License](LICENSE).

---


