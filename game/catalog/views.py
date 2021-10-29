from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from json import dumps
from django.contrib.auth import authenticate, login
from jinja2.nodes import Test
from django.http import JsonResponse
from .forms import LoginForm, NewUserForm
from django.contrib import messages
from django.core import serializers
from django.forms.models import model_to_dict
from .models import Note, History, GameUser, GameProgress
from .lib.objects import NoteBuilder
from catalog.service import get_note_and_questions, get_question
from catalog.lib.ui_dict import UI
from django.forms.models import model_to_dict

def index(request):
    notes = Note.objects.filter(progress_id__exact=1)
    history = History.objects.filter(progress_id__exact=1)
    notes_serialized = serializers.serialize('json', notes)
    history_serialized = serializers.serialize('json', history)
    return render(
        request,
        'index.html', context={'notes': notes_serialized,
                               'history': history_serialized})


def piano(request):
    return render(
        request,
        'catalog/piano/piano.html',
    )


def piano2(request):
    return render(
        request,
        'catalog/piano/piano2.html',
        context={'piano': dumps({'password': 'cd'})},
    )


def piano3(request):
    return render(
        request,
        'catalog/piano/piano3.html',
    )


def piano_secret(request):
    return render(
        request,
        'catalog/piano/piano_secret.html',
    )


def clock(request):
    return render(
        request,
        'catalog/clock.html',
    )


def box(request):
    return render(
        request,
        'catalog/box/box.html',
    )


def box_left(request):
    return render(
        request,
        'catalog/box/box_left.html',
    )


def box_right(request):
    return render(
        request,
        'catalog/box/box_right.html',
    )


def table_recipe(request):
    return render(
        request,
        'catalog/recipe/table_recipe.html',
    )


def book_recipe(request):
    return render(
        request,
        'catalog/recipe/book_recipe.html',
    )


def book_recipe2(request):
    return render(
        request,
        'catalog/recipe/book_recipe2.html',
    )


def bed_room(request):
    return render(
        request,
        'catalog/bed_room.html',
    )


def notes(request):
    return render(
        request,
        'catalog/notes/notes.html',
    )


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('/catalog/')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'registration/login.html', {'form': form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/catalog/login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return HttpResponse('Unsuccessful registration. Invalid information.')
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})

 # def get_note():
 #     """Get notes in which not are done and filter by progress of user"""
 #     notes = Note.objects.filter(progress="1").filter(done=False)
 #     return None if len(notes) == 0 else notes[0]

 

def load_note(request):
    note = Note.getNote()
    request.session['note'] = note
    n = note.getQuestion()
    question = n.send(None)
    data = {'note': note, 'question': question}
            #UI[question.ui](obj_question=question, note=qnotes[0])}
    return JsonResponse(data)

def load_question(request):
    note = request.session['note']
    n = note.getQuestion()
    question = n.send("fine")
    if question is None:
        load_note(request)
        n.close()
    


def note_template(request):
    data = {'html': '<li class="mine"><span>I have something for you.</span></li>'}
    data = {'html': Note.objects.filter(progress_id__exact=1)}
    return JsonResponse(data)

def test_data(request):
    # data = {'html' : Note.objects.filter(progress_id__exact=1)}
    # from game.catalog.lib.objects import NoteBuilder
    # n = NoteBuilder().addQuestion().question("NOWWWW?").correct("fine").build().loadLevel("1").setId().build()
    # print(n.__dict__)
    # print('TYPE')
    # print(type(n))
    # n.save()
    data = {'html': serializers.serialize("json", Note.objects.all())}
    return JsonResponse(data)


def form_handle(request):
    if request.method == 'POST' and request.is_ajax():
        form = Form(request.POST)
        response, context = {}, {}
        if form.is_valid():
            record = form.save()
            rendered = render_to_string('form-result.html', {'record': record}) #якщо треба відображати якісь результати (напр. коментарі)
            context = {'response': rendered, 'result': 'success'}
        else:
            for error in form.errors:
                response[k] = form.errors[error][0]
                context = {'response': response, 'result': 'error'}
        return JsonResponse(context)
    else:
        raise Http404
