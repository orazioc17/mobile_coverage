import pandas as pd
from unittest.mock import patch, Mock
from django.test import TestCase
from django.urls import reverse

from api.serializers import CoverageQuerySerializer
from api.services.mobile_coverage import MobileCoverage


class CoverageSerializerTests(TestCase):

    def test_serializer_valid_address(self):
        serializer = CoverageQuerySerializer(data={"address": "42 rue papernest 75011 Paris"})
        self.assertTrue(serializer.is_valid())

    def test_serializer_reject_invalid_chars(self):
        serializer = CoverageQuerySerializer(data={"address": "//////"})
        self.assertFalse(serializer.is_valid())

    def test_serializer_too_short(self):
        serializer = CoverageQuerySerializer(data={"address": "a"})
        self.assertFalse(serializer.is_valid())

    def test_serializer_normalizes_whitespace(self):
        serializer = CoverageQuerySerializer(data={"address": "  10   Avenue   XYZ   "})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["address"], "10 Avenue XYZ")


class MobileCoverageServiceTests(TestCase):
    def setUp(self):
        self.mock_df = pd.DataFrame({
            "city": ["paris", "paris"],
            "operator": ["Orange", "SFR"],
            "2G": [1, 1],
            "3G": [1, 1],
            "4G": [0, 1],
        })

    @patch("api.services.mobile_coverage.requests.get")
    @patch("api.services.mobile_coverage.MobileCoverage.get_coverage_df")
    def test_retrieve_coverage_valid(self, mock_df, mock_get):
        mock_df.return_value = self.mock_df

        mock_resp = Mock()
        mock_resp.json.return_value = {
            "features": [
                {"properties": {"city": "paris", "score": 0.92}}
            ]
        }
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        service = MobileCoverage("42 rue papernest Paris")
        result = service.retrieve_coverage()

        self.assertIn("coverage", result)
        self.assertIn("Orange", result["coverage"])
        self.assertIn("SFR", result["coverage"])
        self.assertEqual(result["coverage"]["Orange"]["4G"], False)
        self.assertEqual(result["coverage"]["SFR"]["4G"], True)

    @patch("api.services.mobile_coverage.requests.get")
    def test_address_no_match(self, mock_get):
        mock_resp = Mock()
        mock_resp.json.return_value = {"features": []}
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        service = MobileCoverage("invalid address")

        with self.assertRaises(ValueError):
            service.get_city()

    @patch("api.services.mobile_coverage.requests.get")
    def test_geocoding_api_failure(self, mock_get):
        mock_get.side_effect = Exception("service down")

        service = MobileCoverage("any address")

        with self.assertRaises(Exception):
            service.get_city()

    @patch("api.services.mobile_coverage.requests.get")
    @patch("api.services.mobile_coverage.MobileCoverage.get_coverage_df")
    def test_no_coverage_for_city(self, mock_df, mock_get):
        mock_df.return_value = pd.DataFrame(columns=["city", "operator", "2G", "3G", "4G"])

        mock_resp = Mock()
        mock_resp.json.return_value = {
            "features": [{"properties": {"city": "unknown-city", "score": 0.8}}]
        }
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        service = MobileCoverage("some address")
        result = service.retrieve_coverage()

        self.assertEqual(result["coverage"], {})


class EndpointTests(TestCase):

    @patch("api.services.mobile_coverage.MobileCoverage.retrieve_coverage")
    def test_coverage_endpoint_success(self, mock_service):
        mock_service.return_value = {"coverage": {"Orange": {"2G": True}}}

        url = reverse("get_coverage")
        response = self.client.get(url, {"address": "42 rue papernest Paris"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("Orange", response.json()["coverage"])

    def test_coverage_endpoint_missing_param(self):
        url = reverse("get_coverage")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)
