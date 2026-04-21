from django.http import HttpResponse
from django.shortcuts import render

def portfolio_top(request): #ポートフォリオトップ画面
    html = """
    <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
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
        {'name': 'キッズカフェ ひまわり', 'menu': 'パンケーキ'},
        {'name': 'うどん屋 マルちゃん', 'menu': 'うどん'},
        {'name': 'ファミリーレストラン さくら', 'menu':'カレー'},
        {'name': 'cafe sora', 'menu':'パスタ'},
        {'name': 'おやこダイニング nico', 'menu':'オムライス'},
        {'name': '中華ダイニング 好好', 'menu':'ラーメン'},
    ]
    
    if keyword :
        stores = [store for store in stores if keyword in s['name'] or keyword in s['menu']]
    
    return render(request, 'search_result.html', { #キーワード受け取る
        'keyword': keyword,
        'stores' : stores
    })