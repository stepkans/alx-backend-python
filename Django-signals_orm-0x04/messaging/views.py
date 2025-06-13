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

def threaded_conversations(viewed_message_id):
    """
    Retrieve a parent message with its threaded conversations efficiently.
    """
    parent = Message.objects.select_related('sender', 'receiver').get(id=viewed_message_id)
    threaded = Message.objects.filter(parent_message=parent).select_related('sender', 'receiver')
    return renderedThreadedConversation(parent, threaded)


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


@login_required
def create_message(request):
    if request.method == "POST":
        receiver = User.objects.get(id=request.POST['receiver_id'])  # or however you select the receiver
        content = request.POST['content']

        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
        )

        return redirect("threaded_conversations", message.id)

    return render(request, "messaging/create_message.html")

def messages_for_user(request):
    """View messages for the currently authenticated user."""
    messages = Message.objects.filter(
        models.Q(sender=request.user) | models.Q(receiver=request.user)
    ).select_related('sender', 'receiver').prefetch_related('replies')
    return render(request, "messaging/user_messages.html", {"messages": messages})


def unread_messages_view(request):
    """View for retrieving unread messages for the current user."""
    unread = Message.unread.for_user(request.user)
    return render(request, "messaging/unread_messages.html", {"messages": unread})