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
    </body>
    </html>
    """
    return HttpResponse(html)
