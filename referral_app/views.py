from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])  # Override default permission classes
def user_registration(request):
    data=request.data
    serializer=UserSerializer(data=data)
    if serializer.is_valid():
        user=serializer.save()
        token,_=Token.objects.get_or_create(user=user)
        referral_code_=request.data.get('referral_code')
        if referral_code_:
            try:
                referring_user = User.objects.filter(referral_code=referral_code_).first()
            except User.DoesNotExist:
                referring_user = None
            if referring_user:
                referring_user.points+=1
                referring_user.save()
        return Response({'user_id': user.id, 'message': 'User registered successfully','token':str(token)})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def referrals(request):
    user = request.user
    paginator = PageNumberPagination()
    paginator.page_size = 20  # Set the number of items per page
    referrals = User.objects.filter(referral_code=user.referral_code)
    # Paginate the referrals
    paginated_referrals = paginator.paginate_queryset(referrals, request)

    # Serialize the paginated referrals
    serializer = UserSerializer(paginated_referrals, many=True)

    # Return the paginated referrals with pagination metadata
    return Response(serializer.data)