
#Generic Imports
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

#Local imports
from django.views import View
from RFID.forms import *
from RFID.models import *


#------------------- home page ---------------------------------

class HomePageView(LoginRequiredMixin, View):
    """ if not authinticated direct them
    to the login page """

    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/home.html'


    def get(self, request):

        return render(request, self.template_name)



#------------------- Users --------------------------------

class UserPageView(LoginRequiredMixin, View):
    """ Has the two forms: add and get user
    - Handling adding new users here
    """

    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/user.html'

    def post(self, request):
        add_user_form = AddUser(request.POST)
        message = "The user was not added!"

        # Validate if the information passed in post is valid
        if add_user_form.is_valid():
            add_user_form.save()
            message = "The user was successfuly added!"

        error = add_user_form.errors
        form = AddUser()
        get_id_form = GetUser()
        context = {'add_user_form':form, 'get_id_form':get_id_form, 'message':message, 'error': error}

        return render(request, self.template_name, context)

    def get(self, request):
        get_id_form = GetUser()
        form = AddUser()
        context = {'add_user_form':form, 'get_id_form':get_id_form}
        return render(request, self.template_name, context)


class GetUserPageView(LoginRequiredMixin, View):
    """ Gets the user ID or Email and directs
    them to the update page where the user is
    deleted or updated """

    login_url = '/RFID/login/'
    redirect_field_name = ''
    update_template = 'RFID/update_user.html'


    def get_user(self, user_form):
        try:
            if user_form['user_id'].value():
                id = user_form['user_id'].value()
                return get_object_or_404(User, user_id=id)
            else:
                user_email = user_form['email'].value()
                return get_object_or_404(User, email=user_email)
        except:
            redirect('user')

    def post(self, request):
        get_id_form = GetUser(request.POST)
        obj = self.get_user(get_id_form)
        if obj is None:
            message = "The user does not exist!"
        else:
            message = ""

        update_form = AddUser(instance=obj)
        context = {'update_form':update_form, 'message':message}
        return render(request, self.update_template, context)



class UpdateUserPageView(LoginRequiredMixin, View):
    """ Updates user info or deletes them"""

    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/user.html'

    def post(self, request):
        if 'Update' in request.POST:
            form = AddUser(request.POST)
            id = form['user_id'].value()
            User.objects.filter(user_id=id).update(
            first_name = form['first_name'].value(),
            last_name = form['last_name'].value(),
            email = form['email'].value(),
            phone = form['phone'].value(),
            )
            message = 'User information was successfuly updated'

        elif 'Delete' in request.POST:
            form = AddUser(request.POST)
            id = form['user_id'].value()
            user = get_object_or_404(User, user_id=id)
            user.delete()

            message = 'User information successfully deleted'

        get_id_form = GetUser()
        form = AddUser()
        context = {'add_user_form':form, 'get_id_form':get_id_form, 'message':message}
        return render(request, self.template_name, context)



#---------------------- Objects -------------------------------

class ObjectPageView(LoginRequiredMixin, View):
    """ Main page for objects. Has two forms:
    - Add object
    - Edit object
    """

    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/object.html'

    def post(self, request):
        add_object_form = AddObject(request.POST)
        message = 'Object was not added!'

        if add_object_form.is_valid():
            add_object_form.save()
            message = 'Object was successfuly added!'

        error = add_object_form.errors
        object_form = AddObject()
        get_object_form = GetObject()
        context = {'add_object_form':object_form, 'get_object_form':get_object_form, 'message':message, 'error':error}
        return render(request, self.template_name, context)

    def get(self, request):
        object_form = AddObject()
        get_object_form = GetObject()
        context = {'add_object_form':object_form, 'get_object_form':get_object_form}
        return render(request, self.template_name, context)




class GetObjectPageView(LoginRequiredMixin, View):
    """ Gets the object ID or name and redirects to
    update page, where user can delete or update on object
    or a set of objects
    """

    login_url = '/RFID/login/'
    redirect_field_name = ''
    single_object_template = 'RFID/update_single_object.html'
    group_object_template = 'RFID/update_group_object.html'

    def get_object(self, form):
        """Return a queryset based on the
        user input"""

        if form['object_id'].value():
            id = form['object_id'].value()
            try:
                obj = Object.objects.get(object_id=id)
            except ObjectDoesNotExist:
                obj = None
            check = False
            count = 1
            return (obj, count, check)

        else:
            name = form['name'].value()
            querySet = Object.objects.filter(name__iexact=name)
            count = len(querySet)
            obj = Object.objects.filter(name__iexact=name).first()
            check = True
            return (obj, count, check)

    def post(self, request):
        get_object_form = GetObject(request.POST)
        querySet, count, check = self.get_object(get_object_form)
        if querySet is None:
            message = "The object does not exist!"
        else:
            message = ""

        # If this is just one object
        if check is False:
            form = AddObject(instance=querySet)
            context = {'form': form, 'message': message}
            return render(request, self.single_object_template, context)

        else:
            form = GetGroupObject(instance=querySet)
            context = {'form':form, 'count':count, 'message':message}
            return render(request, self.group_object_template, context)




class UpdateSingleObjectView(LoginRequiredMixin, View):
    """ Gets the object ID, updates the specific objects
    information or deletes it. Redirects the user to the
    main objects page.
    """

    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/object.html'


    def post(self, request):
        if 'Update' in request.POST:
            form = AddObject(request.POST)
            id = form['object_id'].value()
            Object.objects.filter(object_id=id).update(
            object_id = form['object_id'].value(),
            name = form['name'].value(),
            availability= form['availability'].value(),
            max_time = form['max_time'].value(),
            location = form['location'].value(),
            )
            message = 'Object information was successfuly updated'

        elif 'Delete' in request.POST:
            form = AddObject(request.POST)
            id = form['object_id'].value()
            obj = get_object_or_404(Object, object_id=id)
            obj.delete()

            message = 'Object was successfully deleted'

        get_id_form = GetObject()
        form = AddObject()
        context = {'add_object_form':form, 'get_object_form':get_id_form, 'message':message}
        return render(request, self.template_name, context)



class UpdateGroupObjectView(LoginRequiredMixin, View):
    """ Gets the object name, updates the group of objects
    information or deletes them. Redirects the user to the
    main objects page.
    """

    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/object.html'

    def post(self, request):
        form = GetGroupObject(request.POST)
        name = form['name'].value()

        if 'Update' in request.POST:
            Object.objects.filter(name=name).update(
            name = form['name'].value(),
            availability = form['availability'].value(),
            max_time = form['max_time'].value(),
            )
            message = 'Information for the group of objects was successfuly updated'

        elif 'Delete' in request.POST:
            Object.objects.filter(name=name).delete()
            message = 'Group of objects were successfully deleted'

        get_id_form = GetObject()
        form = AddObject()
        context = {'add_object_form':form, 'get_object_form':get_id_form, 'message':message}
        return render(request, self.template_name, context)
