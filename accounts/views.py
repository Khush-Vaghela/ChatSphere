from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.

def serve_js(request):

    field = request.GET.get('field', 'Unknown')
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Alert</title>
    </head>
    <body>
        <script type="text/javascript">
            alert("{field} already exists");
            window.location.href = "signup";
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content, content_type='text/html')

def signup(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:

            if User.objects.filter(username = username).exists():
                return redirect(f"{reverse('serve_js')}?field=Username")

            elif User.objects.filter(email = email).exists():
                return redirect(f"{reverse('serve_js')}?field=Email")

            else:
                user = User.objects.create_user(first_name = first_name, last_name = last_name, email = email, username = username, password = password)
                user.save()

        else:
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Alert</title>
            </head>
            <body>
                <script type="text/javascript">
                    alert("Password not matching");
                    window.location.href = "signup";
                </script>
            </body>
            </html>
            """
            return HttpResponse(html_content, content_type='text/html')

        return redirect("/")

    else:

        return render(request, 'signup.html')

def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")

        else:
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Alert</title>
            </head>
            <body>
                <script type="text/javascript">
                    alert("Invalid Credentials!");
                    window.location.href = "login";
                </script>
            </body>
            </html>
            """
            return HttpResponse(html_content, content_type='text/html')

    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect("/")