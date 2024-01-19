from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from app.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.template import loader, TemplateDoesNotExist
import pdfkit
from django.urls import reverse
import io

# Create your views here.
@login_required(login_url='/app/login')
def accept(request):
    if request.method == 'POST':
        name = request.POST.get("name",'')
        phone = request.POST.get("phoneno",'')
        email = request.POST.get("email",'')
        school = request.POST.get("school",'')
        degree = request.POST.get("degree",'')
        university = request.POST.get("university",'')
        skills = request.POST.get("skills",'')
        about_you = request.POST.get("about_you",'')
        previous_work = request.POST.get("previous_work",'')  

        profile = Profile(name=name,phoneno=phone,email=email,school=school,degree=degree,university=university,skills=skills,about_you=about_you,previous_work=previous_work)
        profile.save()

        print("Profile ID:", profile.id)

        return redirect(reverse('preview', kwargs={'uid': profile.id}))
    
    return render(request, 'accept.html')
    # return redirect('/app/preview/<uid>')

def preview(request,uid):
    user_profile = Profile.objects.get(id=uid)
    return render(request,'preview.html',{'user_profile':user_profile, 'uid': uid})

def resume1(request, uid):
    user_profile = Profile.objects.get(id=uid)
    template = loader.get_template('preview.html')
    html = template.render({'user_profile':user_profile})
    option = {
        'page-size':'Letter',
        'encoding':'UTF-9'
    }
    try:
        configuration = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        pdf = pdfkit.from_string(html, False, options=option, configuration=configuration)
    except Exception as e:
        # Handle the exception, print it, or log it
        print(f"Error generating PDF: {e}")
        return HttpResponse("Error generating PDF")
    response = HttpResponse(pdf, content_type='application/pdf')
    response['content-Disposition']='attachment; filename="resume1.pdf"'
    return response

def edit(request, uid):
    if request.method=='GET':
        user_profile=Profile.objects.filter(id = uid) # if we want specific data than we use filter
        return render(request, 'editPreview.html',{'user_profile':user_profile})
    else:
        nm=request.POST['name']
        email=request.POST['email']
        mno=request.POST['phoneno']
        school=request.POST['school']
        degree=request.POST['degree']
        university=request.POST['university']
        skills=request.POST['skills']
        about_you=request.POST['about_you']
        previous_work=request.POST['previous_work']
        profile=Profile.objects.filter(id=uid)
        profile.update(name=nm,email=email,phoneno=mno,school=school,degree=degree,university=university,skills=skills,about_you=about_you,previous_work=previous_work)
        return redirect(reverse('preview', kwargs={'uid': uid}))
    
def template1(request,uid):
    profile = Profile.objects.filter(id=uid)
    return render(request,'Template1.html',{'user_profile':profile})

def templates():
    return redirect('/app/choose-template')

def choose_template(request,uid):
    user_profile=Profile.objects.filter(id = uid) # if we want specific data than we use filter
    return render(request, 'choose_template.html',{'user_profile':user_profile})

def download_pdf(request, template_id, uid):
    # If a valid template_id is provided, fetch data from the Profile model
    if template_id and uid:
        profile = get_object_or_404(Profile, id=uid)
        # Retrieve the chosen template file path dynamically
        template_path = f'../templates/template{template_id}.html'

        try:
            # Attempt to load the template
            template = loader.get_template(template_path)
        except TemplateDoesNotExist:
            # Handle the case where the template doesn't exist
            return HttpResponse(f"Template '{template_path}' does not exist")
        
        rendered_template = template.render({'profile': profile})

        # Render the template with dynamic data from the Profile model
        # rendered_template = render(request, template_path, context={'profile': profile})

        configuration = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

        # Use pdfkit to generate PDF from HTML content
        pdf_content = pdfkit.from_string(str(rendered_template), False, configuration=configuration)

        # Set response headers for PDF download
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="resume.pdf"'

        return response
    else:
        # Handle the case where template_id is not provided or is invalid
        # You can customize this part based on your requirements
        return HttpResponse("Invalid template_id")
    
def home(request):
    return render(request,'homePage.html')

def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        uname=request.POST['uname']
        password=request.POST['password']
        print(fname,lname,email,password,sep='\n')
        # Why we create object? -->
        obj=User.objects.create(username=uname,email=email,first_name=fname,last_name=lname) # to create object 
        # We can create the object with the help of create() or filter()
        obj.set_password(password)
        obj.save() # to store the object
        #return HttpResponse('Fetch Data')  
        return redirect('/app/login')

def user_login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        unm=request.POST['uname']
        upass=request.POST['pass']
        a=authenticate(username=unm, password=upass)
        print(a)
        print("Authentication result: ",a)

        if a is None:
            # return HttpResponse("Login Fail")
            return redirect('/app/login')
        else:
            # return HttpResponse("Login Succes")
            # return HttpResponse("At login authentication")
             login(request,a)
             print(a.id,a.username,a.password,sep='\n')
             return redirect('/app/home')
        
def user_logout(request):
    logout(request)
    return redirect('/app/home')
        
