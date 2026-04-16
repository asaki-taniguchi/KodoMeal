from django.http import HttpResponse

def portfolio_top(request):
    return HttpResponse("<h1>KodoMeal<h1>")