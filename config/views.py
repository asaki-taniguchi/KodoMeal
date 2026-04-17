from django.http import HttpResponse

def portfolio_top(request):
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
        
        <div>
            <button>このアプリにアクセス</button>
        </div>
        
    </body>
    </html>
    """
    return HttpResponse(html)

def app_top(request):
    return HttpResponse("KodoMeal検索画面")
