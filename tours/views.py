from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from tours.data import tours, departures, title, subtitle, description
from random import sample

def main_view(request):
   tour = dict(sample(tours.items(), 6))
   return render(request, "tours/index.html", context={'title': title,
                                                       'departures': departures,
                                                       'tours': tours,
                                                       'subtitle': subtitle,
                                                       'description': description,
                                                       'tour': tour,
                                                       })
def departure_view(request, departure: str):
   if departure in departures.keys():
       copytour = tours.copy()
       deptour = []
       for i in tours.keys():
           if tours[i]['departure'] == departure:
               copytour[i]['numtour'] = i
               deptour += [copytour[i]]
       minprice = min([i['price'] for i in deptour])
       maxprice = max([i['price'] for i in deptour])
       minnight = min([i['nights'] for i in deptour])
       maxnight = max([i['nights'] for i in deptour])

   return render(request, "tours/departure.html", context={'title': title,
                                                       'deptour':deptour,
                                                       'from': departures[departure],
                                                       'minprice': minprice,
                                                       'maxprice': maxprice,
                                                       'minnight': minnight,
                                                       'maxnight': maxnight,
                                                       'departures': departures,
                                                       'tours': tours,
                                                       'title': subtitle,
                                                       'description': description,
                                                       'cnt': len(deptour)
                                                       })
def tour_view(request, id: int):
    tours_departures = tours.get(id).get("departure")
    for key, values in departures.items():
        if key == tours_departures:
            tours_departures = values
    tour = tours.get(id)
    tours_stars = "★" * int(tours.get(id).get("stars"))
    return render(request, 'tours/tour.html', context={'tour': tour,
                                                       'departures': departures,
                                                       'description': description,
                                                       'tours_departures': tours_departures,
                                                       'tours_stars': tours_stars,
                                                       })


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините!')


def custom_handler400(request, exception):
    # Call when SuspiciousOperation raised
    return HttpResponseBadRequest('Неверный запрос!')


def custom_handler403(request, exception):
    # Call when PermissionDenied raised
    return HttpResponseForbidden('Доступ запрещен!')


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')