import json

import jwt
import requests
from cryptography.hazmat.primitives import serialization
from django.conf import settings
from django.utils import timezone
from jwt.algorithms import RSAAlgorithm
from rest_framework.exceptions import ValidationError


class SocialAdapter:
    key = None

    def __init__(self, code=None, access_token=None, origin=None):
        self.code = code
        self.access_token = access_token
        self.origin = origin

    def get_access_token(self):
        raise NotImplementedError("Not Implemented 'get_access_token' method")

    def get_social_user_id(self):
        raise NotImplementedError("Not Implemented 'get_social_user_id' method")


class KakaoAdapter(SocialAdapter):
    key = "kakao"

    def get_access_token(self):
        if not self.access_token:
            return self.access_token

        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_CLIENT_ID,
            "redirect_uri": f"{self.origin}{settings.SOCIAL_REDIRECT_PATH}",
            "code": self.code,
            "client_secret": settings.KAKAO_CLIENT_SECRET,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError("KAKAO GET TOKEN API ERROR")
        data = response.json()

        return data["access_token"]

    def get_social_user_id(self):
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f'Bearer {self.get_access_token()}'}
        response = requests.get(url=url, headers=headers)
        if not response.ok:
            raise ValidationError("KAKAO ME API ERROR")
        data = response.json()

        return data["id"], data["kakao_account"]


class NaverAdapter(SocialAdapter):
    key = "naver"

    def get_access_token(self):
        if self.access_token:
            return self.access_token
        url = "https://nid.naver.com/oauth2.0/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.NAVER_CLIENT_ID,
            "client_secret": settings.NAVER_CLIENT_SECRET,
            "code": self.code,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError("NAVER GET TOKEN API ERROR")
        data = response.json()

        return data["access_token"]

    def get_social_user_id(self):
        url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f'Bearer {self.get_access_token()}'}
        response = requests.post(url=url, headers=headers)
        if not response.ok:
            raise ValidationError("NAVER ME API ERROR")
        data = response.json()

        return data["response"]["id"], data["response"]


class FacebookAdapter(SocialAdapter):
    key = "facebook"

    def get_access_token(self):
        if self.access_token:
            return self.access_token

        url = "https://graph.facebook.com/v14.0/oauth/access_token"
        params = {
            "client_id": settings.FACEBOOK_CLIENT_ID,
            "client_secret": settings.FACEBOOK_CLIENT_SECRET,
            "redirect_uri": f"{self.origin}{settings.SOCIAL_REDIRECT_PATH}",
            "code": self.code,
        }
        response = requests.get(url=url, params=params)
        if not response.ok:
            raise ValidationError(f"FACEBOOK GET TOKEN API ERROR: {response.text}")
        data = response.json()
        return data["access_token"]

    def get_social_user_id(self):
        url = "https://graph.facebook.com/v14.0/debug_token"
        params = {
            "input_token": self.get_access_token(),
            "access_token": f"{settings.FACEBOOK_CLIENT_ID}|{settings.FACEBOOK_CLIENT_ID}",
        }
        response = requests.get(url=url, params=params)
        if not response.ok:
            raise ValidationError(f"FACEBOOK ME API ERROR: {response.text}")
        data = response.json()

        return data["data"]["user_id"], data["data"]


class GoogleAdapter(SocialAdapter):
    key = "google"

    def get_access_token(self):
        pass

    def get_social_user_id(self):
        url = "https://oauth2.googleapis.com/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": f"{self.origin}{settings.SOCIAL_REDIRECT_PATH}",
            "code": self.code,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError("GOOGLE GET TOKEN API ERROR")
        data = response.json()

        decoded = jwt.decode(data["id_token"], "", verify=False)

        return decoded["sub"]


class AppleAdapter(SocialAdapter):
    key = "apple"

    def get_social_user_id(self):
        if not self.access_token:
            headers = {"kid": settings.APPLE_KEY_ID}
            payload = {
                "iss": settings.APPLE_TEAM_ID,
                "iat": timezone.datetime.now(),
                "exp": timezone.datetime.now() + timezone.timedelta(hours=1),
                "aud": "https://appleid.apple.com",
                "sub": settings.APPLE_CLIENT_ID,
            }
            client_secret = jwt.encode(
                payload,
                settings.APPLE_CLIENT_SECRET,
                algorithm="ES256",
                headers=headers,
            )
            url = "https://appleid.apple.com/auth/token"
            data = {
                "grant_type": "authorization_code",
                "client_id": settings.APPLE_CLIENT_ID,
                "client_secret": client_secret,
                "code": self.code,
            }
            response = requests.post(
                url=url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if not response.ok:
                raise ValidationError("APPLE GET TOKEN API ERROR")

            data = response.json()
            access_token = data["id_token"]
        else:
            access_token = self.access_token

        key_payload = requests.get("https://appleid.apple.com/auth/keys").json()
        kid = jwt.get_unverified_header(access_token)["kid"]
        apple_public_key = RSAAlgorithm.from_jwk(
            json.dumps(next(filter(lambda x: x["kid"] == kid, key_payload["keys"])))
        )
        apple_public_key_as_string = apple_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        decoded = jwt.decode(
            access_token,
            key=apple_public_key_as_string,
            algorithms=["RS256"],
            audience=settings.APPLE_APP_ID,
        )
        return decoded["sub"], decoded.get("email", "")
