from typing import Type, Optional, TypeVar
from django.db.models import Model, QuerySet
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import _get_queryset
from utils import NotFoundError

T = TypeVar('T', bound=Model)

def get_object_or_404(
    klass: Type[T] | QuerySet,
    en_message: Optional[str] = None,
    ar_message: Optional[str] = None,
    extra_data: Optional[dict] = None,
    **kwargs
) -> T:
    queryset = _get_queryset(klass)
    
    if not hasattr(queryset, 'get'):
        klass_name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ImproperlyConfigured(
            f"First argument must be a Model, Manager, or QuerySet, not '{klass_name}'"
        )
    
    try:
        return queryset.get(**kwargs)
    except queryset.model.DoesNotExist:
        model_name = queryset.model._meta.verbose_name.title()
        raise NotFoundError(
            en_message=en_message or f"{model_name} not found",
            ar_message=ar_message or f"لم يتم العثور على {model_name}",
        )