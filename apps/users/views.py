from rest_framework.response import Response
from rest_framework.views import APIView


class TestAPIView(APIView):
    def get(self, request):
        return Response({"message": "Users API is working"})