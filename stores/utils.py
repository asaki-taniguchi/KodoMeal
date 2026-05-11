import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.conf import settings

PREFECTURES = [
    '北海道',
    '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
    '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
    '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県',
    '岐阜県', '静岡県', '愛知県', '三重県',
    '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県',
    '鳥取県', '島根県', '岡山県', '広島県', '山口県',
    '徳島県', '香川県', '愛媛県', '高知県',
    '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県',
    '沖縄県',
]

def get_prefecture_from_address(address):
    for prefecture in PREFECTURES:
        if prefecture in address:
            return prefecture

    return None
    
def get_lat_lng_from_address(address):
    api_key = settings.GOOGLE_GEOCODING_API_KEY
    
    if not api_key:
        raise ValueError('Google Geocoding APIキーが設定されていません。')
    
    input_prefecture = get_prefecture_from_address(address)
    
    if not input_prefecture:
        raise ValueError('都道府県を含む住所を入力してください。')
    
    if not re.search(r'[0-9 ０−９]', address):
        raise ValueError('住所は番地まで入力してください。')
    
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
        
    result = data['results'][0]
    
    if result.get('partial_match'):
        raise ValueError('入力住所に完全一致する位置情報を取得できませんでした。')
    
    formatted_address = result.get('formatted_address', '')
    
    if input_prefecture not in formatted_address:
        raise ValueError('入力住所と取得結果の都道府県が一致しません。')
    
    address_components = result.get('address_components', [])
    
    is_japan = any(
        'country' in component.get('types', [])
        and component.get('short_name') == 'JP'
        for component in address_components
    )
    
    if not is_japan:
        raise ValueError('日本国内の住所を入力してください。')

    location_type = result.get('geometry', {}).get('location_type')
    
    if location_type == 'APPROXIMATE':
        raise ValueError('住所が曖昧すぎます。番地まで入力してください。')
    
    location = result['geometry']['location']
    
    latitude = float(location['lat'])
    longitude = float(location['lng'])
    
    return latitude, longitude