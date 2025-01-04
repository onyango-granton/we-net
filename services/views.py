from django.shortcuts import render, redirect
from users.models import Company, User
from django.core.exceptions import ObjectDoesNotExist
from .models import Service, Service_Request
from .forms import CreateNewService, RequestServiceForm
from django.contrib.auth.decorators import login_required


def get_field_value(user_id):
    try:
        company = Company.objects.get(user_id=user_id)
        field_value = company.field
        return [field_value] if field_value != 'All in One' else [
            'Air Conditioner', 
            'Carpentry',
            'Electricity', 
            'Gardening',
            'Home Machines',
            'House Keeping',
            'Interior Design',
            'Locks', 
            'Painting', 
            'Plumbing',
            'Water Heaters'
        ]
    except Company.DoesNotExist:
        return []


@login_required
def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def get_company_name(user_id):
    try:
        company = User.objects.get(id=user_id)
        return company.username
    except User.DoesNotExist:
        return None


def service_field(request, field):
    try:
        services = Service.objects.filter(field__iexact=field)
        return render(request, 'services/list.html', {'services': services})
    except ObjectDoesNotExist:
        return redirect('/')


def create(request):
    user_id = request.user.id
    field_value = get_field_value(user_id)
    
    if request.method == 'POST':
        form = CreateNewService(request.POST, user_id=user_id)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            service = Service.objects.create(
                name=cleaned_data['name'],
                description=cleaned_data['description'],
                price_hour=cleaned_data['price_hour'],
                field=cleaned_data['field'],
                name_company=get_company_name(user_id),
                company_id=user_id
            )
            return redirect('/')
    else:
        form = CreateNewService(user_id=user_id)

    context = {'form': form, 'field_value': field_value}
    return render(request, 'services/create.html', context=context)


def request_service(request, id):
    service = Service.objects.get(id=id)
    
    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            requestService = Service_Request.objects.create(
                user_id=request.user.id,
                service_id=service.id,
                adress=data['adress'],
                nbre_hour=data['nbre_hour'],
                price_hour=service.price_hour,
                service_name=service.name,
                name_company=service.name_company,
                total_price=service.price_hour * data["nbre_hour"],
                field=service.field
            )
            return redirect('/')
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {'service': service, 'form': form})
