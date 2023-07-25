from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import MessageSerializer
from .models import Message
import logging

# Create your views here.

logger = logging.getLogger(__name__)


#Login/SignIn
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



# register/signup
@api_view(['POST'])
def signUp(request):
    user=User.objects.create_user(
        username= request.data["username"],
        email=request.data["email"],
        password=request.data["password"]
    )
    token = RefreshToken.for_user(user)
    return Response({
        'access': str(token.access_token),
        'refresh': str(token),
        'username': user.username,
        'email': user.email
    })


#get received messages
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReceivedMessages(request):
    print(request)
    receiver = request.user.id
    print(receiver)
    messages = Message.objects.filter(Q(receiver=receiver))
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


#get sent mesages
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSentMessages(request):
    
    user = request.user
    messages = Message.objects.filter(Q(sender=user))
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

# adding a messgae
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addMessage(request):
    try:
        sender = request.user
        receiver_username = request.data["receiver"]
        subject = request.data["subject"]
        content = request.data["content"]

        # Check if the receiver exists in the database
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({"error": "Receiver does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the message
        Message.objects.create(sender=sender, receiver=receiver, subject=subject, content=content, unread=True)
        return Response("Message added.")
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# deleting a message
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteMessage(request,id):
    user = request.user
    print(user)
    try:
        logger.debug(f"Delete message request received for message ID: {id}")
        # message = Message.objects.get(id=id, receiver=user)
        message = Message.objects.filter(Q(id=id), Q(sender=user) | Q(receiver=user)).first()
        logger.debug(f"Message found: {message}")
        message.delete()
        # serializer = MessageSerializer(message)
        return Response("message deleted")
    except Message.DoesNotExist:
        logger.debug("Message not found.")

        return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Error deleting message.")

        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#getting a single, yet unread message, and reversing it to "read"
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def readAMessage(request,id):
    receiver = request.user
    try:
        message = Message.objects.filter(Q(receiver=receiver)).get(id=id)
        message.unread=False
        message.save()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)
    except:
        return Response("check that recipient matches message-id and vice-versa or message-id no longer exists")

#reversing unread message  to "read"

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unReadAMessage(request,id):
    receiver = request.user
    try:
        message = Message.objects.filter(Q(receiver=receiver)).get(id=id)
        message.unread=True
        message.save()
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)
    except:
        return Response("check that recipient matches message-id and vice-versa or message-id no longer exists")



#getting unread messages
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUnreadMessages(request):
    receiver = request.user
    try:
        messages = Message.objects.filter(Q(receiver=receiver)).filter(unread=True)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except:
        return Response("something went wrong")

#getting read messages
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReadMessages(request):
    receiver = request.user
    try:
        messages = Message.objects.filter(Q(receiver=receiver)).filter(unread=False)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except:
        return Response("something went wrong")