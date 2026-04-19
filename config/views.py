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
    html = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>KodoMeal 検索画面</title>
    </head>
    <body>
    <div class="header">
        <h1 class="app-title">KodoMeal</h1>
    </div>
        
        <form method="get" class="search-form">
            <input type="text" class="keyword-input" name="keyword" placeholder="キーワード入力">
            
            <div class="menu-tag-group">

                <h2 class="menu-title">Kids Menu</h2>
                
                <button type="button" class="menu-tag-button">うどん</button>
                <button type="button" class="menu-tag-button">ラーメン</button>
                <button type="button" class="menu-tag-button">カレー</button>
                <button type="button" class="menu-tag-button">パスタ</button>
                
            </div>
            
            <button type="button" class="detail-search-button">＋詳細検索</button>
            <button type="submit" class="search-button">検索する</button>
        </form>
        
        <nav class="bottom-nav">
            <button type="button" class="nav-button">お気に入り</button>
            <button type="button" class="nav-button">検索する</button>
            <a href="/login/" class="nav-button">ログイン</a>
        </nav>
    </body>
    </html>    
    """
    return HttpResponse(html)
