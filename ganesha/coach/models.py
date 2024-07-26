from ganesha.core.GaneshaBaseModel import GaneshaBaseModel, ObjectIdPydanticAnnotation


class processAudioModelResponse(GaneshaBaseModel):
    response_from_coach: str

