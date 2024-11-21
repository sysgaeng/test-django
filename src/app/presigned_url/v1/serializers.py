import random
import string

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from django.apps import apps
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.presigned_url.utils import FIELD_CHOICES, FileTypeChoices


class PresignedSerializer(serializers.Serializer):
    file_name = serializers.CharField(write_only=True)
    file_type = serializers.ChoiceField(choices=FileTypeChoices.choices, write_only=True)
    field_choice = serializers.ChoiceField(choices=FIELD_CHOICES, write_only=True)
    url = serializers.URLField(read_only=True)
    fields = serializers.JSONField(read_only=True)

    def validate(self, attrs):
        model, field_name = self.get_field_info(attrs.get("field_choice"))
        upload_path = self.get_upload_path(model, field_name)
        response = self.create_presigned_post(attrs["file_name"], attrs["file_type"], upload_path)
        attrs.update(response)
        return attrs

    def create(self, validated_data):
        return validated_data

    def get_field_info(self, field_choice):
        app_label, model_name, field_name = field_choice.split(".")
        try:
            model = apps.get_model(app_label, model_name)
        except Exception as e:
            raise ValidationError("Invalid Model Data")
        return model, field_name

    def get_upload_path(self, model, field_name):
        field = model._meta.get_field(field_name)
        if hasattr(field, "upload_to"):
            return field.upload_to
        return None

    def create_presigned_post(self, file_name, file_type, upload_path=None):
        s3_config = Config(
            region_name="ap-northeast-2",
            signature_version="s3v4",
        )
        s3_client = boto3.client("s3", config=s3_config)
        basename = "/".join(["_media", upload_path])
        object_key = self.get_object_key(s3_client, basename, file_name)

        response = s3_client.generate_presigned_post(
            settings.AWS_STORAGE_BUCKET_NAME,
            object_key,
            Conditions=[
                ["content-length-range", 0, 20971520],  # 20MB
                ["starts-with", "$Content-Type", f"{file_type}/"],
            ],
            ExpiresIn=360,
        )
        return response

    def get_object_key(self, s3_client, basename, file_name):
        object_key = f"{basename}{file_name}"
        try:
            s3_client.head_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=object_key,
            )
            name, ext = file_name.rsplit(".", 1)
            characters = string.ascii_lowercase + string.digits
            random_string = "".join(random.choices(characters, k=7))
            file_name = ".".join([f"{name}_{random_string}", ext])
            return self.get_object_key(s3_client, basename, file_name)
        except ClientError:
            return object_key
