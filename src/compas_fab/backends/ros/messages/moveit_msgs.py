from __future__ import absolute_import

from .std_msgs import ROSmsg
from .std_msgs import Header

from .geometry_msgs import PoseStamped
from .geometry_msgs import Vector3
from .geometry_msgs import Quaternion

from .sensor_msgs import JointState
from .sensor_msgs import MultiDOFJointState

from .trajectory_msgs import JointTrajectory
from .trajectory_msgs import MultiDOFJointTrajectory

from .object_recognition_msgs import ObjectType

from .octomap_msgs import OctomapWithPose

class CollisionObject(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/CollisionObject.html
    """
    ADD = 0
    REMOVE = 1
    APPEND = 2
    MOVE = 3

    def __init__(self, header=None, id="collision_obj", type=None,
                 primitives=None, primitive_poses=None, meshes=None, mesh_poses=None,
                 planes=None, plane_poses=None, operation=0):
        self.header = header if header else Header() # a header, used for interpreting the poses
        self.id = id # the id of the object (name used in MoveIt)
        self.type = type if type else ObjectType() # The object type in a database of known objects
        # solid geometric primitives
        self.primitives = primitives if primitives else []
        self.primitive_poses = primitive_poses if primitive_poses else []
        # meshes
        self.meshes = meshes if meshes else []
        self.mesh_poses = mesh_poses if mesh_poses else []
        # bounding planes
        self.planes = planes if planes else []
        self.plane_poses = plane_poses if plane_poses else []
        self.operation = operation  # ADD or REMOVE or APPEND or MOVE


class AttachedCollisionObject(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/AttachedCollisionObject.html
    """

    def __init__(self, link_name=None, object=None, touch_links=None,
                 detach_posture=None, weight=0):
        self.link_name = link_name if link_name else ''
        self.object = object if object else CollisionObject()
        self.touch_links = touch_links if touch_links else []
        self.detach_posture = detach_posture if detach_posture else JointTrajectory()
        self.weight = weight


class Constraints(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/Constraints.html
    """

    def __init__(self, name='', joint_constraints=None, position_constraints=None,
                 orientation_constraints=None, visibility_constraints=None):
        self.name = name
        self.joint_constraints = joint_constraints if joint_constraints else []
        self.position_constraints = position_constraints if position_constraints else []
        self.orientation_constraints = orientation_constraints if orientation_constraints else []
        self.visibility_constraints = visibility_constraints if visibility_constraints else []


class RobotState(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/RobotState.html
    """

    def __init__(self, joint_state=None, multi_dof_joint_state=None,
                 attached_collision_objects=None, is_diff=False):
        self.joint_state = joint_state if joint_state else JointState()
        self.multi_dof_joint_state = multi_dof_joint_state if multi_dof_joint_state else MultiDOFJointState()
        self.attached_collision_objects = attached_collision_objects if attached_collision_objects else []
        self.is_diff = is_diff

    @classmethod
    def from_msg(cls, msg):
        joint_state = JointState.from_msg(msg['joint_state'])
        multi_dof_joint_state = MultiDOFJointState.from_msg(
            msg['multi_dof_joint_state'])
        attached_collision_objects = [AttachedCollisionObject.from_msg(
            item) for item in msg['attached_collision_objects']]
        return cls(joint_state, multi_dof_joint_state, attached_collision_objects, msg['is_diff'])


class PositionIKRequest(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/PositionIKRequest.html

    Examples
    --------
    >>> base_link = 'base_link'
    >>> planning_group = 'manipulator'
    >>> pose = Pose([420, -25, 459], [1, 0, 0], [0, 1, 0])
    >>> joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint',
                       'elbow_joint', 'wrist_1_joint', 'wrist_2_joint',
                       'wrist_3_joint']
    >>> joint_positions = [3.39, -1.47, -2.05, 0.38, -4.96, -6.28]
    >>> header = Header(frame_id='base_link')
    >>> pose_stamped = PoseStamped(header, pose)
    >>> joint_state = JointState(name=joint_names, position=joint_positions,
                                 header=header)
    >>> multi_dof_joint_state = MultiDOFJointState(header=header,
                                                   joint_names=joint_names)
    >>> start_state = RobotState(joint_state, multi_dof_joint_state)
    >>> ik_request = PositionIKRequest(group_name=planning_group,
                                       robot_state=start_state,
                                       pose_stamped=pose_stamped,
                                       avoid_collisions=True)
    """

    def __init__(self, group_name="robot", robot_state=None, constraints=None,
                 pose_stamped=None, timeout=1.0, attempts=8,
                 avoid_collisions=True):
        self.group_name = group_name
        self.robot_state = robot_state if robot_state else RobotState()
        self.constraints = constraints if constraints else Constraints()
        self.avoid_collisions = avoid_collisions
        self.pose_stamped = pose_stamped if pose_stamped else PoseStamped()
        self.timeout = timeout
        self.attempts = attempts


class RobotTrajectory(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/RobotTrajectory.html
    """

    def __init__(self, joint_trajectory=JointTrajectory(),
                 multi_dof_joint_trajectory=MultiDOFJointTrajectory()):
        self.joint_trajectory = joint_trajectory
        self.multi_dof_joint_trajectory = multi_dof_joint_trajectory

    @classmethod
    def from_msg(cls, msg):
        joint_trajectory = JointTrajectory.from_msg(msg['joint_trajectory'])
        multi_dof_joint_trajectory = MultiDOFJointTrajectory.from_msg(
            msg['multi_dof_joint_trajectory'])
        return cls(joint_trajectory, multi_dof_joint_trajectory)


class MoveItErrorCodes(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/MoveItErrorCodes.html
    """
    # overall behavior
    SUCCESS = 1
    FAILURE = 99999

    PLANNING_FAILED = -1
    INVALID_MOTION_PLAN = -2
    MOTION_PLAN_INVALIDATED_BY_ENVIRONMENT_CHANGE = -3
    CONTROL_FAILED = -4
    UNABLE_TO_AQUIRE_SENSOR_DATA = -5
    TIMED_OUT = -6
    PREEMPTED = -7

    # planning & kinematics request errors
    START_STATE_IN_COLLISION = -10
    START_STATE_VIOLATES_PATH_CONSTRAINTS = -11

    GOAL_IN_COLLISION = -12
    GOAL_VIOLATES_PATH_CONSTRAINTS = -13
    GOAL_CONSTRAINTS_VIOLATED = -14

    INVALID_GROUP_NAME = -15
    INVALID_GOAL_CONSTRAINTS = -16
    INVALID_ROBOT_STATE = -17
    INVALID_LINK_NAME = -18
    INVALID_OBJECT_NAME = -19

    # system errors
    FRAME_TRANSFORM_FAILURE = -21
    COLLISION_CHECKING_UNAVAILABLE = -22
    ROBOT_STATE_STALE = -23
    SENSOR_INFO_STALE = -24

    # kinematics errors
    NO_IK_SOLUTION = -31

    def __init__(self, val=-31):
        self.val = val

    def __int__(self):
        return self.val

    def __eq__(self, other):
        return self.val == other

    def __ne__(self, other):
        return self.val != other

    @property
    def human_readable(self):
        cls = type(self)
        for k, v in cls.__dict__.items():
            if v == self.val:
                return k
        return ''


class PlannerParams(ROSmsg):
    """http://docs.ros.org/melodic/api/moveit_msgs/html/msg/PlannerParams.html
    """

    def __init__(self, keys=None, values=None, descriptions=None):
        self.keys = keys if keys else [] # parameter names (same size as values)
        self.values = values if values else [] # parameter values (same size as keys)
        self.descriptions = descriptions if descriptions else [] # parameter description (can be empty)

class WorkspaceParameters(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/WorkspaceParameters.html
    """
    def __init__(self, header=Header(), min_corner=Vector3(-1000,-1000,-1000), max_corner=Vector3(1000,1000,1000)):
        self.header = header
        self.min_corner = min_corner
        self.max_corner = max_corner

class TrajectoryConstraints(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/TrajectoryConstraints.html
    """
    def __init__(self, constraints=None):
        self.constraints = constraints if constraints else [] #Constraints[]


class JointConstraint(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/JointConstraint.html
    """
    def __init__(self, joint_name="", position=0, tolerance_above=0, tolerance_below=0, weight=1.):
        self.joint_name = joint_name
        self.position = position
        self.tolerance_above = tolerance_above
        self.tolerance_below = tolerance_below
        self.weight = weight

class VisibilityConstraint(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/VisibilityConstraint.html
    """
    def __init__(self):
        raise NotImplementedError

class BoundingVolume(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/BoundingVolume.html
    """
    def __init__(self, primitives=None, primitive_poses=None, meshes=None,
                 mesh_poses=None):
        self.primitives = primitives if primitives else [] #shape_msgs/SolidPrimitive[]
        self.primitive_poses = primitive_poses if primitive_poses else [] #geometry_msgs/Pose[]
        self.meshes = meshes if meshes else [] #shape_msgs/Mesh[]
        self.mesh_poses = mesh_poses if mesh_poses else [] #geometry_msgs/Pose[]

class PositionConstraint(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/PositionConstraint.html
    """
    def __init__(self, header=None, link_name=None, target_point_offset=None,
                 constraint_region=None, weight=None):
        self.header = header if header else Header()
        self.link_name = link_name if link_name else ""
        self.target_point_offset = target_point_offset if target_point_offset else Vector3(0.,0.,0.) # geometry_msgs/Vector3
        self.constraint_region = constraint_region if constraint_region else BoundingVolume() # moveit_msgs/BoundingVolume
        self.weight = weight if weight else 1.# float64

class OrientationConstraint(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/OrientationConstraint.html
    """
    def __init__(self, header=None, orientation=None, link_name=None,
                 absolute_x_axis_tolerance=0.0, absolute_y_axis_tolerance=0.0,
                 absolute_z_axis_tolerance=0.0, weight=1):
        self.header = header if header else Header()
        self.orientation = orientation if orientation else Quaternion()#geometry_msgs/Quaternion
        self.link_name = link_name if link_name else ""
        self.absolute_x_axis_tolerance = absolute_x_axis_tolerance
        self.absolute_y_axis_tolerance = absolute_y_axis_tolerance
        self.absolute_z_axis_tolerance = absolute_z_axis_tolerance
        self.weight = weight # float64


class PlanningSceneComponents(ROSmsg):
    """http://docs.ros.org/kinetic/api/moveit_msgs/html/msg/PlanningSceneComponents.html
    """
    SCENE_SETTINGS = 1
    ROBOT_STATE=2
    ROBOT_STATE_ATTACHED_OBJECTS=4
    WORLD_OBJECT_NAMES=8
    WORLD_OBJECT_GEOMETRY=16
    OCTOMAP=32
    TRANSFORMS=64
    ALLOWED_COLLISION_MATRIX=128
    LINK_PADDING_AND_SCALING=256
    OBJECT_COLORS=512

    def __init__(self, components=None):
        self.components = components if components else self.SCENE_SETTINGS

    def __eq__(self, other):
        return self.components == other

    @property
    def human_readable(self):
        cls = type(self)
        for k, v in cls.__dict__.items():
            if v == self.components:
                return k
        return ''

class  AllowedCollisionMatrix(ROSmsg):
    """http://docs.ros.org/melodic/api/moveit_msgs/html/msg/AllowedCollisionMatrix.html
    """
    def __init__(self, entry_names=None, entry_values=None, default_entry_names=None, default_entry_values=None):
        self.entry_names = entry_names if entry_names else [] # string[]
        self.entry_values = entry_values if entry_values else [] # moveit_msgs/AllowedCollisionEntry[]
        self.default_entry_names = default_entry_names if default_entry_names else [] # string[]
        self.default_entry_values = default_entry_values if default_entry_values else [] # bool[]

class PlanningSceneWorld(ROSmsg):
    """http://docs.ros.org/melodic/api/moveit_msgs/html/msg/PlanningSceneWorld.html
    """
    def __init__(self, collision_objects=None, octomap=None):
        self.collision_objects = collision_objects if collision_objects else [] #collision objects # CollisionObject[]
        self.octomap = octomap if octomap else OctomapWithPose() # octomap_msgs/OctomapWithPose

class PlanningScene(ROSmsg):
    """http://docs.ros.org/melodic/api/moveit_msgs/html/msg/PlanningScene.html
    """
    def __init__(self, name='', robot_state=None, robot_model_name='',
                 fixed_frame_transforms=None, allowed_collision_matrix=None,
                 link_padding=None, link_scale=None, object_colors=None, world=None,
                 is_diff=False):
        self.name = name # string
        self.robot_state = robot_state if robot_state else RobotState() # moveit_msgs/RobotState
        self.robot_model_name = robot_model_name # string
        self.fixed_frame_transforms = fixed_frame_transforms if fixed_frame_transforms else [] # geometry_msgs/TransformStamped[]
        self.allowed_collision_matrix = allowed_collision_matrix if allowed_collision_matrix else AllowedCollisionMatrix()
        self.link_padding = link_padding if link_padding else [] # moveit_msgs/LinkPadding[]
        self.link_scale = link_scale if link_scale else [] # moveit_msgs/LinkScale[]
        self.object_colors = object_colors if object_colors else [] # moveit_msgs/ObjectColor[]
        self.world = world if world else PlanningSceneWorld() # moveit_msgs/PlanningSceneWorld
        self.is_diff = is_diff # bool

        """
        SCENE_SETTINGS = 1
        ROBOT_STATE=2
        ROBOT_STATE_ATTACHED_OBJECTS=4
        WORLD_OBJECT_NAMES=8
        WORLD_OBJECT_GEOMETRY=16
        OCTOMAP=32
        TRANSFORMS=64
        ALLOWED_COLLISION_MATRIX=128
        LINK_PADDING_AND_SCALING=256
        OBJECT_COLORS=512
        """


    @classmethod
    def from_msg(cls, msg):
        robot_state = RobotState.from_msg(msg['robot_state'])
        allowed_collision_matrix = msg['allowed_collision_matrix']
        world = msg['world']
        return cls(msg['name'], robot_state, msg['robot_model_name'],
                 msg['fixed_frame_transforms'], allowed_collision_matrix,
                 msg['link_padding'], msg['link_scale'], msg['object_colors'],
                 world, msg['is_diff'])

