from django.conf.urls import url
 
from . import view

from django.conf.urls.static import static
from . import settings

# static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    url(r'^$', view.index),
    url(r'^savefile/$', view.savefile),  # savefile函数用来存储文件
]