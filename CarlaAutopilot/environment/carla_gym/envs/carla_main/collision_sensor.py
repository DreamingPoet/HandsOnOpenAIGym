#!/usr/bin/env python

# ==============================================================================
# -- CollisionSensor -----------------------------------------------------------
# ==============================================================================

import collections
import math
import weakref
import carla

from environment.carla_gym.envs.carla_main.util import *

class CollisionSensor(object):
    def __init__(self, parent_actor):
        self.sensor = None
        self.history = []
        self._parent = parent_actor
        self.collision_frame = 0
        self.collision_vehicle = 0
        self.collision_walker = 0
        self.collision_actor = 0
        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.other.collision')
        self.sensor = world.spawn_actor(bp, carla.Transform(), attach_to=self._parent)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: CollisionSensor._on_collision(weak_self, event))

    def get_collision(self, frame):
        if frame == self.collision_frame:
            return (
                self.collision_vehicle,
                self.collision_walker,
                self.collision_actor
            )
        return (0,0,0)

    def get_collision_history(self):
        history = collections.defaultdict(int)
        for frame, intensity in self.history:
            history[frame] += intensity
        return history

    @staticmethod
    def _on_collision(weak_self, event):
        self = weak_self()
        if not self:
            return


        if self.collision_frame != event.frame:
            self.collision_frame = event.frame
            self.collision_vehicle = 0
            self.collision_walker = 0
            self.collision_actor = 0
        
        # print(type(event.other_actor))
        if isinstance(event.other_actor, carla.Vehicle):
            # print('Collision with Vehicle')
            self.collision_vehicle =  self.collision_vehicle + 1
        elif isinstance(event.other_actor, carla.Walker):
            # print('Collision with Walker')
            self.collision_walker =  self.collision_walker + 1
        elif isinstance(event.other_actor, carla.Actor):
            # print('Collision with Actor')
            self.collision_actor =  self.collision_actor + 1

        # actor_name = get_actor_display_name(event.other_actor)
        
        # self.hud.notification('Collision with %r' % actor_name)
        # impulse = event.normal_impulse
        # intensity = math.sqrt(impulse.x**2 + impulse.y**2 + impulse.z**2)
        # self.history.append((event.frame, intensity))

        if len(self.history) > 400:
            self.history.pop(0)