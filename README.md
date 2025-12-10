# mobile_coverage
Technical test. Api to get mobile network coverage by operators in France from a string address

TODO: explain how to download and add communes.gpkg, just in case



score is a value returned by the official French Geocoding API (Géoplateforme).
While not formally documented as a confidence rating, it appears to represent how closely the query matches the returned address.
We expose it to help clients evaluate the reliability of the geocoding result.