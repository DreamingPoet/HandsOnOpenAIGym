#!/usr/bin/env python

import weakref
import carla

# ==============================================================================
# -- LaneInvasionSensor --------------------------------------------------------
# ==============================================================================


class LaneInvasionSensor(object):
    def __init__(self, parent_actor):
        self.sensor = None
        self.lane_frame = 0
        self.intersection_otherlane = 0 # 压到其他车道
        self.intersection_offroad = 0 # 偏离机动车道

        # If the spawn object is not a vehicle, we cannot use the Lane Invasion Sensor
        if parent_actor.type_id.startswith("vehicle."):
            self._parent = parent_actor
            # self.hud = hud
            world = self._parent.get_world()
            bp = world.get_blueprint_library().find('sensor.other.lane_invasion')
            self.sensor = world.spawn_actor(bp, carla.Transform(), attach_to=self._parent)
            # We need to pass the lambda a weak reference to self to avoid circular
            # reference.
            weak_self = weakref.ref(self)
            self.sensor.listen(lambda event: LaneInvasionSensor._on_invasion(weak_self, event))

    def lane_check(self, frame):
        if frame == self.lane_frame:
            return (
                self.intersection_otherlane,
                self.intersection_offroad
            )
        return (0,0)


    @staticmethod
    def _on_invasion(weak_self, event):
        self = weak_self()
        if not self:
            return

        print("lane_check")
        lane_types = set()

        if self.lane_frame != event.frame:
            self.lane_frame = event.frame
            self.intersection_otherlane = 0
            self.intersection_offroad = 0
            
        for x in event.crossed_lane_markings:
            lane_types.add(x.type)
            x = str(x.type)
            if x == 'None'or x == 'Solid':
                self.intersection_offroad =  self.intersection_offroad + 1
            else :
                self.intersection_otherlane =  self.intersection_otherlane + 1

        # lane_types = set(x.type for x in event.crossed_lane_markings)
        # text = ['%r' % str(x).split()[-1] for x in lane_types]
        # print(text)
        # self.hud.notification('Crossed line %s' % ' and '.join(text))