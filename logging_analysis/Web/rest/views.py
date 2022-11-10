from rest_framework.decorators import api_view
from rest_framework.response import Response

from Web.models import Tar
from rest.serializers import TarSerializer


@api_view(['GET', 'POST'])
def tars_list(request):
    '''
    List all tasks, or create a new task.
    '''
    if request.method == 'GET':
        tasks = Tar.objects.all()
        serializer = TarSerializer(tasks, many=True)
        return Response(serializer.data)
