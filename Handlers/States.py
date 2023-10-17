from aiogram.fsm.state import StatesGroup, State

class logSates(StatesGroup):
    Choice = State()
    EnterId = State()
    EnterIdT = State()
class admADDStates(StatesGroup):
    EnterFSc = State()
    EnterData = State()

class LeaderClubStates(StatesGroup):
    Choice = State()
    EnterApl = State()
    EnterIdea = State()


class ERROR_States(StatesGroup):
    EnterReport = State()
    AddPhotos = State()

class AdmStates(StatesGroup):
    Choice = State()
    LCAplChoice = State()
    EnterComment = State()
    notification = State()
