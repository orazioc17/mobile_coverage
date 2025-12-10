from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import CoverageQuerySerializer
from .services.mobile_coverage import MobileCoverage

# Create your views here.

@swagger_auto_schema(
    method='get', 
    query_serializer=CoverageQuerySerializer, 
    operation_description="Get mobile coverages for a given address",
    responses={
        200: openapi.Response(
            description="Coverage result",
            examples={
                "application/json": {
                    "matched_city": "Paris",
                    "confidence_score": 0.95,
                    "coverage": {
                        "Orange": {"2G": True, "3G": True, "4G": True},
                        "SFR": {"2G": True, "3G": True, "4G": False},
                        "Bouygues": {"2G": True, "3G": True, "4G": True},
                        "Free": {"2G": False, "3G": True, "4G": True}
                    }
                }
            }
        ),
        400: "Bad Request - Invalid input or processing error",
        500: "Internal Server Error"
    }
)
@api_view(['GET'])
def get_coverage(request):

    serializer = CoverageQuerySerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    address = serializer.validated_data['address']
    
    mobile_coverage = MobileCoverage(address)
    try:
        coverage_data = mobile_coverage.retrieve_coverage()
    except ValueError as e:
        return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
    except RuntimeError as e:
        return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Unknown error occured [{str(e)}]"}, status=HTTP_400_BAD_REQUEST)
    
    return Response(coverage_data, status=HTTP_200_OK)
