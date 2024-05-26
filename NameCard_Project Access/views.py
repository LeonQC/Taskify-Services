from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserDetailedNameCard, ProjectAccess
from .serializers import UserDetailedNameCardSerializer, ProjectAccessSerializer

class UserDetailedNameCardlView(APIView):
    def get(self, request):
        user_id = request.query_params.get('UserId')
        if not user_id:
            return Response({
                'success': False,
                'msg': 'UserId parameter is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserDetailedNameCard.objects.get(id=user_id)
        except UserDetailedNameCard.DoesNotExist:
            return Response({
                'success': False,
                'msg': 'User not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserDetailedNameCardSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectAccessView(APIView):
    def put(self, request):
        user_id = request.query_params.get('User_id')
        if not user_id:
            return Response({
                'status': 'error',
                'msg': 'User_id parameter is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserDetailedNameCard.objects.get(id=user_id)
        except UserDetailedNameCard.DoesNotExist:
            return Response({
                'status': 'error',
                'msg': 'User not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        roles = request.data.get('roles', [])
        access, created = ProjectAccess.objects.get_or_create(user=user)
        access.roles = roles
        access.save()

        return Response({
            'status': 'success',
            'data': {
                'userId': user.id,
                'roles': access.roles
            }
        }, status=status.HTTP_200_OK)
