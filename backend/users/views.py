import random
import string

import requests
from requests.auth import HTTPBasicAuth

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from django.conf import settings

from sentry_sdk import capture_exception

from django.contrib.auth.models import User

from users.models import Profile


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        code = request.data['code']
        response = requests.post(
            url=settings.STEPIK_TOKEN_URL,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': settings.STEPIK_REDIRECT_URL
            },
            auth=HTTPBasicAuth(settings.STEPIK_CLIENT_ID, settings.STEPIK_CLIENT_SECRET)
        )
        if response.status_code != 200:
            raise Exception('Authorization failed')
        try:
            stepik_access_token = response.json()['access_token']
        except KeyError:
            raise Exception('Stepik Access token is not provided')

        user_response = requests.get(
            url=settings.STEPIK_GET_USER_URL,
            headers={'Authorization': 'Bearer {}'.format(stepik_access_token)}
        ).json()


        try:
            user_props = {
                'stepik_id': user_response['users'][0]['id'],
                'full_name': user_response['users'][0]['full_name'],
                'avatar': user_response['users'][0]['avatar']
            }
        except KeyError as e:
            print(e)
            raise Exception('Getting Stepik User Data Error')

        if Profile.objects.filter(stepik_id=user_props['stepik_id']):
            user = User.objects.get(profile__stepik_id=user_props['stepik_id'])
        else:
            user = User.objects.create(
                username='StepikUser{}'.format(user_props['stepik_id']),
                password=''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            )
            user.profile.stepik_id = user_props['stepik_id']
            user.profile.full_name = user_props['full_name']
            user.profile.avatar = user_props['avatar']
            user.profile.save()

        payload = jwt_payload_handler(user)
        access_token = jwt_encode_handler(payload)
        res = {
            'user': {
                'stepik_id': user.profile.stepik_id,
                'full_name': user.profile.full_name,
                'url': user.profile.url,
                'avatar': user.profile.avatar,
            },
            'access_token': access_token
        }
        return Response(res, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        capture_exception(e)
        res = {'Error': 'Please, provide valid data'}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

