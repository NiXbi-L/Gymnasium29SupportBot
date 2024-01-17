from aiogram.fsm.state import StatesGroup, State

class logSates(StatesGroup):
    Choice = State()
    EnterId = State()
    EnterIdT = State()
class admADDStates(StatesGroup):
    EnterFSc = State()
    EnterData = State()
    EnterCData = State()
    EnterTData = State()
    EnterClassNum = State()
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
    EnterDB = State()

class ViewRequest(StatesGroup):
    View = State()
class ViewLCWRequest(StatesGroup):
    View = State()


class Chat(StatesGroup):
    EnterFSc = State()
    Choice = State()
    EnterMessage = State()
    EnterMessageUser = State()

class Planer(StatesGroup):
    Choice = State()
    EnterEvDate = State()
    EnterEvName = State()
    EnterNoteText = State()
    ChangeEvDate = State()
    ChangeEvName = State()
    ChangeNoteText = State()
    YesNo = State()

class ViewEvents(StatesGroup):
    Choice = State()
    EnterMonth = State()
    View = State()

