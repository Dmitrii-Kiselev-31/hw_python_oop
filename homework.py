from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {training_type}; '
               'Длительность:{duration: 0.3f} ч.; '
               'Дистанция:{distance: 0.3f} км; '
               'Ср. скорость:{speed: 0.3f} км/ч; '
               'Потрачено ккал: {calories:0.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           distance,
                           mean_speed,
                           spent_calories)


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: float = 18
    coeff_calorie_2: float = 20

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1
                * self.get_mean_speed()
                - self.coeff_calorie_2)
                * self.weight
                / self.M_IN_KM
                * (self.duration
                * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_walking_1: float = 0.035
    coeff_walking_2: float = 2
    coeff_walking_3: float = 0.029

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.coeff_walking_1
                * self.weight
                + (self.get_mean_speed()
                   ** self.coeff_walking_2
                   // self.height)
                * self.coeff_walking_3
                * self.weight)
                * (self.duration
                * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_swim_1: float = 1.1
    coeff_swim_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.coeff_swim_1)
                * self.coeff_swim_2
                * self.weight)

    def get_distance(self) -> float:
        return (self.action
                * self.LEN_STEP
                / self.M_IN_KM)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    return TRAINING_TYPE[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


TRAINING_TYPE: dict[str, ClassVar] = {'SWM': Swimming,
                                      'RUN': Running,
                                      'WLK': SportsWalking,
                                      }
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        if workout_type not in TRAINING_TYPE:
            raise KeyError(f'Тренировка типа "{workout_type}" не поддерживается')
        training = read_package(workout_type, data)
        main(training)
