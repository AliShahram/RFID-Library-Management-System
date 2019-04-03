OBJ_LOCATION_CHOICES = (
    ('', ("--  Location")),
    ('H', ("Hopper")),
    ('T', ("Turing")),

)

OBJ_AVAILABILITY_CHOICES = (
    ('', ("-- Availability")),
    ('Y', ("Available")),
    ('N', ("Unavailable")),

)


RECORD_TYPE_CHOICES = (
    ('', ("-- Type")),
    (1, ("Check Out")),
    (0, ("Check In")),
)


RECORD_STATUS_CHOICES = (
    ('', ("-- Status")),
    ('True', ("Active")),
    ('False', ("Completed")),
)
