#Django Imports
from django.core.exceptions import ObjectDoesNotExist

#Local imports
from django.apps import apps
Object = apps.get_model('RFID', 'Object')
User = apps.get_model('RFID', 'User')
Records = apps.get_model('RFID', 'Records')


class CheckOperation:
    def __init__(self, form):
        self.form = form

    #Print the form
    def printForm(self):
        print(self.form)


    def distinguish_ids(self):
        """ Distinguish between user and object IDs
        and append object id to a list"""

        objs = []
        data = self.form.cleaned_data
        usr = data['user']
        for title in data:
            if title != 'user' and title != 'type' and data[title] != "":
                objs.append(data[title])
        return usr, objs


    def check_user_status(self, usr_id):
        """Check if the user is allowed to check out items.
           Measures:
                - check if the user is in the system
                - check if the user doesn't have five or more previous checkouts that
                    hasn't been returned
            returns:
                user_inst = results user object instance, if doesn't exist return None
                allowed = True for allowed, False for not allowed
                numItems = number of items the user can check out
        """

        try:
            user_inst = User.objects.get(user_id=usr_id)
        except ObjectDoesNotExist:
            user_inst = None

        if user_inst:
            history = Records.objects.filter(user_id=usr_id, status=1, active=True)
            if len(history) >= 5:
                allowed = False
                numItems = 0
            else:
                allowed = True
                numItems = 5 - len(history)

        else:
            allowed = False
            numItems = 0
        return user_inst, allowed, numItems


    def check_objs_status(self, obj_ids, numItems):
        """check if the objects are allowed to be checked out
           Measures:
                - check if object is in the system
                - check object table to see if object is available
                - checks how many items the user can checkout and based
                  on that makes objects available for checkout
           Returns:
                - list of of object instances that are available to be checkout
                - list of object instances that are not available for checkout
        """
        count_items = 1
        avail_checkout = []
        not_avail_checkout = []

        for id in obj_ids:
            try:
                obj = Object.objects.get(object_id=id)
            except ObjectDoesNotExist:
                obj = None

            if count_items <= numItems:
                if obj:
                    if obj.availability == 'Y':
                        avail_checkout.append(obj)
                        count_items += 1
                    else:
                        not_avail_checkout.append(obj)
            else:
                not_avail_checkout.append(obj)
        return avail_checkout, not_avail_checkout


    def checkout_objs(self, usr_inst, avail_checkout):
        """ Performs the checkout operation"""

        for obj_inst in avail_checkout:
            Records.objects.create(
                user_id = usr_inst,
                object_id = obj_inst,
                status = 1,
                active = True
            )

            obj_inst.availability = 'N'
            obj_inst.save()


def perform_checkout(form):
    op = CheckOperation(form)
    usr_id, obj_ids = op.distinguish_ids()
    user_inst, allowed, numItems = op.check_user_status(usr_id)
    avail_checkout, not_avail_checkout = op.check_objs_status(obj_ids, numItems)

    if user_inst:       #if user exists
        if allowed == True:     #if user is allowed to checkout
            if len(avail_checkout)>0:       #If there is objects available to checkout
                op.checkout_objs(user_inst, avail_checkout)         #Perform the checkout
                success = True
                message = "Checkout was sucessful!"
            else:
                success = False
                message = "Checkout was not successful! Scanned items are not available for checkout"
        else:
            success = False
            message = "Checkout was not successful! The user has already checkout out maximum number of items"
    else:
        success = False
        message = "Checkout was not successful! The user is not registered in the system"

    context = {
        "sucess":success,
        "message":message,
        "user_inst":user_inst,
        "avail_checkout":avail_checkout,
        "not_avail_checkout":not_avail_checkout
    }
    return context
