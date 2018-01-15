import goap


class State:

    def __init__(self):

        self.weapon_ready = False
        self.rounds = 0
        self.clips = 1

        self.enemy_visible = True
        self.enemy_alive = True

    def reload(self, rounds):
        return self.next_state(rounds=self.rounds + rounds)

    def fire(self):
        return self.next_state(rounds=self.rounds - 1, enemy_alive=False)

    @property
    def can_reload(self):
        return self.weapon_ready and self.clips > 0

    @property
    def can_fire(self):
        return (
            self.enemy_visible and
            self.weapon_ready and
            self.rounds > 0
        )

    def next_state(self, **kwargs):
        defaults = {
            'weapon_ready': self.weapon_ready,
            'rounds': self.rounds,
            'clips': self.clips,
            'enemy_visible': self.enemy_visible,
            'enemy_alive': self.enemy_alive,
        }
        defaults.update(kwargs)
        state = self.__class__()
        for k, v in defaults.items():
            setattr(state, k, v)
        return state


class EquipWeapon:

    key = "equip weapon"

    @staticmethod
    def cost(state):
        return 2

    @staticmethod
    def condition(state):
        return not(state.weapon_ready)

    @staticmethod
    def effect(state):
        return state.next_state(weapon_ready=True)


class Reload:

    key = "reload"

    @staticmethod
    def cost(state):
        return 2

    @staticmethod
    def condition(state):
        return state.can_reload

    @staticmethod
    def effect(state):
        return state.reload(6)


class Fire:

    key = "fire"

    @staticmethod
    def cost(state):
        return 2

    @staticmethod
    def condition(state):
        return state.can_fire

    @staticmethod
    def effect(state):
        return state.fire()


class UseTurret:

    key = "use turret"

    @staticmethod
    def cost(state):
        return 10

    @staticmethod
    def condition(state):
        return state.enemy_visible

    @staticmethod
    def effect(state):
        return state.next_state(enemy_alive=False)


class KnifeAttack:

    key = "knife attack"

    @staticmethod
    def cost(state):
        return 12

    @staticmethod
    def condition(state):
        return state.enemy_visible

    @staticmethod
    def effect(state):
        return state.next_state(enemy_alive=False)


class Scout:

    key = "scout"

    @staticmethod
    def cost(state):
        return 1

    @staticmethod
    def condition(state):
        return not(state.enemy_visible)

    @staticmethod
    def effect(state):
        return state.next_state(enemy_visible=True)


class Hide:

    key = "hide"

    @staticmethod
    def cost(state):
        return 1

    @staticmethod
    def condition(state):
        return state.enemy_visible

    @staticmethod
    def effect(state):
        return state.next_state(enemy_visible=False)


class HideFromEnemy:

    label = "Hide from Enemy"

    @staticmethod
    def validate(state, next_state):
        return not(next_state.enemy_visible)


class KillEnemy:

    label = "Kill Enemy"

    @staticmethod
    def validate(state, next_state):
        return not(next_state.enemy_alive)


if __name__ == "__main__":

    actions = [
        Hide,
        Reload,
        Fire,
        UseTurret,
        KnifeAttack,
        EquipWeapon,
        Scout,
    ]

    state = State()

    for goal in [HideFromEnemy, KillEnemy]:

        print("Goal", goal.label)
        plan = goap.create_plan(state, actions, goal)

        for action in plan:
            print(action.key)
