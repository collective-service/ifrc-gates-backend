from django.db import models
from django.urls import reverse


def get_admin_url(model: models.Model, action):
    meta = model._meta
    return reverse(f'admin:{meta.app_label}_{meta.model_name}_{action}')
