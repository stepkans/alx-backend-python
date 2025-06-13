from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        return redirect("home")  # or wherever you want to go after deletion

    return render(request, "messaging/confirm_delete.html")

def threaded_conversations(viewed_message_id):
    """
    Retrieve a message and its threaded conversations efficiently.
    """
    message = (
        Message.objects
        .select_related('sender', 'receiver')
        .prefetch_related('replies__sender', 'replies__receiver')
        .get(id=viewed_message_id)
    )

    return message

def get_thread_replies(message):
    """
    Recursively retrieve all replies to a message in a threaded structure.
    """
    thread = []
    for reply in message.replies.all().select_related('sender', 'receiver').prefetch_related('replies__sender', 'replies__receiver'):
        thread.append({ 
            'message': reply,
            'replies': get_thread_replies(reply)
        })
    return thread