from abc import ABC, abstractmethod
from typing import Set, Any
from faker import Faker
import time


fake = Faker()


class Observer(ABC):
    @abstractmethod
    def on_message(self, data: Any) -> None:
        pass


class Provider(ABC):
    def __init__(self):
        self.subs: Set[Observer] = set()

    def subscribe(self, *observers: Observer) -> None:
        self.subs.update(observers)

    def unsubscribe(self, observer: Observer) -> None:
        self.subs.discard(observer)

    def push_message(self, data: Any) -> None:
        for obs in self.subs:
            obs.on_message(data)


## usage
class NameDataProvider(Provider):

    def stream_bank_data(self, count=5):
        for _ in range(count):
            self.push_message(fake.name())
            time.sleep(0.5)


class SomeConsumer(Observer):
    def on_message(self, data):
        print("Message Recieved @1:", data)


class SomeConsumer2(Observer):
    def on_message(self, data):
        print("Message Recieved @2:", data)


obs = SomeConsumer()
obs2 = SomeConsumer2()

pub = NameDataProvider()
pub.subscribe(obs, obs2)

pub.stream_bank_data()


pub.unsubscribe(obs2)
