from django.shortcuts import render

def portfolio_top(request): #ポートフォリオトップ画面
    return render(request, 'portfolio_top.html')