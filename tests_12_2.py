import unittest

class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run()

                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers


class TournamentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    def setUp(self):
        self.usain = Runner("Усэйн", 10)
        self.andrei = Runner("Андрей", 9)
        self.nick = Runner("Ник", 3)

    @classmethod
    def tearDownClass(cls):
        for key, result in cls.all_results.items():
            print(f"{key}: {result}")

    def test_usain_and_nick(self):
        tournament = Tournament(90, self.usain, self.nick)
        results = tournament.start()
        self.__class__.all_results[1] = {k: str(v) for k, v in results.items()}
        self.assertTrue(str(results[max(results)]) == "Ник")

    def test_andrei_and_nick(self):
        tournament = Tournament(90, self.andrei, self.nick)
        results = tournament.start()
        self.__class__.all_results[2] = {k: str(v) for k, v in results.items()}
        self.assertTrue(str(results[max(results)]) == "Ник")

    def test_usain_andrei_and_nick(self):
        tournament = Tournament(90, self.usain, self.andrei, self.nick)
        results = tournament.start()
        self.__class__.all_results[3] = {k: str(v) for k, v in results.items()}
        self.assertTrue(str(results[max(results)]) == "Ник")


class FixedTournament(Tournament):
    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            self.participants.sort(key=lambda x: -x.speed)  
            for participant in self.participants[:]:  
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers


class FixedTournamentTest(unittest.TestCase):
    def setUp(self):
        self.usain = Runner("Усэйн", 10)
        self.andrei = Runner("Андрей", 9)
        self.nick = Runner("Ник", 3)

    def test_fixed_tournament(self):
        tournament = FixedTournament(90, self.usain, self.andrei, self.nick)
        results = tournament.start()
        self.assertTrue(str(results[max(results)]) == "Ник")
        self.assertEqual(str(results[1]), "Усэйн")
        self.assertEqual(str(results[2]), "Андрей")

if __name__ == "__main__":
    unittest.main()
