from django.shortcuts import render


def error403(request,exception):
    return render(request,'error/error-403.html')

def error404(request,exception):
    return render('error/error-404.html')

def error500(request):
    return render(request,'error/error-500.html')