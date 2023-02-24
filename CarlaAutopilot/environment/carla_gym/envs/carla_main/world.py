#!/usr/bin/env python

# ==============================================================================
# -- World ---------------------------------------------------------------
# ==============================================================================

import random
import sys
import carla
from environment.carla_gym.envs.carla_main.camera_manager import CameraManager

from environment.carla_gym.envs.carla_main.util import find_weather_presets, get_actor_blueprints
from environment.carla_gym.envs.carla_main.collision_sensor import CollisionSensor
from environment.carla_gym.envs.carla_main.lane_invasion_sensor import LaneInvasionSensor
from environment.carla_gym.envs.carla_main.util import get_actor_display_name


class World(object):
    """ Class representing the surrounding environment """

    def __init__(self, carla_world, args):
        """Constructor method"""
        self._args = args
        self.world = carla_world
        try:
            self.map = self.world.get_map()
        except RuntimeError as error:
            print('RuntimeError: {}'.format(error))
            print('  The server could not send the OpenDRIVE (.xodr) file:')
            print('  Make sure it exists, has the same name of your town, and is correct.')
            sys.exit(1)
        # self.hud = hud
        self.player = None
        self.player_start_loction = None
        self.collision_sensor = None
        self.lane_invasion_sensor = None
        self.gnss_sensor = None
        self.camera_manager = None
        self._gamma = args.gamma
        self._weather_presets = find_weather_presets()
        self._weather_index = 0
        self._actor_filter = args.filter
        self._actor_generation = args.generation
        self._control = carla.VehicleControl()
        self.restart(args)
        self.world.on_tick(self.on_world_tick)
        self.recording_enabled = False
        self.recording_start = 0
        self.frame = 0

    def restart(self, args):
        """Restart the world"""
        # Keep same camera config if the camera manager exists.
        cam_index = self.camera_manager.index if self.camera_manager is not None else 0
        cam_pos_id = self.camera_manager.transform_index if self.camera_manager is not None else 0

        # Get a random blueprint.
        blueprint = self.world.get_blueprint_library().filter(args.filter)[0]
        blueprint.set_attribute('role_name', 'hero')
        if blueprint.has_attribute('color'):
            color = random.choice(blueprint.get_attribute('color').recommended_values)
            blueprint.set_attribute('color', color)

        # Spawn the player.
        if self.player is not None:
            spawn_point = self.player.get_transform()
            spawn_point.location.z += 2.0
            spawn_point.rotation.roll = 0.0
            spawn_point.rotation.pitch = 0.0
            self.destroy()
            self.player = self.world.try_spawn_actor(blueprint, spawn_point)
            self.modify_vehicle_physics(self.player)
        while self.player is None:
            if not self.map.get_spawn_points():
                print('There are no spawn points available in your map/town.')
                print('Please add some Vehicle Spawn Point to your UE4 scene.')
                sys.exit(1)
            # spawn_points = self.map.get_spawn_points()

            self.player_start_loction = carla.Location(x=-30.644844, y=24.471010, z=0.600000)
            spawn_point = carla.Transform(self.player_start_loction, carla.Rotation(pitch=0.000000, yaw=0.159198, roll=0.000000))
            # spawn_point = spawn_points[0]
            print("spawn player at " + str(spawn_point))
            # spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
            self.player = self.world.try_spawn_actor(blueprint, spawn_point)
            self.modify_vehicle_physics(self.player)


        if self._args.sync:
            self.world.tick()
        else:
            self.world.wait_for_tick()

        # Set up the sensors.
        self.collision_sensor = CollisionSensor(self.player)
        self.lane_invasion_sensor = LaneInvasionSensor(self.player)
        # self.gnss_sensor = GnssSensor(self.player)
        self.camera_manager = CameraManager(self.player, self._gamma)
        self.camera_manager.transform_index = cam_pos_id
        self.camera_manager.set_sensor(cam_index, notify=False)
        actor_type = get_actor_display_name(self.player)
        # self.hud.notification(actor_type)

    def next_weather(self, reverse=False):
        """Get next weather setting"""
        self._weather_index += -1 if reverse else 1
        self._weather_index %= len(self._weather_presets)
        preset = self._weather_presets[self._weather_index]
        # self.hud.notification('Weather: %s' % preset[1])
        self.player.get_world().set_weather(preset[0])

    def modify_vehicle_physics(self, actor):
        #If actor is not a vehicle, we cannot use the physics control
        try:
            physics_control = actor.get_physics_control()
            physics_control.use_sweep_wheel_collision = True
            actor.apply_physics_control(physics_control)
        except Exception:
            pass

    def on_world_tick(self, timestamp):

        # self.server_fps = self._server_clock.get_fps()
        self.frame = timestamp.frame
        # self.simulation_time = timestamp.elapsed_seconds

    def tick(self, clock):
        """Method for every tick"""
        # self.hud.tick(self, clock)

    def render(self, display):
        """Render world"""
        self.camera_manager.render(display)
        # self.hud.render(display)

    def destroy_sensors(self):
        """Destroy sensors"""
        self.camera_manager.sensor.destroy()
        self.camera_manager.sensor = None
        self.camera_manager.index = None

    def apply_control(self, throttle, steer, brake):
        self._control.throttle = throttle
        self._control.steer = steer
        self._control.brake = brake
        self._control.reverse = False
        self._control.hand_brake = False

        # 应用控制
        self.player.apply_control(self._control)

    def destroy(self):
        """Destroys all actors"""
        actors = [
            self.camera_manager.sensor,
            self.collision_sensor.sensor,
            self.lane_invasion_sensor.sensor,
            # self.gnss_sensor.sensor,
            self.player]
        for actor in actors:
            if actor is not None:
                actor.destroy()