import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.conf import settings

def get_lat_lng_from_address(address):
    api_key = settings.GOOGLE_GEOCODING_API_KEY
    
    if not api_key:
        raise ValueError('Google Geocoding APIキーが設定されていません。')
    
    endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
    
    params = {
        'address': address,
        'key': api_key,
        'language': 'ja',
        'region': 'jp',
    }
    
    url = f'{endpoint}?{urlencode(params)}'
    
    try:
        with urlopen(url, timeout=10) as response:
            response_body = response.read().decode('utf-8')
            data = json.loads(response_body)
            
    except (HTTPError, URLError, TimeoutError) as error:
        raise ValueError('Geocoding APIへの接続に失敗しました。') from error

    status = data.get('status')

    if status != 'OK' or not data.get('results'):
        error_message = data.get('error_message', '')
        raise ValueError(
            f'住所から位置情報を取得できませんでした。status={status}, message={error_message}'
        )

    location = data['results'][0]['geometry']['location']
    
    latitude = float(location['lat'])
    longitude = float(location['lng'])
    
    return latitude, longitude