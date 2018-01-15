import heapq


class Node:
    def __init__(self, state, cost=0, parent=None, action=None):
        self.state = state
        self.cost = cost
        self.parent = parent
        self.action = action
        self.key = self.action.key if self.action else None

    def __str__(self):
        return self.action.key if self.action else "root"

    def __repr__(self):
        return "<%s>" % self

    def __gt__(self, other):
        return self.cost > other.cost

    def build_graph(self, actions, goal, leaves=None):
        leaves = leaves or []

        for action in actions:
            if action.condition(self.state):
                next_state = action.effect(self.state)
                cost = self.cost + action.cost(next_state)
                node = self.__class__(
                    parent=self,
                    cost=cost,
                    state=next_state,
                    action=action,
                )
                if goal.validate(self.state, next_state):
                    heapq.heappush(leaves, node)
                else:
                    subset = [a for a in actions if a.key != action.key]
                    return node.build_graph(subset, goal, leaves)
        return leaves

    def get_plan(self, goal):

        plan = []
        node = self

        while node is not None:
            if node.action:
                plan.insert(0, node.action)
            node = node.parent

        return plan


def create_plan(state, actions, goal):

    root = Node(parent=None, cost=0, state=state, action=None)
    try:
        return heapq.heappop(root.build_graph(actions, goal)).get_plan(goal)
    except IndexError:
        return []
