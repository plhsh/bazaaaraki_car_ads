from dataclasses import dataclass


from api.district import District
# from bot.subscriptions import Subscription
# !!! Substitute or smth here


@dataclass
class Ad:
    title: str
    year: int
    price: int
    milage: int
    transmission: str
    engine_type: str
    id: int
    location_1: str
    location_2: str
    date: str
    url: str

    def __str__(self) -> str:
        return (
            f'Title: {self.title}\n'
            f'Year: {self.year}\n'
            f'Price: {self.price}\n'
            f'{self.milage} {self.transmission} {self.engine_type}\n'
            f'Ad ID: {self.id}\n'
            f'{self.location_1}: {self.location_2}\n'
            f'{self.date}\n'
            f'{self.url}\n\n'
               )

    def district(self) -> District:
        if "Paphos" in self.location_1:
            return District.PAPHOS
        elif "Famagusta" in self.location_1:
            return District.FAMAGUSTA
        elif "Larnaka" in self.location_1:
            return District.LARNACA
        elif "Lefkosia" in self.location_1:
            return District.LEFKOSIA
        elif "Limassol" in self.location_1:
            return District.LIMASSOL
        else:
            return District.UNKNOWN

    # def matches_subscription(self, subscription: Subscription) -> bool:
    #     price = int(float(self.price))
    #     district = self.district().value
    #
    #     matches_car = price in range(subscription.car.price_min, subscription.car.price_max) \
    #                   and district == subscription.car.district \
    #                   and self.category == Category.CARS
    #
    #     marches_estate = price in range(subscription.estate.price_min, subscription.estate.price_max) \
    #                      and district == subscription.estate.district \
    #                      and self.category == Category.ESTATE
    #
    #     return matches_car or marches_estate