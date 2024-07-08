from ganesha.core.GaneshaBaseModel import GaneshaBaseModel


class StatusResponse(GaneshaBaseModel):
    status: bool = True
