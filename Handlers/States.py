from aiogram.fsm.state import StatesGroup, State

class logSates(StatesGroup):
    Choice = State
    EnterId = State()
    EnterIdT = State()
class admADDStates(StatesGroup):
    EnterFSc = State()