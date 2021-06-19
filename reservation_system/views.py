from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from reservation_system.models import Rooms, Booking

from datetime import date, datetime


# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class AddRoom(View):
    def get(self, request):
        response = HttpResponse("""
            <form action="" method="POST">
                <label>
                    Room name: <input type="text" name="name"/>
                </label><br>
                <label>
                    Room capacity: <input type="number" name="capacity"/>
                </label><br>
                <label>
                    Project present?: <input type="checkbox" value=1 name="projector"/>
                </label> <br>
                <br>
                <input type="submit" value="Save the Room">
            </form>
        """)
        return response

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')

        if not projector:
            projector = False
        else:
            projector = True

        warn = ""

        if not name:
            warn += ("You need to enter Room's name!<br>")
        if Rooms.objects.filter(name=name.title()).exists():
            warn += ("Such Room already exist! Change name of the room!<br>")
        if int(capacity) <= 0:
            warn += ("We won't kill anyone to fulfill your sick requirments, room can't be empty!<br>")

        if warn == "":
            Rooms.objects.create(name=name.title(), capacity=capacity, projector=projector)
            warn += "<br>Your Room has been saved to DB!"
        return redirect('/rooms')

class AddRoom2(View):
    def get(self, request):
        return render(request, "add_room.html")

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get('projector') == 0

        if not name:
            return render(request, "add_room.html", context={"error": "Room name hasn't been entered"})
        if capacity <= 0:
            return render(request, "add_room.html", context={"error": "Capacity needs to be positive"})
        if Rooms.objects.filter(name=name.title()).first():
            return render(request, "add_room.html", context={"error": "Such room already exist"})

        Rooms.objects.create(name=name.title(), capacity=capacity, projector=projector)
        return redirect('room-list')

@method_decorator(csrf_exempt, name='dispatch')
class AllRooms(View):
    def get(self, request):
        rooms = Rooms.objects.all()
        all_rooms = HttpResponse("""
        <table><tr>
        <th>Room</th><th>Capacity</th><th>Available</th><th>Projector</th><th></th><th></th><th></th></tr>
        """)
        for room in rooms:
            all_rooms.write(
                f"""<tr><td><a href="/room/{room.id}">{room.name}</a></td>
                <td>{room.capacity}</td>
                <td>{"No" if room.booking_set.filter(date=date.today()) else "Yes"}</td>
                <td>{"Yes" if room.projector else "No"}</td>
                <td><a href="/room/modify/{room.id}"><button type="submit" name="edit" value="{room.id}">Edit</button></a></td>
                <td><a href="/room/delete/{room.id}"><button type="submit" name="delete" value="{room.id}">Delete</button></a></td>
                <td><a href="/room/reserve/{room.id}"><button type="submit" name="book" value="{room.id}">Book</button></a></td></tr>
                """)
        all_rooms.write('</table>')

        if rooms.count() == 0:
            return HttpResponse("Lack of available rooms!")

        return all_rooms


class AllRooms2(View):
    def get(self, request):
        rooms = Rooms.objects.all()
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.booking_set.all()]
            room.reserved = date.today() in reservation_dates
        return render(request, "rooms.html", context={"rooms": rooms})

@method_decorator(csrf_exempt, name='dispatch')
class EditRoom(View):
    def get(self, request, id):
        # id = request.GET.get('edit')
        room = Rooms.objects.get(id=id)
        response = HttpResponse(f"""
                    <form action="" method="POST">
                        <label>
                            Room name: <input type="text" name="name" value="{room.name}"/>
                        </label><br>
                        <label>
                            Room capacity: <input type="number" name="capacity" value="{room.capacity}"/>
                        </label><br>
                        <label>
                            Project present?: <input type="checkbox" value={room.projector} name="projector" 
                            {'checked' if room.projector == 1 else ''}/>
                        </label> <br>
                        <br>
                        <input type="submit" value="Save the Room">
                    </form>
                """)

        print(room.projector)
        return response

    def post(self, request, id):

        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector')

        room = Rooms.objects.get(pk=id)

        if not projector:
            projector = False
        else:
            projector = True

        warn = ""

        if not name:
            warn += ("You need to enter Room's name!<br>")
        if Rooms.objects.filter(name=name.title()).exists() and room.name != name:
            warn += ("Such Room already exist! Change name of the room!<br>")
        if int(capacity) <= 0:
            warn += ("We won't kill anyone to fulfill your sick requirments you bastard, room can't be empty!<br>")

        if warn == "":
            room.name = name.title()
            room.capacity = capacity
            room.projector = projector
            room.save()
            return redirect('/rooms')
        return HttpResponse(warn)

class EditRoom2(View):
    def get(self, request, id):
        room = Rooms.objects.get(id=id)
        return render(request, "modify_room.html", context={"room": room})

    def post(self, request, id):
        room = Rooms.objects.get(id=id)
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"

        if not name:
            return render(request, "modify_room.html", context={"room": room, "error": "Room name hasn't been entered"})
        if capacity <= 0:
            return render(request, "modify_room.html", context={"room": room, "error": "Capacity needs to be positive"})
        if name != room.name and Rooms.objects.filter(name=name.title()).first():
            return render(request, "modify_room.html", context={"room": room, "error": "Such room already exist"})

        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()

        return redirect("room-list")



@method_decorator(csrf_exempt, name='dispatch')
class DelRoom(View):
    def get(self, request, id):
        room = Rooms.objects.get(pk=id)
        room.delete()
        return redirect('/rooms')

class DelRoom2(View):
    def get(self, request, id):
        room = Rooms.objects.get(pk=id)
        room.delete()
        return redirect('room-list')


@method_decorator(csrf_exempt, name='dispatch')
class BookRoom(View):
    today = date.today()

    def get(self, request, id):
        room = Rooms.objects.get(pk=id)
        response = f"""
        <form action="" method="POST">
                        <label>
                            Reservation date: <input type="date" name="book_date" value="{self.today}" min = "{self.today}"/>
                        </label><br>
                        <label>
                            Comment field: <input type="text" name="comment"/>
                        </label><br>
                        <br>
                        <table><td>"""
        for booked in room.booking_set.all().order_by('date'):
            response += f'<tr><td>{booked.date}</td><td>{booked.comment}</tr>'
        response += '</td></table></tr><br><br><input type="submit" value="Book the Room"></form>'
        return HttpResponse(response)

    def post(self, request, id):
        date = request.POST.get('book_date')
        comment = request.POST.get('comment')

        fdate = datetime.strptime(date, "%Y-%m-%d").date()
        conf_room = Rooms.objects.get(id=id)

        books = []

        bookings = Booking.objects.filter(room=id)
        for book in bookings:
            books.append(datetime.strftime(book.date, "%Y-%m-%d"))

        if date in books:
            return HttpResponse(f'Already booked at {date}, choose different date!')
        elif fdate < self.today:
            return HttpResponse(f"Can't book the Room in the past, today is {self.today}")
        else:
            Booking.objects.create(date=date, comment=comment, room=conf_room)
            return redirect('/rooms')


class BookRoom2(View):
    today = str(date.today())

    def get(self, request, id):
        room = Rooms.objects.get(pk=id)
        reservations = room.booking_set.filter(date__gte=str(self.today)).order_by('date')
        return render(request, "reservation.html", context={"room": room,
                                                            "reservations": reservations})

    def post(self, request, id):
        date = request.POST.get('date')
        comment = request.POST.get('comment')
        room = Rooms.objects.get(id=id)

        reservations = room.booking_set.filter(date__gte=str(datetime.date.today())).order_by('date')

        if Booking.objects.filter(room=room, date=date):
            return render(request, "reservation.html", context={"room": room,
                                                                "reservations": reservations,
                                                                "error": "Room already booked!"})
        if date < str(self.today):
            return render(request, "reservation.html", context={"room": room,
                                                                "reservations": reservations,
                                                                "error": "Only current/future dates are allowed!"})

        Booking.objects.create(room=room, date=date, comment=comment)
        return redirect("room-list")


class RoomDtl(View):
    def get(self, request, id):
        room = Rooms.objects.get(pk=id)

        room_dtl = HttpResponse(f"""
                <table><tr><th>Room</th><th>Capacity</th><th>Available</th><th>Projector</th><th>Booked</th></tr>
                <tr><td>{room.name}</td><td>{room.capacity}</td><td>{"No" if room.booking_set.filter(date=date.today()) else "Yes"}</td><td>{room.projector}</td><td>
                <table>
                """)
        for booked in room.booking_set.all().order_by('date'):
            if booked.date >= date.today():
                room_dtl.write(f'<tr><td>{booked.date}</td><td>{booked.comment}</tr>')

        room_dtl.write('</td></table></tr></table><br><br>')
        room_dtl.write(f"""<a href="/room/modify/{id}">Edit Room</a>
                            <a href="/room/delete/{id}">Delete Room</a>
                            <a href="/room/reserve/{id}">Book Room</a><br><br>
                            <a href="/rooms">All Rooms</a><br><br>
        """)
        return room_dtl

class RoomDtl2(View):
    def get(self, request, id):
        room = Rooms.objects.get(pk=id)
        reservations = room.booking_set.filter(date__gte=str(date.today())).order_by('date')
        return render(request, "room_details.html", context={"room": room, "reservations": reservations})

class Main(View):
    def get(self, request):
        response = HttpResponse("""
                    <form action="/search/" method="GET">
                        <label>
                            Room name: <input type="text" name="name"/>
                        </label><br>
                        <label>
                            Min room capacity: <input type="number" name="min_capacity"/>
                        </label><br>
                        <label>
                            Project present?: <input type="checkbox" value=1 name="projector"/>
                        </label> <br>
                        <br>
                        <input type="submit" value="Find the Room">
                    </form>
                """)
        return response

class Search(View):
    today = date.today()
    def get(self, request):
        name = request.GET.get('name')
        min_capacity = request.GET.get('min_capacity')
        min_capacity = 0 if not min_capacity else min_capacity
        projector = True if request.GET.get('projector') else False

        q_rooms = Rooms.objects.filter(name__icontains=name, capacity__gt=min_capacity, projector=projector).exclude(booking__date=self.today)

        if q_rooms:
            response = HttpResponse("""<table><tr><th>Room Name:</th><th>Capacity:</th><th>Projector:</th></tr>""")
            for q in q_rooms:
                response.write(f'<tr><td>{q.name}</td><td>{q.capacity}</td><td>{q.projector}</td></tr>')
            response.write('</table>')
        else:
            response = HttpResponse('No rooms available for the search!')

        response.write(f'<br><br><a href="/">Go back to SEARCH</a>')
        return HttpResponse(response)

class Search2(View):
    def get(self, request):
        name = request.GET.get("name")
        capacity = request.GET.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.GET.get("projector") == "on"

        rooms = Rooms.objects.all()
        if projector:
            rooms = rooms.filter(projector=projector)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms = rooms.filter(name__icontains=name)

        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.booking_set.all()]
            room.reserved = str(date.today()) in reservation_dates
        return render(request, "rooms.html", context={"rooms": rooms, "date": date.today()})