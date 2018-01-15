import goap


class State:

    def __init__(self, axe_available, axe_equipped, wood=0):
        self.axe_available = axe_available
        self.axe_equipped = axe_equipped
        self.wood = wood

    def next_state(self, **kwargs):
        new_state = {
            'axe_available': self.axe_available,
            'axe_equipped': self.axe_equipped,
            'wood': self.wood,
        }
        new_state.update(kwargs)
        return self.__class__(**new_state)


class ChopWood:
    key = "chop wood"

    @staticmethod
    def cost(state):
        return 2

    @staticmethod
    def condition(state):
        return state.axe_equipped

    @staticmethod
    def effect(state):
        return state.next_state(wood=state.wood + 1)


class GetAxe:
    key = "get axe"

    @staticmethod
    def cost(state):
        return 2

    @staticmethod
    def condition(state):
        return state.axe_available and not state.axe_equipped

    @staticmethod
    def effect(state):
        return state.next_state(axe_equipped=True)


class GatherWood:
    key = "gather wood"

    @staticmethod
    def cost(state):
        return 5

    @staticmethod
    def condition(state):
        return True

    @staticmethod
    def effect(state):
        return state.next_state(wood=state.wood + 1)


class CollectWood:
    label = "Gather Wood"

    @staticmethod
    def validate(state, next_state):
        return next_state.wood > state.wood


if __name__ == "__main__":

    actions = [
        GatherWood,
        GetAxe,
        ChopWood,
    ]

    print('I have an axe in my hand')
    state = State(True, True)
    plan = goap.create_plan(state, actions, CollectWood)

    for action in plan:
        print(action.key)

    print('I must fetch an axe')
    state = State(True, False)
    plan = goap.create_plan(state, actions, CollectWood)

    for action in plan:
        print(action.key)

    print('No axe is available')
    state = State(False, False)
    plan = goap.create_plan(state, actions, CollectWood)

    for action in plan:
        print(action.key)
