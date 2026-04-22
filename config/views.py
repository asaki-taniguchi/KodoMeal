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