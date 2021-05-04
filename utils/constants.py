ACTIVATION_TIME = 10

PLANNING = 0
ACTIVE = 1
IN_CONTROL = 2
FINISHED = 3

STATUSES = [
    (PLANNING, 'PLANNING'),
    (ACTIVE, 'ACTIVE'),
    (IN_CONTROL, 'IN_CONTROL'),
    (FINISHED, 'FINISHED')    
]

UPDATE_MESSAGE = 'Look to this task. There are some updates'
TASK_EXPIRED_MESSAGE = 'Your finish time is expired. You should restructure your task.'

