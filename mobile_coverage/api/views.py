from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from .serializers import CoverageQuerySerializer
from .data.data_retriever import MobileCoverage

# Create your views here.

@swagger_auto_schema(
    method='get', 
    query_serializer=CoverageQuerySerializer, 
    operation_description="Get mobile coverages for a given address"
)
@api_view(['GET'])
def get_coverage(request):

    serializer = CoverageQuerySerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    address = serializer.validated_data['address']
    
    mobile_coverage = MobileCoverage(address)
    coverage_data = mobile_coverage.retrieve_coverage()
    print(coverage_data)

    data = {
        "message": "Mobile Coverage API is working!"
    }
    return Response(data)
