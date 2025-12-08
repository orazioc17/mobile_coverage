from rest_framework import serializers

class CoverageQuerySerializer(serializers.Serializer):
    address = serializers.CharField(
        required=True, 
        allow_blank=False,
        help_text="Address to get mobile coverage for. Example: 42 rue papernest 75011 Paris",
        trim_whitespace=True,
    )
