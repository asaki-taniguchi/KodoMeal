from django.http import HttpResponse
from django.shortcuts import render

def portfolio_top(request): #ポートフォリオトップ画面
    html = """
    <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>KodoMeal</title>
        </head>
        <body>
    
        <h1>KodoMeal</h1> 
        
        <div>
            <p>アプリのスクショ</p> 
        </div>
        
        <div>
            <a href="#">企画書</a>
            <a href="#">画面設計図</a> 
            <a href="#">画面遷移図</a>
            <a href="#">ER図</a>
        </div>
        
        <a href="/kodomeal/" class="app-link-button">このアプリにアクセス</a>
        
    </body>
    </html>
    """
    return HttpResponse(html)

def app_top(request): #アプリトップ画面
    return render(request,'app_top.html')

def search_result(request):  #検索結果画面
    keyword = request.GET.get('keyword')
    
    stores = [
        {'id': 1, 'name': 'キッズカフェ ひまわり', 'menu': 'パンケーキ'},
        {'id': 2, 'name': 'うどん屋 マルちゃん', 'menu': 'うどん'},
        {'id': 3, 'name': 'ファミリーレストラン さくら', 'menu':'カレー'},
        {'id': 4, 'name': 'cafe sora', 'menu':'パスタ'},
        {'id': 5, 'name': 'おやこダイニング nico', 'menu':'オムライス'},
        {'id': 6, 'name': '中華ダイニング 好好', 'menu':'ラーメン'},
    ]
    
    if keyword :
        stores = [store for store in stores if keyword in store['name'] or keyword in store['menu']]
    
    return render(request, 'search_result.html', { #キーワード受け取る
        'keyword': keyword,
        'stores' : stores
    })
    
def store_detail(request, store_id):
    stores = [
        {
            'id': 1,
            'name': 'キッズカフェ ひまわり',
            'menu': 'パンケーキ',
            'address': '東京都渋谷区〇〇1-1-1',
            'phone': '03-1234-5678',
            'holiday': '不定休',
            'hours': '11:00〜20:00',
            'parking': 'あり(店舗前3台)',
            'has_kids_chair': True,
            'is_stroller_ok': True,
            'has_diapper': True,
            'has_kids_space': True
        },
        {
            'id': 2,
            'name': 'うどん屋 マルちゃん',
            'menu': 'うどん',
            'address': '東京都世田谷区〇〇2-2-2',
            'phone': '03-9876-5432',
            'holiday': '水曜',
            'hours': '10:00〜18:00',
            'parking': 'なし',
            'has_kids_chair': True,
            'is_stroller_ok': True,
            'has_diapper': False,
            'has_kids_space': False 
        },
        {
            'id': 3,
            'name': 'ファミリーレストラン さくら',
            'menu':'カレー',
            'address': '東京都杉並区〇〇3-3-3',
            'phone': '03-2222-3333',
            'holiday': '年中無休',
            'hours': '10:00〜22:00',
            'parking': 'あり(10台)',
            'has_kids_chair': True,
            'is_stroller_ok': True,
            'has_diapper': True,
            'has_kids_space': False
            },
        {
            'id': 4,
            'name': 'cafe sora',
            'menu':'パスタ',
            'address': '東京都目黒区〇〇4-4-4',
            'phone': '03-4444-5555',
            'holiday': '月曜',
            'hours': '10:00〜19:00',
            'parking': 'なし（近隣にコインパーキングあり)',
            'has_kids_chair': False,
            'is_stroller_ok': True,
            'has_diapper': False,
            'has_kids_space': False
            },
        {
            'id': 5,
            'name': 'おやこダイニング nico',
            'menu':'オムライス',
            'address': '東京都練馬区〇〇5-5-5',
            'phone': '03-6666-7777',
            'holiday': '木曜',
            'hours': '10:00〜17:00',
            'parking': 'あり(店舗前2台、第二駐車場3台)',
            'has_kids_chair': True,
            'is_stroller_ok': True,
            'has_diapper': True,
            'has_kids_space': True,
            },
        {
            'id': 6,
            'name': '中華ダイニング 好好',
            'menu':'ラーメン',
            'address': '東京都中野区〇〇6-6-6',
            'phone': '03-8888-9999',
            'holiday': '火曜',
            'hours': '11:00〜25:00',
            'parking': 'あり',
            'has_kids_chair': False,
            'is_stroller_ok': True,
            'has_diapper': False,
            'has_kids_space': False
            },
    ]
    
    store = next((store for store in stores if store['id'] == store_id), None)
    
    return render(request, 'store_detail.html', { 
        'store' : store
    })
    
    
    