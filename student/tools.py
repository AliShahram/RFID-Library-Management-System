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


    def get_user_instance(self, usr_id):
        """ gets a user ID and returns an instance of the user
            returns None if the user doesn't exist"""
        try:
            user_inst = User.objects.get(user_id=usr_id)
        except ObjectDoesNotExist:
            user_inst = None
        return user_inst


    def get_object_instance(self, obj_id):
        """ gets an object ID and return an instance of the object
            return None if the user does'nt exist"""
        try:
            obj_inst = Object.objects.get(object_id=obj_id)
        except:
            obj_inst = None
        return obj_inst


    def change_obj_availability(self, obj_inst):
        """ if object is unavailable make it available, and vice versa"""

        if obj_inst.availability == 'N':
            obj_inst.availability = 'Y'
        else:
            obj_inst.availability = 'N'
        obj_inst.save()


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

        user_inst = self.get_user_instance(usr_id)

        if user_inst:
            history = Records.objects.filter(user_id=usr_id, type=1, status=True)
            if len(history) >= 5:
                allowed = False
                numItems = 0
            else:
                allowed = True
                numItems = 5 - len(history)

        else:
            allowed = False
            numItems = 0
        print("user authenticat completed")
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
                type = 1,
                status = True
            )

            self.change_obj_availability(obj_inst)




    def get_user_active_records(self, usr_id, obj_ids):
        """takes all instances of the user in the records table"""

        avail_checkin_records = []
        not_avail_checkin_inst = []
        avail_checkin_inst = []

        user_inst = self.get_user_instance(usr_id)
        for obj in obj_ids:
            obj_inst = self.get_object_instance(obj)
            print(obj_inst)
            try:
                record_list = Records.objects.get(
                    user_id=user_inst,
                    object_id=obj,
                    status=True,
                    )
                avail_checkin_records.append(record_list)
                avail_checkin_inst.append(obj_inst)
            except ObjectDoesNotExist:
                not_avail_checkin_inst.append(obj_inst)
        return user_inst, avail_checkin_records, avail_checkin_inst, not_avail_checkin_inst



    def checkin_objs(self, user_inst, avail_checkin_records, avail_checkin_inst):
        """ Check in operation:
            - create new record in records table
            - update records table
            - change object availability """

        for record in avail_checkin_records:
            record.status = 0
            record.save()

        for obj_inst in avail_checkin_inst:
            Records.objects.create(
                user_id = user_inst,
                object_id = obj_inst,
                type = 0,
                status = False,
            )
            self.change_obj_availability(obj_inst)



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
        "success":success,
        "message":message,
        "user_inst":user_inst,
        "check_items_success":avail_checkout,
        "check_items_fail":not_avail_checkout
    }
    return context




def perform_checkin(form):
    op = CheckOperation(form)
    usr_id, obj_ids = op.distinguish_ids()
    user_inst, avail_checkin_records, avail_checkin_inst, not_avail_checkin = op.get_user_active_records(usr_id, obj_ids)

    if user_inst:       #If user exists
        op.checkin_objs(user_inst, avail_checkin_records, avail_checkin_inst)
        success = True
        message = "Checkin was sucessful!"
    else:
        success = False
        message = "Checkin was not successful! The user is not registered "


    context = {
        "success":success,
        "message":message,
        "user_inst":user_inst,
        "check_items_success":avail_checkin_inst,
        "check_items_fail":not_avail_checkin,
    }
    return context
