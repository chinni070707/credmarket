from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q
from .models import Conversation, Message
from listings.models import Listing


@login_required
def inbox(request):
    """Display all user's conversations"""
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).select_related('listing', 'buyer', 'seller')
    
    context = {'conversations': conversations}
    return render(request, 'messaging/inbox.html', context)


@login_required
def conversation_detail(request, pk):
    """Display conversation detail and handle new messages"""
    conversation = get_object_or_404(
        Conversation,
        pk=pk
    )
    
    # Verify user is part of this conversation
    if request.user not in [conversation.buyer, conversation.seller]:
        django_messages.error(request, 'You do not have access to this conversation.')
        return redirect('messaging:inbox')
    
    # Mark all received messages as read
    Message.objects.filter(
        conversation=conversation,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)
    
    # Handle new message
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            other_user = conversation.get_other_user(request.user)
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                receiver=other_user,
                content=content
            )
            # Don't show a success message for sending messages
            # Just stay on the same page without redirect to avoid popup
    
    messages = conversation.messages.all()
    
    context = {
        'conversation': conversation,
        'messages': messages,
    }
    return render(request, 'messaging/conversation_detail.html', context)


@login_required
def start_conversation(request, listing_slug):
    """Start a new conversation about a listing"""
    listing = get_object_or_404(Listing, slug=listing_slug)
    
    # Prevent seller from messaging themselves
    if listing.seller == request.user:
        django_messages.error(request, 'You cannot message yourself.')
        return redirect('listings:listing_detail', slug=listing_slug)
    
    # Check if conversation already exists
    conversation, created = Conversation.objects.get_or_create(
        listing=listing,
        buyer=request.user,
        seller=listing.seller
    )
    
    # If sending initial message
    if request.method == 'POST' and created:
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                receiver=listing.seller,
                content=content
            )
    
    return redirect('messaging:conversation_detail', pk=conversation.pk)
