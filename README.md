# cotw
Problem Definition : COTW have a list of places names that are in English which they would like to translate them into various native languages . They have published a list of priority languages and places that they would like to translate 

https://translator-client-qa.taethni.com/2021-indigitous-hackathon

*See input folder for example of places that requires translation

Method : Using Google map API to search for the translated name. Google map platform supports a number of languages that COTW desires to translate into https://developers.google.com/maps/faq


You would have to register on developers.google.com to get an API key.  

https://developers.google.com/maps/documentation/geocoding/overview

Example 1 : 

In the following example, we are looking for Gairigaun in the Nepalese language 
https://maps.googleapis.com/maps/api/geocode/json?address=Gairigaun&language=ne&key=

{'results': [{'address_components': [{'long_name': 'गैरिगौ', 'short_name': 'गैरिगौ', 'types': ['neighborhood', 'political']}, {'long_name': 'धरना', 'short_name': 'धरना', 'types': ['locality', 'political']}, {'long_name': 'दाङ', 'short_name': 'दाङ', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'लुम्बिनी प्रदेश', 'short_name': 'लुम्बिनी प्रदेश', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'नेपाल', 'short_name': 'NP', 'types': ['country', 'political']}, {'long_name': '22400', 'short_name': '22400', 'types': ['postal_code']}], 'formatted_address': 'गैरिगौ, धरना 22400, नेपाल', 'geometry': {'bounds': {'northeast': {'lat': 27.9983044, 'lng': 82.4121808}, 'southwest': {'lat': 27.9923551, 'lng': 82.40844729999999}}, 'location': {'lat': 27.9942491, 'lng': 82.4109403}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 27.9983044, 'lng': 82.4121808}, 'southwest': {'lat': 27.9923551, 'lng': 82.40844729999999}}}, 'place_id': 'ChIJXfUyyIqRlzkR0NUKz8XXuZ4', 'types': ['neighborhood', 'political']}], 'status': 'OK'}

Based on the types that were classified for the result, the returned result indicates that this is at ['neighborhood', 'political'] level. Hence from the address components, will search for the one with type matching ['neighborhood', 'political'] and extracting the "long_name" गैरिगौ

The example above was a simplified query that yields a positive search on Google map. However, a more detailed way of querying google map is needed as as google will return some wrong results if there were approximate matches. One way of constructing better query could be extracting information from ARCGIS Feature Service to concatentate places in {adm4_nm},{adm3_nm},{adm2_nm},{adm1_nm},country . Any latitude and longitude returned from ArcGIS can also be used to do reverseGeocoding


Verification of the accuracy of the search result will also need to be done 





