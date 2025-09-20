from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Petition
from .forms import PetitionForm

@login_required
def petition_view(request):
    """
    Handles displaying the petition form and processing form submissions.
    Only accessible to logged-in users.
    """
    petitions = Petition.objects.all()

    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            # Create petition object but don't save to database yet
            petition = form.save(commit=False)
            # Assign the current logged-in user
            petition.user = request.user
            # Now save the petition to the database
            petition.save()
            return redirect('petition_view')
    else:
        form = PetitionForm()

    context = {
        'form': form,
        'petitions': petitions
    }
    return render(request, 'petition/petition_page.html', context)

@login_required
def like_petition_view(request, petition_id):
    """
    Handles liking or unliking a petition.
    """
    # Get the petition object
    petition = get_object_or_404(Petition, id=petition_id)

    # Prevent a user from liking their own petition
    if petition.user == request.user:
        return redirect('petition_view')

    # Check if the user has already liked the petition
    if request.user in petition.likes.all():
        # If they have, remove the like (unlike)
        petition.likes.remove(request.user)
    else:
        # If they haven't, add the like
        petition.likes.add(request.user)

    return redirect('petition_view')

