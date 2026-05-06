<div align="center">
<h1>Django Calorie Counter (Django Form)</h1>
</div>

---

# Context

- [Context](#context)
  - [Question](#question)
  - [Solution](#solution)
    - [Virtual Environment Setup](#virtual-environment-setup)
    - [Project \& App Setup](#project--app-setup)
    - [Create Models](#create-models)
    - [Register Models in Admin](#register-models-in-admin)
    - [Database Migrations](#database-migrations)
    - [Superuser Create](#superuser-create)
    - [Create Django Forms](#create-django-forms)

## Question

> Develop a Calorie Counter that can be used to estimate the number of calories a person needs to consume each day. This calculator can also provide some simple guidelines for gaining or losing weight. Users can also keep track of how many calories he/she needs and how much he/she consumes in a day. To calculate calories, we have two formulas:
>
> For a male
>
> - `BMR= 66.47+(13.75 x weight in kg) + (5.003 x height in cm) - (6.755 x age in years)`
>
> For a female
>
> - `BMR=655.1+(9.563 x weight in kg)+(1.850 xheight in cm) - (4.676 x age in years)`

- Job Specification information:

  1. Create a new Django project named `Name_ID_CaloryCounter` and a `Calorie Counter app`.
  2. Define your Calorie Counter models.
  3. Create views for Login (username/email and password) and Registration (`username`, `email`, `password`, `confirm password`) pages.
  4. Create a `django-form` to take input `Name`, `Age`, `Gender`, `Height`, `Weight` etc.
  5. Create a Django form to take input daily consumed calories (`Item name`, `Calorie consumed`)
  6. Create a dashboard where the user can view the required calories for her/him and the consumed calories daily.
  7. Define URL Patterns and configure project-level URLs.
  8. Implement the required Function and Logic in the `view.py` file.

- Job Specification information:
  - Create a new Django project. (Naming Convention: `Name_ID_CaloryCounter`)
  - Run migration to create the data tables.
  - Create a superuser. (`username`: `admin`, `password`: `1234`)
  - Register your models to the Django admin.

---
[⬆️ Go to Context](#context)

## Solution

### Virtual Environment Setup

- Create virtual environment

  ```sh
  py -m venv .venv
  ```

- Activate virtual environment

  ```sh
  .venv\Scripts\activate.bat
  ```

- Install required packages

  ```sh
  pip install django pillow crispy-bootstrap5
  ```

---
[⬆️ Go to Context](#context)

### Project & App Setup

- Project

  ```sh
  django-admin startproject Tansen_101_CaloryCounter
  ```

- App

  ```sh
  py manage.py startapp CalorieCounter
  ```

- Add app name in [settings.py](./Tansen_101_CaloryCounter/settings.py) `INSTALLED_APPS`

  ```py
  INSTALLED_APPS = [
      ...
      # my apps
      'CalorieCounter'
  ]
  ```

---
[⬆️ Go to Context](#context)

### Create Models

- Open [models.py](./CalorieCounter/models.py) and create models

  - User authentication model

    ```py
    class User(AbstractUser):

        def __str__(self):
            return f'{self.username}'
    ```

    - We will use this model for registration (`username`, `email`, `password`, `confirm password`)
    - We need to add a variable `AUTH_USER_MODEL` in [settings.py](./Tansen_101_CaloryCounter/settings.py)

      ```py
      # auth model (app_name.model_name)
      AUTH_USER_MODEL='CalorieCounter.User'
      ```

  - User profile model

    ```py
    #Name, Age, Gender, Height, Weight
    class BasicInfoModel(models.Model):
        GENDER_TYPES = [
            ('Male','Male'),
            ('Female','Female'),
        ]
        user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name='user_info',
            null=True
        )
        name = models.CharField(max_length=100, null=True)
        age = models.PositiveIntegerField(null=True)
        gender = models.CharField(choices=GENDER_TYPES, max_length=10, null=True)
        height = models.FloatField(null=True)
        weight = models.FloatField(null=True)
        bmr =models.FloatField(null=True)

        def __str__(self):
            return f'{self.name}'
    ```

    - We will use this model for storing user profile data
    - In question `Name, Age, Gender, Height, Weight` are mentioned but we defined two more here, one is relationship field `user` and another field is for `bmr` calculation
    - In relationship we made `one-to-one (OneToOneField)` cause one user can have only one profile

  - Calorie consumed model

    ```py
    # consumed calories (Item name, Calorie consumed)
    class ConsumedCalories(models.Model):
        item_name = models.CharField(max_length=200, null=True)
        calorie = models.FloatField(null=True)
        created_at = models.DateField(auto_now_add=True, null=True)
        consumed_by = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            null=True,
            related_name='user_calorie'
        )

        def __str__(self):
            return f'{self.item_name}-{self.consumed_by}'
    ```

    - We will use this model to store user consumed calories
    - In question Item `name, Calorie consumed` only two field mentioned but we created two more, one is relationship field `consumed_by` and another is `created_at`
    - In relationship we made `one-to-many (ForeignKey)` relation cause one user can eat many food items, `created_at` field defined to calculate daily calories

---
[⬆️ Go to Context](#context)

### Register Models in Admin

- Register all models in [admin.py](./CalorieCounter/admin.py)

  ```py
  from django.contrib import admin
  from CalorieCounter.models import *

  # Register your models here.
  admin.site.register([
      User,
      BasicInfoModel,
      ConsumedCalories,
  ])
  ```

---
[⬆️ Go to Context](#context)

### Database Migrations

- Project Level Migrations

  ```sh
  py manage.py makemigrations
  ```

  ```sh
  py manage.py migrate
  ```

- App Level Migrations

  ```sh
  py manage.py makemigrations CalorieCounter
  ```

  ```sh
  py manage.py migrate CalorieCounter
  ```

---
[⬆️ Go to Context](#context)

### Superuser Create

- Create superuser

  ```sh
  py manage.py createsuperuser
  ```

---
[⬆️ Go to Context](#context)

### Create Django Forms

- Create a file [forms.py](./CalorieCounter/forms.py) and create django forms in it

  - `RegistrationForm` and `LoginForm`

    ```py

    from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

    # user creation form
    class RegistrationForm(UserCreationForm):
        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']

    # authentication form
    class LoginForm(AuthenticationForm):
        pass
    ```

    - Both form is based on our custom user model which we named `User` in [models.py](./CalorieCounter/models.py)
    - Here `password1` and `password2` in register page one is password and another is confirm password
    - Comment this part in [settings.py](./Tansen_101_CaloryCounter/settings.py) to skip default validation

      ```py
      # AUTH_PASSWORD_VALIDATORS = [
      #     {
      #         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
      #     },
      #     {
      #         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
      #     },
      #     {
      #         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
      #     },
      #     {
      #         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
      #     },
      # ]
      ```

  - `ProfileUpdateForm`

    ```py
    # profile form
    class ProfileUpdateForm(forms.ModelForm):
        class Meta:
            model = BasicInfoModel
            fields = '__all__'
            exclude = ['user', 'bmr']
    ```

    - We named it update profile cause after account creation user will update their profile
    - The excluded two fields will be handle in [views.py](./CalorieCounter/views.py)

  - `ConsumedCalorieForm`

    ```py
    # calorie form
    class ConsumedCalorieForm(forms.ModelForm):
        class Meta:
            model = ConsumedCalories
            fields = '__all__'
            exclude = ['consumed_by']
    ```

    - Using this form user will add their consumed foods each time they eat
    - `consumed_by` is the relationship in the model so it is excluded and will be handle in [views.py](./CalorieCounter/views.py)

---
[⬆️ Go to Context](#context)
