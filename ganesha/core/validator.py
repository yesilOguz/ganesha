from functools import wraps
from fastapi import HTTPException, status

from bson import ObjectId


def validate_object_id(param_name):
    def decorator(func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):
            if param_name not in kwargs:
                raise ValueError(f"{param_name} parameter is missing")

            obj_id = kwargs[param_name]

            if not ObjectId.is_valid(obj_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"{param_name}={obj_id} is not valid ObjectId!")

            return func(*args, **kwargs)
        return wrapper_func
    return decorator
