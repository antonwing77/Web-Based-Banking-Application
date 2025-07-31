from rest_framework.routers import DefaultRouter
from .views import DebitCardViewSet

router = DefaultRouter()
router.register(r'debitcards', DebitCardViewSet, basename='debitcards')

urlpatterns = router.urls