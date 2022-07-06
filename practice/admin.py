# Register your models here.
from django.contrib import admin

from .models import User,Problem,Submission,Testcase

admin.site.register(User)
admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(Testcase)

