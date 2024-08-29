import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class CommonBaseModel(models.Model):
    slug = models.SlugField("slug", unique=True, editable=False, default=uuid.uuid4)

    updated_at = models.DateTimeField(_("data de atualização"), auto_now=True)

    class Meta:
        abstract = True


class CommonModel(CommonBaseModel):
    created_at = models.DateTimeField(_("data de criação"), auto_now_add=True)

    class Meta(CommonBaseModel.Meta):
        abstract = True
        ordering = ["-created_at"]
