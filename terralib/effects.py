class Buff:
    def __init__(self, potion_id: int, duration: int):
        self.id = potion_id
        self.duration = duration

    def __str__(self):
        return f"Potion ID: {self.id}, Potion Duration: {self.duration}"

    def get_potion_id(self) -> int:
        return self.id

    def get_potion_duration(self) -> int:
        return self.Duration


class Debuff(Buff):
    def __init__(self, potion_id: int, duration: int):
        super(potion_id, duration)

    def get_potion_id(self) -> int:
        return self.id

    def get_potion_duration(self) -> int:
        return self.duration
