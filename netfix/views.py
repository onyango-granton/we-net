from django.shortcuts import render

from users.models import User, Company,Customer
from services.models import Service,Service_Request
from datetime import date

def home(request):
    return render(request, 'users/home.html', {'user': request.user})
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def user_profile(request, name):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        return render(request, 'users/error.html', {'message': 'User not found'})

    if user.is_customer:
        return customer_profile(request, user)
    elif user.is_company:
        return company_profile(request, user)
    else:
        return render(request, 'users/error.html', {'message': 'Invalid user type'})
    
def customer_profile(request, user):
    service_request = Service_Request.objects.filter(user_id=user.id)
    user_age = None

    if user.is_customer:
        customer = Customer.objects.get(user_id=user.id)
        user_age = calculate_age(customer.birth)

    return render(request, 'users/profile.html', {
        'user': user,
        'user_age': user_age,
        'service_request': service_request
    })

def company_profile(request, user):
    services = Service.objects.filter(name_company=user.username).order_by("-date")
    company = Company.objects.get(user_id=user.id)

    return render(request, 'users/profile.html', {
        'user': user,
        'user_age': None,
        'user_company': company.field,
        'services': services
    })