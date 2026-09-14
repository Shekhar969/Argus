from typing import List

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/zones",
    tags=["zones"]
)


# ============================================================
# MODELS
# ============================================================

class ZonePoint(BaseModel):
    x: float
    y: float


class ZoneCreate(BaseModel):
    zone_id: str
    camera_id: str
    coordinates: List[ZonePoint]


# ============================================================
# GET ALL ZONES
# ============================================================

@router.get("")
def get_zones(request: Request):

    camera_service = request.app.state.camera_service

    zones = camera_service.zone_storage.get_zones()

    return {
        "zones": zones
    }


# ============================================================
# GET ZONE FOR CAMERA
# ============================================================

@router.get("/{camera_id}")
def get_camera_zone(
    camera_id: str,
    request: Request
):

    camera_service = request.app.state.camera_service

    if camera_id != camera_service.camera_id:

        raise HTTPException(
            status_code=404,
            detail="Camera not found"
        )

    zone = (
        camera_service.zone_storage
        .get_zone_for_camera(camera_id)
    )

    if zone is None:

        return {
            "zone": None
        }

    return {
        "zone": zone
    }


# ============================================================
# CREATE / UPDATE ZONE
# ============================================================

@router.post("")
def create_zone(
    zone: ZoneCreate,
    request: Request
):

    camera_service = request.app.state.camera_service

    # --------------------------------------------------------
    # Check camera
    # --------------------------------------------------------

    if zone.camera_id != camera_service.camera_id:

        raise HTTPException(
            status_code=404,
            detail="Camera not found"
        )

    # --------------------------------------------------------
    # Validate points
    # --------------------------------------------------------

    if len(zone.coordinates) < 3:

        raise HTTPException(
            status_code=400,
            detail="Zone must contain at least 3 points"
        )

    # --------------------------------------------------------
    # Convert coordinates
    # --------------------------------------------------------

    coordinates = [
        (
            point.x,
            point.y
        )
        for point in zone.coordinates
    ]

    # --------------------------------------------------------
    # Update runtime zone
    # --------------------------------------------------------

    camera_service.set_zone(
        zone_id=zone.zone_id,
        coordinates=coordinates
    )

    # --------------------------------------------------------
    # Persist zone
    # --------------------------------------------------------

    saved_zone = (
        camera_service.zone_storage.save_zone(
            zone_id=zone.zone_id,
            camera_id=zone.camera_id,
            coordinates=coordinates
        )
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "success": True,
        "zone": saved_zone
    }