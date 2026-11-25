"""Run the same simulated approved effect through two agent instances."""
from pathlib import Path
from projects.p03_tool_agent.app import Agent, Approval
from projects.p03_tool_agent.state import SQLiteActionStore


def main():
    path = Path('generated/p3_effects.db')
    path.parent.mkdir(parents=True, exist_ok=True)
    approval = Approval('demo', 'acknowledge_alert', 'A-17', 'lesson-key-1')
    state = SQLiteActionStore(path)
    state.grant(approval)
    print(Agent(effect_store=state).simulate_action('demo', 'acknowledge_alert',
                                                     'A-17', 'lesson-key-1', approval))
    print(Agent(effect_store=SQLiteActionStore(path)).simulate_action(
        'demo', 'acknowledge_alert', 'A-17', 'lesson-key-1', approval))


if __name__ == '__main__':
    main()
