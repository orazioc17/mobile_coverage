from rest_framework import serializers
import re


class CoverageQuerySerializer(serializers.Serializer):
    address = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=255,
        help_text="Address to search mobile coverage for. Example: 42 rue papernest 75011 Paris",
        trim_whitespace=True,
    )

    def validate_address(self, value):
        normalized = " ".join(value.split())

        # Rejecting too-short inputs
        if len(normalized) < 5:
            raise serializers.ValidationError("Address appears too short.")

        # Reject inputs without any alphabetical characters
        if not re.search("[a-zA-Z]", normalized):
            raise serializers.ValidationError("Address must contain alphabetic characters.")

        # Reject strings made of symbols only
        if re.match(r"^[\W_]+$", normalized):
            raise serializers.ValidationError("Address contains invalid characters.")

        return normalized
