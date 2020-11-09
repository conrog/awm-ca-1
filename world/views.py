from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from . import models
from .models import Pub

# Create your views here.
@login_required
def update_location(request):
    try:
        user_profile = models.Profile.objects.get(user=request.user)
        if not user_profile:
            raise ValueError("Can't get User Detials")

        point = request.POST["point"].split(",")
        point = [float(part) for part in point]
        point = Point(point, srid=4326)

        user_profile.last_location = point
        user_profile.save()

        return JsonResponse({
            "message":f"Set location to {point.wkt}."},
            status=200 )
    except Exception as e:
        return JsonResponse({
            "message":str(e)},
            status=400 )

@login_required()
def get_nearest_pubs(request):
    try:
        user_profile = models.Profile.objects.get(user=request.user)
        user_location = user_profile.last_location
        lat = user_location[0]
        long = user_location[1]
        list = []

        queryset = Pub.objects.annotate(distance=Distance('location', Point(lat,long, srid=4326))).order_by('distance')[0:5]

        for query in queryset:
            list.append({
                'name' : query.name,
                'latitude': query.location[0],
                'longitude': query.location[1],
                'distance' : str(query.distance)
            })

        return JsonResponse({
            'data' : list,
        }, status=200)
    except Exception as e:
        return JsonResponse({
            "message":str(e)},
            status=400 )