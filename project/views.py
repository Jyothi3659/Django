from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, generics
from rest_framework import viewsets
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
# Create your views here.

class GroupsView(APIView):

    def get(self,request):
        queryset = Activity.objects.all()
        page = request.GET.get('page',1)
        paginator = Paginator(queryset, 5)
        try:
            grp_paginated = paginator.page(page)
        except PageNotAnInteger:
            grp_paginated = paginator.page(1)
        except EmptyPage:
            grp_paginated = paginator.page(paginator.num_pages)
		#return render(request , 'groups_info.html', context={'grp_info':grp_info,'grp_no':range(grp_no)})
        return render(request , 'pagination.html', context={'grp_paginated':grp_paginated})


#relational filters 
class ActivityFilterAPIView(generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project_status', 'created_by__username']
    # search_fields = ['project_status', 'created_by__username']
    # filter_backends = (filters.SearchFilter,)
     


class ActivityAPIView(APIView):

    def get(self, request):
        permission_classes = (IsAuthenticated,)
        # import ipdb;ipdb.set_trace()
        activity = Activity.objects.all()
        serializer  = ActivitySerializer(activity, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        import ipdb; ipdb.set_trace()        
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # import ipdb; ipdb.set_trace()
            projects = Activity.objects.all().count()
            weightage_project = {}
            weightage_project['weightage'] = 100/projects
            projectweightageserializer = ProjectWeightageSerializer(data=weightage_project)
            if projectweightageserializer.is_valid():
                projectweightageserializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class MileStoneAPIView(APIView):

    def get(self, request):
        # import ipdb;ipdb.set_trace()
        milestone = MileStone.objects.all()
        serializer  = MilestoneSerializer(milestone, many = True)
        return Response(serializer.data)

    def post(self, request):
        # import ipdb; ipdb.set_trace()
        if (request.data.get('start') >= request.data.get('project_start_date')) & (request.data.get('start') <= request.data.get('project_end_date')):
            serializer = MilestoneSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# class GuardianAPIViewUpdate(APIView):

#     def post(self, request, id):
#         guardian = Guardian.objects.get(id=id)
#         serializer = GuardianSerializer(guardian, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GuardianAPIViewDelete(APIView):

#     def post(self, request, id):
#         # import ipdb; ipdb.set_trace()
#         guardian = Guardian.objects.get(id=id)
#         if guardian.active == 2:
#             Guardian.objects.filter(id=id).update(active=0)
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             guardian.objects.filter(id=id).update(active=2)
#             return Response(status=status.HTTP_204_NO_CONTENT)
