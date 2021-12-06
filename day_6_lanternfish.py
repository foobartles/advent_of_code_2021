from typing import List


class LanternFishSchoolModel:
    NEW_FISH_SPAWN_TIMER = 8
    OLD_FISH_REFRESH_SPAWN_TIMER = 6

    def __init__(self, starting_timers: List[int]):
        self.starting_timers = starting_timers
        self.spawn_timer_counts = {}
        self._reset_model()

    def _reset_model(self):
        self.spawn_timer_counts = dict.fromkeys(range(self.NEW_FISH_SPAWN_TIMER+1), 0)
        for timer in self.starting_timers:
            self.spawn_timer_counts[timer] += 1

    def model_fish_growth(self, number_of_days: int) -> int:
        self._reset_model()
        for day in range(number_of_days):
            self._simulate_day()

        return sum(self.spawn_timer_counts.values())

    def _simulate_day(self):
        spawn_timer_copy = self.spawn_timer_counts.copy()
        for i in range(8):
            spawn_timer_copy[i] = spawn_timer_copy[i+1]
        spawn_timer_copy[self.NEW_FISH_SPAWN_TIMER] = self.spawn_timer_counts[0]
        spawn_timer_copy[self.OLD_FISH_REFRESH_SPAWN_TIMER] += self.spawn_timer_counts[0]
        self.spawn_timer_counts = spawn_timer_copy

    def __str__(self):
        return str(self.spawn_timer_counts)


if __name__ == '__main__':
    with open('puzzle_inputs/day_6.txt', 'r') as f:
        fish_timers =[int(x) for x in f.readline().split(',')]

    fish_model = LanternFishSchoolModel(fish_timers)
    print(f"part one solution: {fish_model.model_fish_growth(18)}")
    print(f"part two solution: {fish_model.model_fish_growth(256)}")



