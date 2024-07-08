from ganesha.core.GaneshaBaseModel import GaneshaBaseModel


class locationModel(GaneshaBaseModel):
    latitude: float
    longitude: float


class process8hrModel(GaneshaBaseModel):
    locations: list[locationModel] = []


class process8hrModelResponse(GaneshaBaseModel):
    response_from_coach: str
