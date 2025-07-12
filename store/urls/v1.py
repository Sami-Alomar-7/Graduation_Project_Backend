from django.urls import path
from store.views.store_list_views import (
    CustomerStoreBookListView,
    CustomerStoreBookDetailView,
    AdminStoreBookListView,
    AdminStoreBookDetailView,
    AdminStoreBookByStatusView
)
from store.views.store_delete_views import AdminStoreBookDeleteView
from store.views.customer_store_request_views import (
    CustomerStoreRequestView,
    CustomerStoreRequestListView,
    CustomerStoreRequestByStatusView
)
from store.views.admin_store_action_views import (
    AdminStoreActionView,
    AdminPendingRequestsView
)

urlpatterns = [
    # Customer store list books endpoints
    path('customer/store/books/', CustomerStoreBookListView.as_view(), name='customer-store-book-list'),
    path('customer/store/books/<int:store_book_id>/', CustomerStoreBookDetailView.as_view(), name='customer-store-book-detail'),
    
    # Admin store detail book endpoints
    path('admin/store/books/', AdminStoreBookListView.as_view(), name='admin-store-book-list'),
    path('admin/store/books/<int:store_book_id>/', AdminStoreBookDetailView.as_view(), name='admin-store-book-detail'),
    path('admin/store/books/status/<str:status>/', AdminStoreBookByStatusView.as_view(), name='admin-store-book-by-status'),
    
    # Admin store delete endpoint
    path('admin/store/books/<int:book_id>/delete/', AdminStoreBookDeleteView.as_view(), name='admin-store-book-delete'),
    
    # Customer store request endpoints
    path('customer/store/request/<int:book_id>/', CustomerStoreRequestView.as_view(), name='customer-store-request'),
    path('customer/store/requests/', CustomerStoreRequestListView.as_view(), name='customer-store-requests-list'),
    path('customer/store/requests/status/<str:status>/', CustomerStoreRequestByStatusView.as_view(), name='customer-store-requests-by-status'),
    
    # Admin store action endpoints
    path('admin/store/action/<int:store_book_id>/', AdminStoreActionView.as_view(), name='admin-store-action'),
    path('admin/store/pending-requests/', AdminPendingRequestsView.as_view(), name='admin-pending-requests'),
]
