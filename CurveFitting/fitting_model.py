from enum import Enum


class FittingModel(Enum):
    Linear = "linear"
    Square = "square"
    Parabolic = "quadratic"
    # Sinusoidal = "sinusoidal"

    @classmethod
    def value_of(cls, target_value:str):
        for e in FittingModel:
            if e.value == target_value:
                return e
        raise ValueError(f'{target_value} is INVALID')
    
    def get_equation_name(cls):
        if cls.value == FittingModel.Linear:
            return "ax + b"
        elif cls.value== FittingModel.Parabolic:
            return "ax^2 + bx + c"
        elif cls.Square== FittingModel.Square:
            return "ax^2 + b"
        else:
            raise ValueError(f'{cls.value} is INVALID')
            
