from .serializers import UserSerializer
from users.models import User
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def registration_view(request):

	if request.method == 'POST':
		serializer = UserSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			user = serializer.save()
			data['response'] = 'successfully registered new user.'
		
		else:
			data = serializer.errors
		return Response(data)



 