from . import prepare,tools
from .states import standard,programmer

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"STANDARD": standard.CalculatorStd(),
              "PROGRAMMER":programmer.CalculatorPro()}
    controller.setup_states(states, "STANDARD")
    controller.main()
