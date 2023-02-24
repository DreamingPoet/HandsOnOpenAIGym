python a2c_agent.py --env MountainCar-v0    
python a2c_agent.py --env CartPole-v1

pip install opencv-python

观测空间
动作空间

观测空间 -- 动作空间 （ 对应关系 是否有意义 ）

奖励函数

超参

启动 并 连接 carla
创建本车玩家
创建传感器
获取数据
施加控制

episode 训练次数

step  = UE 1 fps， 到达期望目的的控制步骤数

分析 carla-gym 的观测参数：

// 关于protobuf 的数据结构说明
https://protobuf.dev/reference/cpp/api-docs/google.protobuf.descriptor/#FieldDescriptor.CppType.details

def _read_observation(self):

    pos_x  =player_measurements.transform.location.x / 100,  # cm -> m
    pos_y = player_measurements.transform.location.y / 100,
    speed = player_measurements.forward_speed,
    col_cars = player_measurements.collision_vehicles,
    col_ped = player_measurements.collision_pedestrians,
    col_other = player_measurements.collision_other,
    other_lane = 100 * player_measurements.intersection_otherlane, # 交叉路口,其他车道
    offroad= 100 * player_measurements.intersection_offroad, # 交叉路口，偏离车道


Vector3D {
    x: float
    y: float
    z: float
}

Rotation3D {
    pitch: float
    yaw: float
    roll: float
}

Transform {
    location: Vector3D
    orientation: Vector3D
    rotation: Rotation3D
}

// 定义一个绑定在车上的盒子
BoundingBox {
    transform: Transform
    extent: Vector3D
}

// 车辆
Vehicle {
    transform: Transform
    bounding_box: BoundingBox
    forward_speed: float
}

// 行人
Pedestrian {
    transform: Transform
    bounding_box: BoundingBox
    forward_speed: float
}

// 交通灯状态
ENUM State {
    GREEN:0
    YELLOW:1
    RED:2
}

// 交通灯
TrafficLight {
    transform: Transform
    state: ENUM
}

// 限速标志
SpeedLimitSign {
    transform: Transform
    speed_limit: float
}

// 代理
Agent {

    id: UINT32
    vehicle: Vehicle
    pedestrian: Pedestrian
    speed_limit_sign: SpeedLimitSign

}


// 传感器类型
ENUM State {
    UNKNOWN:0
    CAMERA:1
    LIDAR_RAY_CAST:2
}

// 传感器
ENUM Type {
    id: UINT32
    type: ENUM
    name: STRING

}

// 场景描述
SceneDescription {
    map_name: STRING
    player_start_spots: Transform
    sensors: Type
}
 
// 观测数据
PlayerMeasurements {
    transform: Transform
    bounding_box: BoundingBox
    acceleration: Vector3D
    forward_speed: float
    collision_vehicles: float
    collision_pedestrians: float
    collision_other: float
    intersection_otherlane: float
    intersection_offroad: float
    autopilot_control: Control
}

// 观测数据
Measurements {
    frame_number: UINT64
    platform_timestamp: UINT32
    game_timestamp: UINT32
    player_measurements: PlayerMeasurements
    non_player_agents: Agent
}



// ActionSpace 对车辆的控制
Control {
    steer: float
    throttle: float
    brake: float
    hand_brake: BOOL
    reverse: BOOL
}


// 请求新  Episode
RequestNewEpisode {
    ini_file: STRING
}

// 
EpisodeReady {
    player_start_spot_index: UINT32
}

EpisodeReady {
    ready: BOOL
}


