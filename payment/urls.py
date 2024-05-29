from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from payment.views import (
   
#     PaymentViewSet,
   
    
#     PesapalCheckoutAPIView,
#     PesapalIPNHandler,
#     PayLaterView,
# )

app_name = "payment"

router = DefaultRouter()
# router.register(r"", PaymentViewSet)

urlpatterns = [
    # path("payments/", include(router.urls)),
    # path(
    #     "create-checkout-session/",
    #     PesapalCheckoutAPIView.as_view(),
    #     name="checkout_session",
    # ),
    # path('pay_later/', PayLaterView.as_view(), name='pay-later'),

    
  
    #path("pesapal/<int:pk>/",PesapalCheckoutAPIView.as_view(), name="pesapalcheckout"),
    # path("ipn/",PesapalIPNHandler.as_view(), name="pesapalipn"),

]
