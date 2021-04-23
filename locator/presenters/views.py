# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response
from locator.presenters.factories import LocatorFactory
from clientlocator.exceptions import ClientLocatorException


# Register your viewsets here.
class LocatorViewSet(viewsets.GenericViewSet):
    """
    API made using Django Rest Framework
    """

    factory = LocatorFactory()
    http_method_names = ["get", "post"]

    @action(methods=["POST"], detail=False, url_path="search")
    def search_clients(self, request):
        """
           Endpoint to search a list of users by coordinates
           :param request:
           :return: dict
        """
        try:
            search_results = self.factory.create_search_iterator(data=request.data)
            return Response(search_results, status=HTTP_200_OK)
        except Exception as error:
            if isinstance(error, ClientLocatorException):
                return Response({"msg": error.args[0]}, status=HTTP_200_OK)
            else:
                return Response(error, status=HTTP_500_INTERNAL_SERVER_ERROR)
