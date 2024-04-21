from django.shortcuts import render
from tweak.forms import EmployeeForm
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.
def tweak(request):
    if request.method =='POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            form = EmployeeForm()
            messages.success(request,'Record saved successfully!')
            return HttpResponseRedirect("tweak")
        else:
            messages.error(request, 'Failed to save record to the system!')
    else:
        form = EmployeeForm()
    context = {
        'form': form,
    }
    return render(request, template_name='tweak/crispy.html', context = context)
