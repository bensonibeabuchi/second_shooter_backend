from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

# Create your views here.
# Permission class to allow access only to the owner
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class ShotListView(generics.ListCreateAPIView):
    serializer_class = ShotListSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return ShotList.objects.filter(user=self.request.user)

class ShotListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShotListSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return ShotList.objects.filter(user=self.request.user)

class ConsentFormView(generics.ListCreateAPIView):
    serializer_class = ConsentFormSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return ConsentForm.objects.filter(photographer_name=self.request.user)

class ConsentFormDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConsentFormSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return ConsentForm.objects.filter(photographer_name=self.request.user)

class ProjectView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    

# class ShotListView(APIView):
#     serializer_class = ShotListSerializer
#     permission_classes = [AllowAny]

#     def get(self, request):
#         all_shot_list = ShotList.objects.all()
#         serialized_shot_list = ShotListSerializer(all_shot_list, many=True)
#         return Response(serialized_shot_list.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = ShotListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def put(self, request, pk):
#         try:
#             shot_list = ShotList.objects.get(pk=pk)
#         except ShotList.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ShotListSerializer(shot_list, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         try:
#             shot_list = ShotList.objects.get(pk=pk)
#         except ShotList.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ShotListSerializer(shot_list, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         try:
#             shot_list = ShotList.objects.get(pk=pk)
#         except ShotList.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         shot_list.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # ConsentForm View
# class ConsentFormView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         all_consent_forms = ConsentForm.objects.all()
#         serialized_consent_forms = ConsentFormSerializer(all_consent_forms, many=True)
#         return Response(serialized_consent_forms.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = ConsentFormSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         try:
#             consent_form = ConsentForm.objects.get(pk=pk)
#         except ConsentForm.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ConsentFormSerializer(consent_form, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         try:
#             consent_form = ConsentForm.objects.get(pk=pk)
#         except ConsentForm.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ConsentFormSerializer(consent_form, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         try:
#             consent_form = ConsentForm.objects.get(pk=pk)
#         except ConsentForm.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         consent_form.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# # Project View
# class ProjectView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         all_projects = Project.objects.all()
#         serialized_projects = ProjectSerializer(all_projects, many=True)
#         return Response(serialized_projects.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, pk):
#         try:
#             project = Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ProjectSerializer(project, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         try:
#             project = Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ProjectSerializer(project, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         try:
#             project = Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         project.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)