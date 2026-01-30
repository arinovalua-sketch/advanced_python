from django.urls import path
from .views import (
    items_page,
    lost_items,
    register,
    dashboard,
    add_item,
    claim_item,
    api_items,
)

urlpatterns = [
    path('', items_page),
    path('lost/', lost_items),
    path('register/', register),
    path('dashboard/', dashboard),
    path('add/', add_item),
    path('claim/<int:item_id>/', claim_item),

    path('api/items/', api_items),
]

