from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from .models import Attractions, AttractionTags, UserRoute, RouteAttractions, UserMess
from .forms import LoginForm, UserRegistrationForm, RouteForm, AttractionForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


import math
import pandas as pd
from Routing.coordinates import get_coordinates
from Routing.do_routing import get_map
from TextAnalysis.descriptions import get_description
from TextAnalysis.create_tags import create_tag_monument


routs_number = 0
city = 'Москва'


def index(request):
    users_list = get_user_model().objects.all()
    routs_list = UserRoute.objects.filter()
    n1 = 0
    n2 = len(users_list)
    n3 = len(routs_list)
    n4 = routs_number
    numbers_list = [n1, n2, n3, n4]
    data = {'numbers': numbers_list}
    return render(request, "index.html", context=data)


def about(request):
    users_list = get_user_model().objects.all()
    routs_list = UserRoute.objects.filter()
    n1 = 0
    n2 = len(users_list)
    n3 = len(routs_list)
    n4 = routs_number
    numbers_list = [n1, n2, n3, n4]
    data = {'numbers': numbers_list}
    return render(request, "about.html", context=data)


def gallery(request, sheet_id):
    object_list = Attractions.objects.filter()
    list_len = len(object_list)
    n = math.ceil(list_len/12)
    numbers = [x+1 for x in range(n)]
    data_list = []
    for i in range(12):
        cur_id = (sheet_id-1)*12 + i
        if cur_id < list_len:
            link = f'/attraction/{object_list[cur_id].id}'
            img_link = f"images/attraction/{object_list[cur_id].img_link}"
            name = str(object_list[cur_id].name)
            cur_dict = {"link": link,
                        "img_link": img_link,
                        "name": name}
            data_list.append(cur_dict)
    data = {"collection": data_list, "numbers": numbers, "n": sheet_id}
    return render(request, "gallery.html", context=data)


def attraction(request, attraction_id):
    try:
        cur_attraction = Attractions.objects.get(id=attraction_id)
        name = cur_attraction.name
        img_link = f"images/attraction/{cur_attraction.img_link}"
        print(img_link)
        description = cur_attraction.short_description
        data = {"name": name, "img_link": img_link, "description": description}
        return render(request, "attraction.html", context=data)
    except ObjectDoesNotExist:
        redirect('/')



def statistics(request):
    return render(request, "statistics.html")


def articles(request, article_id):
    df_articles = pd.read_excel('./articles.xlsx', sheet_name=str(article_id))
    df_articles = df_articles.fillna('-')
    collection = []
    h0 = ''
    p0_1 = ''
    p0_2 = ''
    p0_3 = ''
    for cur_index, row in df_articles.iterrows():
        if cur_index == 0:
            h0 = row['h']
            p0_1 = row['p1']
            p0_2 = row['p2']
            p0_3 = row['p3']
        else:
            collection.append({'h': row['h'], 'p1': row['p1'], 'p2': row['p2'], 'p3': row['p3']})
    data = {"h0": h0, "p0_1": p0_1, "p0_2": p0_2, "p0_3": p0_3, "collection": collection}
    return render(request, "articles.html", context=data)


@login_required
def my_routs(request):
    my_routs_list = UserRoute.objects.filter(user=request.user.id)
    routs = []
    for route in my_routs_list:
        temp = {"name": route.route_name,
                "city": route.city,
                "text": route.route_text,
                "id": route.id}
        routs.append(temp)
    data = {"routs": routs}
    return render(request, "my_routs.html", context=data)


def cur_route(request, route_id):
    global city
    route = UserRoute.objects.get(id=route_id)
    route_attractions_list = RouteAttractions.objects.filter(route=route_id)
    name = route.route_name
    text = route.route_text
    if route.user == request.user:
        is_user = True
    else:
        is_user = False
    collection = []
    for cur_object in route_attractions_list:
        cur_attraction = Attractions.objects.get(id=cur_object.attraction)
        temp = {"point": cur_attraction.name,
                "address": cur_attraction.address,
                "description": cur_attraction.short_description}
        collection.append(temp)
    data = {"name": name, "city": city, "text": text, "collection": collection, "id": route_id, "is_user": is_user}
    return render(request, "cur_route.html", context=data)


def recommendations(request):
    my_routs_list = UserRoute.objects.filter(user__is_superuser=1)
    routs = []
    for route in my_routs_list:
        temp = {"name": route.route_name,
                "city": route.city,
                "text": route.route_text,
                "id": route.id}
        routs.append(temp)
    data = {"routs": routs}
    return render(request, "recommendations.html", context=data)


def patch_route(request, route_id):
    if request.POST:
        if '_edit' in request.POST:
            route = UserRoute.objects.get(id=route_id)
            city = route.city
            my_str = route.points_list
            if route.user == request.user:
                is_user = True
            else:
                is_user = False
            while True:
                if '\r' in my_str:
                    my_str = my_str.replace('\r', '')
                else:
                    break
            points = eval(my_str)
            points_str = ''
            for i in points:
                points_str += i
            form = RouteForm(initial={'route_name': route.route_name,
                                      'route_text': route.route_text,
                                      'points': points_str,
                                      'route_id': route_id})
            data = {"city_name": city, "form": form}
            return render(request, "new_route.html", context=data)
        elif '_delete' in request.POST:
            route = UserRoute.objects.get(id=route_id)
            route.delete()
            return redirect('/my_routs')
        elif '_make_route' in request.POST:
            return redirect(f'/routing/{route_id}')
        else:
            route_id = request.POST.get("route_id", -1)
            route = UserRoute.objects.get(id=route_id)
            points = request.POST.get("points", "Undefined")
            route.route_name = request.POST.get("route_name", "Undefined")
            route.route_text = request.POST.get("route_text", "Undefined")
            route.points_list = points.split("\n")
            route.save()
            return redirect('/my_routs')
    return redirect('/')


def choose_route(request):
    my_routs_list = UserRoute.objects.filter(user=request.user.id)
    routs = []
    for route in my_routs_list:
        temp = {"name": route.route_name,
                "city": route.city,
                "text": route.route_text,
                "id": route.id}
        routs.append(temp)
    recommendations_routs_list = UserRoute.objects.filter(user__is_superuser=1)
    for route in recommendations_routs_list:
        temp = {"name": route.route_name,
                "city": route.city,
                "text": route.route_text,
                "id": route.id}
        routs.append(temp)
    data = {"routs": routs}
    return render(request, "choose_route.html", context=data)


def routing(request, route_id=-1):
    global routs_number
    if route_id != -1:
        route = UserRoute.objects.get(id=route_id)
        city = route.city
        coordinates = route.coordinates_list
        coordinates = eval(coordinates)
        cur_map = get_map(coordinates)
        cur_map.save('map.html')
    data = {"map_src": "map.html"}
    routs_number += 1
    return render(request, "routing.html", context=data)


def send_mes(request):
    user_mes = UserMess()
    user_mes.name = request.POST.get("name", "Undefined")
    user_mes.gmail = request.POST.get("gmail", "Undefined")
    user_mes.theme = request.POST.get("theme", "Undefined")
    user_mes.mes = request.POST.get("mes", "Undefined")
    user_mes.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def new_route(request):
    city_name = request.POST.get("city_name", "Undefined")
    return redirect(f'/create_route/{city_name}')


@login_required
def create_route(request):
    global city
    if request.method == 'POST':
        points = request.POST.get("points", "Undefined")
        route = UserRoute()
        route.user = request.user
        route.city = city
        route.route_name = request.POST.get("route_name", "Undefined")
        route.route_text = request.POST.get("route_text", "Undefined")
        route.points_list = points.split("\n")
        route.save()
        return redirect('/my_routs')
    else:
        form = RouteForm()
        object_list = Attractions.objects.filter()
        collection = []
        for cur_obj in object_list:
            tags = AttractionTags.objects.filter(attraction=cur_obj.id)
            tags_list = [cur_tag.tag for cur_tag in tags]
            name = cur_obj.name
            address = cur_obj.address
            temp = {"name": name,
                    "address": address,
                    "tags": tags_list,
                    "city": city}
            collection.append(temp)
        data = {"city_name": city, "form": form, "collection": collection}
        return render(request, "new_route.html", context=data)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print(1)
                    return redirect('.')
                else:
                    print(2)
                    return redirect('.')
            else:
                print(3)
                return redirect('.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return redirect('/user_login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration.html', {'user_form': user_form})


def add_attraction(request):
    global city
    form = AttractionForm()
    if request.method == 'POST':
        name = request.POST.get("name")
        img_link = request.POST.get("img_link")
        address = request.POST.get("address")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        short_description = request.POST.get("short_description")
        if (address == '') and (latitude == '') and (longitude == '') and (short_description == ''):
            print('1')
            form = AttractionForm(initial={'name': name,
                                           'img_link': img_link})
            try:
                cur_address = get_coordinates(name)
            except TimeoutError:
                try:
                    cur_address = get_coordinates(name)
                except TimeoutError:
                    print('Адрес не найден')
                    return render(request, 'add_attraction.html', {'form': form})
            if cur_address[0] is not None:
                form = AttractionForm(initial={'name': name,
                                               'img_link': img_link,
                                               'address': cur_address[0],
                                               'latitude': cur_address[1],
                                               'longitude': cur_address[2]})
                return render(request, 'add_attraction.html', {'form': form})
            else:
                form = AttractionForm()
                return render(request, 'add_attraction.html', {'form': form})
        elif (address != '') and (latitude != '') and (longitude != '') and (short_description == ''):
            description = get_description(name, city)
            form = AttractionForm(initial={'name': name,
                                           'img_link': img_link,
                                           'address': address,
                                           'latitude': latitude,
                                           'longitude': longitude,
                                           'short_description': description})
            return render(request, 'add_attraction.html', {'form': form})
        elif (address != '') and (latitude != '') and (longitude != '') and (short_description != ''):
            attraction = Attractions()
            attraction.name = name
            attraction.img_link = img_link
            attraction.address = address
            attraction.latitude = latitude
            attraction.longitude = longitude
            attraction.short_description = short_description
            attraction.save()
    return render(request, 'add_attraction.html', {'form': form})


def create_tags(request):
    if request.POST:
        if '_monument' in request.POST:
            monument_names_list = ['памятник', 'монумент', 'бюст', 'скульптура', 'фонтан']
            create_tag_monument(monument_names_list, 'monument')
        elif '_parks' in request.POST:
            monument_names_list = ['парк', 'сад']
            create_tag_monument(monument_names_list, 'parks')
        elif '_location' in request.POST:
            print(3)
    return render(request, 'create_tags.html')
