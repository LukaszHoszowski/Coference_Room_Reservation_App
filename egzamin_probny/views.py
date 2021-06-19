from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views import View

class Start(View):
    def get(self, request):
        response = HttpResponse("""
        <a href="/lecture_details/1/">Pierwszy wyklad</a><br>
        <a href="/set_username/lukasz/">Zapisz mnie</a><br>
        <a href="/say_hello">Przywitaj mnie</a><br>
        <a href="/say_hello/5/">Przywitaj mnie 5 razy</a><br>
        <a href="/create_cookie/cookie/cookie/10//">Upiecz ciastko</a><br>
        <a href="/delete_cookie_cookie/">Zjedz ciastko</a><br>
        <a href="/add_student/">Dodaj studenta</a>       
        """)

        return response

class Lecture(View):
    def get(self, request, id):
        id = request.GET.get('id')
        details = Lecture.objects.get(pk=id)
        response = HttpResponse(f"""
        <table><tr><th>Name:</th><th>Lecturer:</th><th>Students list:</th></tr>
        <tr><td>{details.name}</td><td>{details.lecturer}</td><td>
        
        {details.students__set.all().name}
        
        
        </td>
        """)

        return response