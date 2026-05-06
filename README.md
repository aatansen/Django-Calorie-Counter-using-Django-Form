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
    - [Templates Setup](#templates-setup)
    - [User Authentication](#user-authentication)
    - [Dashboard](#dashboard)
    - [Profile](#profile)
    - [Update Profile](#update-profile)
    - [Add and Update Calories](#add-and-update-calories)
    - [Show All Added Calories](#show-all-added-calories)
    - [Delete Added Calories](#delete-added-calories)

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

### Templates Setup

- Create all the HTML files

  ```txt
  📁 templates
  ├── 📁 master
  │   ├── 🌐 base-form.html
  │   ├── 🌐 base.html
  │   ├── 🌐 message.html
  │   └── 🌐 nav.html
  ├── 🌐 calorie-list.html
  ├── 🌐 dashboard.html
  └── 🌐 profile.html
  ```

  - We are using single [base-form.html](./CalorieCounter/templates/master/base-form.html) for every form we defined in [forms.py](./CalorieCounter/forms.py)

- Make sure to use crispy form in the [base-form.html](./CalorieCounter/templates/master/base-form.html)

---
[⬆️ Go to Context](#context)

### User Authentication

- For registration
  - Create function in [views.py](./CalorieCounter/views.py)

    ```py
    def register_page(request):
        if request.method == 'POST':
            form_data = RegistrationForm(request.POST)
            if form_data.is_valid():
                form_data.save()
                messages.success(request, 'Registration Successfully')
                return redirect('login_page')
        form_data = RegistrationForm()
        context = {
            "form_data": form_data,
            'form_title': 'User Registration Form',
            'form_btn': 'Register'
        }
        return render(request, 'master/base-form.html',context)
    ```

    - Make sure [base-form.html](./CalorieCounter/templates/master/base-form.html) has `csrf torken` and `method="POST" enctype="multipart/form-data"`

  - Add URL pattern in [urls.py](./CalorieCounter/urls.py)

- For login
  - Create function in [views.py](./CalorieCounter/views.py)

    ```py
    def login_page(request):
        if request.method == 'POST':
            form_data = LoginForm(request, request.POST)
            if form_data.is_valid():
                user = form_data.get_user()
                login(request, user)
                messages.success(request, 'Login Successfully')
                return redirect('dashboard_page')

        form_data = LoginForm()
        context = {
            'form_data': form_data,
            'form_title': 'User Login Form',
            'form_btn': 'Login'
        }
        return render(request, 'master/base-form.html', context)
    ```

    - In here we used `get_user()` from the form data

  - Add URL pattern in [urls.py](./CalorieCounter/)

- Do the same for `logout_page` function

---
[⬆️ Go to Context](#context)

### Dashboard

- Just render it for first time, later we will update (first user need to update their profile and add calories then we will update this dashboard)
- Update as follows

  ```py
  @login_required
  def dashboard_page(request):
      try:
          current_user = request.user
          bmr = round(request.user.user_info.bmr, 2)
      except:
          current_user = None
          bmr = 0

      today = date.today()
      today_consumed_data = ConsumedCalories.objects.filter(
          consumed_by=current_user,
          created_at=today
      )
      total_consumed_calories = today_consumed_data.aggregate(
          total_caloire=Sum('calorie'),
          total_count=Count('calorie')
      )
      total_caloire = total_consumed_calories['total_caloire']
      less_more = bmr - total_caloire

      if bmr > total_caloire:
          suggestion = 'Eat more'
      else:
          suggestion = 'Eat less'

      context = {
          'required_calories': bmr,
          'today_consumed_data': today_consumed_data,
          'consumed_calories': total_caloire,
          'total_count': total_consumed_calories['total_count'],
          'less_more': less_more,
          'suggestion': suggestion,

      }

      return render(request, 'dashboard.html', context)
  ```

  - We used `aggregate` for calculation in the query
    - First we filter based on user and the day user consumed those foods then we use `aggregate` to do some calculation which are imported by `from django.db.models import Sum, Count`

---
[⬆️ Go to Context](#context)

### Profile

- Just render this page
- We will access all data using `related_name`

---
[⬆️ Go to Context](#context)

### Update Profile

- Render the following views

  ```py
  @login_required
  def update_profile(request):
      try:
          current_user = request.user.user_info
      except:
          current_user = None

      if request.method == 'POST':
          form_data = ProfileUpdateForm(request.POST, instance=current_user)
          if form_data.is_valid():
              data = form_data.save(commit=False)
              data.user = request.user

              weight = data.weight
              height = data.height
              age = data.age
              if data.gender == 'Male':
                  # BMR= 66.47+(13.75 x weight in kg) + (5.003 x height in cm) - (6.755 x age in years)
                  bmr_calculate = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
              else:
                  # BMR=655.1+(9.563 x weight in kg)+(1.850 xheight in cm) - (4.676 x age in years)
                  bmr_calculate = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

              data.bmr = bmr_calculate
              data.save()
              messages.success(request, 'Profile UPdate Successfully')
              return redirect('profile_page')

      form_data = ProfileUpdateForm(instance=current_user)
      context = {
          'form_data': form_data,
          'form_title': "Update Profile Info",
          'form_btn': 'Update'
      }
      return render(request, 'master/base-form.html', context)
  ```

  - In here we used `commit=False` to calculate and assigning the field which we excluded in [forms.py](./CalorieCounter/forms.py)

---
[⬆️ Go to Context](#context)

### Add and Update Calories

- Both are using same HTML base form

  ```py
  def add_calorie(request):
      if request.method == 'POST':
          form_data = ConsumedCalorieForm(request.POST)
          if form_data.is_valid():
              data = form_data.save(commit=False)
              data.consumed_by = request.user
              data.save()
              messages.success(request, 'Successfully')
              return redirect('consumed_calories_list')
      form_data = ConsumedCalorieForm()
      context = {
          'form_data': form_data,
          'form_title': "Add Calorie Info",
          'form_btn': 'Add Calorie'
      }
      return render(request, 'master/base-form.html', context)


  def update_calorie(request, id):
      try:
          data = ConsumedCalories.objects.get(id=id)
      except:
          data = None
      if request.method == 'POST':
          form_data = ConsumedCalorieForm(request.POST, instance=data)
          if form_data.is_valid():
              data = form_data.save(commit=False)
              data.consumed_by = request.user
              data.save()
              messages.success(request, 'Successfully')
              return redirect('consumed_calories_list')
      form_data = ConsumedCalorieForm(instance=data)
      context = {
          'form_data': form_data,
          'form_title': "UPdate Calorie Info",
          'form_btn': 'UPdate Calorie'
      }
      return render(request, 'master/base-form.html', context)
  ```

---
[⬆️ Go to Context](#context)

### Show All Added Calories

  ```py
  def consumed_calories_list(request):
      consumed_data = ConsumedCalories.objects.filter(consumed_by=request.user)

      context = {
          'consumed_data': consumed_data
      }

      return render(request, 'calorie-list.html', context)
  ```

---
[⬆️ Go to Context](#context)

### Delete Added Calories

  ```py
  def delete_calorie(request, id):
      try:
          data = ConsumedCalories.objects.get(id=id)
          data.delete()
          messages.success(request, 'Successfully')
      except:
          data = None
          messages.success(request, 'Not Successful')
      return redirect('consumed_calories_list')
  ```

---
[⬆️ Go to Context](#context)
