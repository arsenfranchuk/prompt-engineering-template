from fastapi import APIRouter, Depends, Query

from app.dependencies import get_current_user, get_dashboard_service
from app.models.dashboard import DashboardSummaryResponse
from app.models.user import UserInDb
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(
    period: str = Query(
        default="current_month",
        description="Period: current_month, previous_month, current_year, all",
    ),
    current_user: UserInDb = Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardSummaryResponse:
    return service.get_summary(current_user.id, period=period)
