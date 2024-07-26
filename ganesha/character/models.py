from typing import Annotated

from bson import ObjectId

from ganesha.core.GaneshaBaseModel import GaneshaBaseModel, ObjectIdPydanticAnnotation


class CharacterGetModelListResponse(GaneshaBaseModel):
    characters: list[str]


class CameraOrbitSettings(GaneshaBaseModel):
    theta: float = 0
    phi: float = 75
    radius: float = 105


class CameraTargetSettings(GaneshaBaseModel):
    x: float
    y: float
    z: float


class CharacterCameraSettings(GaneshaBaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
    object_name: str
    camera_orbit: CameraOrbitSettings
    camera_target: CameraTargetSettings


class CharacterGetCameraSettings(GaneshaBaseModel):
    object_name: str
    camera_orbit: CameraOrbitSettings
    camera_target: CameraTargetSettings


class CharacterGetCameraSettingsResponse(GaneshaBaseModel):
    object_name: str
    camera_orbit: CameraOrbitSettings
    camera_target: CameraTargetSettings
