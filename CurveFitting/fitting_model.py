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
