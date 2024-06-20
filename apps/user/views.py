# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .serializers import UserSerializer
# from rest_framework import status
# from .models import UserAccount

# class UserDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request,iduser, format=None):
#         if UserAccount.objects.filter(id_user=iduser).exists():
            
#             user = UserAccount.objects.get(id_user=iduser)
#             serializer = UserSerializer(user)

#             return Response({'user':serializer.data})
#         else:
#             return Response({'error':'user doesnt exist'}, status=status.HTTP_404_NOT_FOUND)