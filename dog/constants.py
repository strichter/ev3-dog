from pybricks.parameters import Direction, Port

# Wait time in milliseconds inbetween busy loop iterations.
DEFAULT_WAIT_TIME = 10

# The maximum speed of the leg axles. This vlaue has been carefully measured
# to ensure that the robot stays steady while executing an action.
MAX_SPEED = 125

# Default speed for all robot actions.
DEFAULT_SPEED = MAX_SPEED // 2

# Reset speed.
RESET_SPEED = -DEFAULT_SPEED

# The duty/actuation to apply to the motors during reset. This value has been
# carefully measured to allow the legs to fold up but not jam into th emodel.
RESET_DUTY = 40


#### Front Leg Set

FRONT_RIGHT_LEG_UPPER_PORT = Port.D
FRONT_RIGHT_LEG_LOWER_PORT = Port.C
FRONT_LEFT_LEG_UPPER_PORT = Port.A
FRONT_LEFT_LEG_LOWER_PORT = Port.B

FRONT_UPPER_DIRECTION = Direction.COUNTERCLOCKWISE
FRONT_LOWER_DIRECTION = Direction.COUNTERCLOCKWISE

FRONT_UPPER_GEARS = [8, 40]
FRONT_LOWER_GEARS = [8, 40]

# These angles have been carefully measured to provide a max upright position
# while keep the robot stable. An angle of 0 degrees is the folded up position.
FRONT_MAX_UPRIGHT_UPPER_ANGLE = 80
FRONT_MAX_UPRIGHT_LOWER_ANGLE = 120

# Those angles are relative to the max upright angles.
FRONT_MAX_LIFTUP_UPPER_ANGLE = 60
FRONT_MAX_LIFTUP_LOWER_ANGLE = 40

#### Back Leg Set

BACK_RIGHT_LEG_UPPER_PORT = Port.A
BACK_RIGHT_LEG_LOWER_PORT = Port.B
BACK_LEFT_LEG_UPPER_PORT = Port.D
BACK_LEFT_LEG_LOWER_PORT = Port.C

BACK_UPPER_DIRECTION = Direction.CLOCKWISE
BACK_LOWER_DIRECTION = Direction.CLOCKWISE

BACK_UPPER_GEARS = [8, 40]
BACK_LOWER_GEARS = [8, 40]

# These angles have been carefully measured to provide a max upright position
# while keep the robot stable. An angle of 0 degrees is the folded up position.
BACK_MAX_UPRIGHT_UPPER_ANGLE = 60
BACK_MAX_UPRIGHT_LOWER_ANGLE = 120

# XXX: Angles need to be determined.
# Those angles are relative to the max upright angles.
BACK_MAX_LIFTUP_UPPER_ANGLE = 0
BACK_MAX_LIFTUP_LOWER_ANGLE = 135

