from django.http import HttpResponse

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
        
        <div>
            <a href="/kodomeal/">
                <button>このアプリにアクセス</button>
            </a>
        </div>
        
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
        
        <form class="search-form">
            <input type="text" class="keyword-input" name="keyword" placeholder="キーワード入力">
            
            <div class="menu-tag-group">

                <h2 class="menu-title">Kids Menu</h2>
                
                <button type="button" class="menu-tag-button">うどん</button>
                <button type="button" class="menu-tag-button">ラーメン</button>
                <button type="button" class="menu-tag-button">カレー</button>
                <button type="button" class="menu-tag-button">パスタ</button>
                
            </div>
            
            <button type="button" class="detail-serch-button">＋詳細検索</button>
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

def register_view(request): #アカウント登録画面
    html = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>アカウント作成</title>
    </head>
    <body>
    
        <a href="/login/" class="back-link">◀︎戻る</a>
    
        <h1 class="register-title">新規登録</h1>
        
        <p class="description">
            以下全ての項目を入力してください
        </p>
        
        <form method="post" class="register-form">
        
            <div class="input-group">
                <label>ユーザー名</label><br>
                <input type="text" class="input-field" placeholder="ユーザー名">
                <p class="note">変更できません</p>
            </div>
            
            <div class="input-group">
                <label>メールアドレス</label><br>
                <input type="email" class="input-field" placeholder="sample@example.com">
            </div>
            
            <div class="input-group">
                <label>パスワード</label><br>
                <input type="password" class="input-field" placeholder="パスワード">
            </div>
            
            <div class="input-group">
                <label>パスワード(確認)</label><br>
                <input type="password" class="input-field" placeholder="パスワード再入力">
                <p class="note">半角英数字8文字以上20文字以内</p>
            </div>
            
            <button type="submit" class="register-button">登録</button>
            
        </form>
        
        <a href="/login/" class="login-link">
            ログインはこちら
        </a>
        
    </body>
    </html>
    """
    return HttpResponse(html)
