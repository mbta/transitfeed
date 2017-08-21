#!/usr/bin/python2.5

# Copyright (C) 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from gtfsobjectbase import GtfsObjectBase
import problems as problems_module
import util

class Transfer(GtfsObjectBase):
  """Represents a transfer in a schedule"""
  _REQUIRED_FIELD_NAMES = ['from_stop_id', 'to_stop_id', 'transfer_type']
  _FIELD_NAMES = _REQUIRED_FIELD_NAMES + ['min_transfer_time', 'min_walk_time', 'min_wheelchair_time', 'suggested_buffer_time', 'wheelchair_transfer']
  _TABLE_NAME = 'transfers'
  _ID_COLUMNS = ['from_stop_id', 'to_stop_id']

  def __init__(self, schedule=None, from_stop_id=None, to_stop_id=None, transfer_type=None,
               min_transfer_time=None, min_walk_time=None, min_wheelchair_time=None,
               suggested_buffer_time=None, wheelchair_transfer=None, field_dict=None):
    self._schedule = None
    if field_dict:
      self.__dict__.update(field_dict)
    else:
      self.from_stop_id = from_stop_id
      self.to_stop_id = to_stop_id
      self.transfer_type = transfer_type
      self.min_transfer_time = min_transfer_time
      self.min_walk_time = min_walk_time
      self.min_wheelchair_time = min_wheelchair_time
      self.suggested_buffer_time = suggested_buffer_time
      self.wheelchair_transfer = wheelchair_transfer

    if getattr(self, 'transfer_type', None) in ("", None):
      # Use the default, recommended transfer, if attribute is not set or blank
      self.transfer_type = 0
    else:
      try:
        self.transfer_type = util.NonNegIntStringToInt(self.transfer_type)
      except (TypeError, ValueError):
        pass

    if hasattr(self, 'min_transfer_time'):
      try:
        self.min_transfer_time = util.NonNegIntStringToInt(self.min_transfer_time)
      except (TypeError, ValueError):
        pass
    else:
      self.min_transfer_time = None

    if hasattr(self, 'min_walk_time'):
      try:
        self.min_walk_time = util.NonNegIntStringToInt(self.min_walk_time)
      except (TypeError, ValueError):
        pass
    else:
      self.min_walk_time = None

    if hasattr(self, 'min_wheelchair_time'):
      try:
        self.min_wheelchair_time = util.NonNegIntStringToInt(self.min_wheelchair_time)
      except (TypeError, ValueError):
        pass
    else:
      self.min_wheelchair_time = None

    if hasattr(self, 'suggested_buffer_time'):
      try:
        self.suggested_buffer_time = util.NonNegIntStringToInt(self.suggested_buffer_time)
      except (TypeError, ValueError):
        pass
    else:
      self.suggested_buffer_time = None

    if hasattr(self, 'wheelchair_transfer'):
      try:
        self.wheelchair_transfer = util.NonNegIntStringToInt(self.wheelchair_transfer)
      except (TypeError, ValueError):
        pass
    else:
      self.wheelchair_transfer = None

    if schedule is not None:
      # Note from Tom, Nov 25, 2009: Maybe calling __init__ with a schedule
      # should output a DeprecationWarning. A schedule factory probably won't
      # use it and other GenericGTFSObject subclasses don't support it.
      schedule.AddTransferObject(self)

  def ValidateFromStopIdIsPresent(self, problems):
    if util.IsEmpty(self.from_stop_id):
      problems.MissingValue('from_stop_id')
      return False
    return True

  def ValidateToStopIdIsPresent(self, problems):
    if util.IsEmpty(self.to_stop_id):
      problems.MissingValue('to_stop_id')
      return False
    return True

  def ValidateTransferType(self, problems):
    if not util.IsEmpty(self.transfer_type):
      if (not isinstance(self.transfer_type, int)) or \
          (self.transfer_type not in range(0, 4)):
        problems.InvalidValue('transfer_type', self.transfer_type)
        return False
    return True

  def ValidateMinimumTransferTime(self, problems):
    if not util.IsEmpty(self.min_transfer_time):
      if self.transfer_type != 2:
        problems.MinimumTransferTimeSetWithInvalidTransferType(
            self.transfer_type)

      # If min_transfer_time is negative, equal to or bigger than 24h, issue
      # an error. If smaller than 24h but bigger than 3h issue a warning.
      # These errors are not blocking, and should not prevent the transfer
      # from being added to the schedule.
      if (isinstance(self.min_transfer_time, int)):
        if self.min_transfer_time < 0:
          problems.InvalidValue('min_transfer_time', self.min_transfer_time,
                                reason="This field cannot contain a negative " \
                                       "value.")
        elif self.min_transfer_time >= 24*3600:
          problems.InvalidValue('min_transfer_time', self.min_transfer_time,
                                reason="The value is very large for a " \
                                       "transfer time and most likely " \
                                       "indicates an error.")
        elif self.min_transfer_time >= 3*3600:
          problems.InvalidValue('min_transfer_time', self.min_transfer_time,
                                type=problems_module.TYPE_WARNING,
                                reason="The value is large for a transfer " \
                                       "time and most likely indicates " \
                                       "an error.")
      else:
        # It has a value, but it is not an integer
        problems.InvalidValue('min_transfer_time', self.min_transfer_time,
                              reason="If present, this field should contain " \
                                "an integer value.")
        return False
    elif self.transfer_type == 2:
    	problems.InvalidValue('min_transfer_time', self.min_transfer_time,
                              reason="This field must be filled when " \
                                "transfer_type == 2.")
    return True

  def ValidateMinimumWalkTime(self, problems):
    if not util.IsEmpty(self.min_walk_time):
      if self.transfer_type != 2:
        problems.MinimumTransferTimeSetWithInvalidTransferType(
            self.transfer_type)

      # If min_transfer_time is negative, equal to or bigger than 24h, issue
      # an error. If smaller than 24h but bigger than 3h issue a warning.
      # These errors are not blocking, and should not prevent the transfer
      # from being added to the schedule.
      if (isinstance(self.min_walk_time, int)):
        if self.min_walk_time < 0:
          problems.InvalidValue('min_walk_time', self.min_walk_time,
                                reason="This field cannot contain a negative " \
                                       "value.")
        elif self.min_walk_time >= 24*3600:
          problems.InvalidValue('min_walk_time', self.min_walk_time,
                                reason="The value is very large for a " \
                                       "transfer time and most likely " \
                                       "indicates an error.")
        elif self.min_walk_time >= 3*3600:
          problems.InvalidValue('min_walk_time', self.min_walk_time,
                                type=problems_module.TYPE_WARNING,
                                reason="The value is large for a transfer " \
                                       "time and most likely indicates " \
                                       "an error.")
        else:
          problems.InvalidValue('min_walk_time', self.min_walk_time,
                                reason="This field cannot contain a negative " \
                                       "value.")
      else:
        # It has a value, but it is not an integer
        problems.InvalidValue('min_walk_time', self.min_walk_time,
                              reason="If present, this field should contain " \
                                "an integer value.")
        return False
    elif self.transfer_type == 2:
    	problems.InvalidValue('min_walk_time', self.min_walk_time,
                              reason="This field must be filled when " \
                                "transfer_type == 2.")
    return True

  def ValidateMinimumWheelchairTime(self, problems):
    if not util.IsEmpty(self.min_wheelchair_time):
      if self.transfer_type != 2:
        problems.MinimumTransferTimeSetWithInvalidTransferType(
            self.transfer_type)

      # If min_transfer_time is negative, equal to or bigger than 24h, issue
      # an error. If smaller than 24h but bigger than 3h issue a warning.
      # These errors are not blocking, and should not prevent the transfer
      # from being added to the schedule.
      if (isinstance(self.min_wheelchair_time, int)):
      	if self.wheelchair_transfer == 2:
      	  problems.InvalidValue('min_wheelchair_time', self.min_wheelchair_time,
                                reason="This field cannot be filled when " \
                                       "wheelchair_transfer == 2.")
        elif self.min_wheelchair_time < 0:
          problems.InvalidValue('min_wheelchair_time', self.min_wheelchair_time,
                                reason="This field cannot contain a negative " \
                                       "value.")
        elif self.min_wheelchair_time >= 24*3600:
          problems.InvalidValue('min_wheelchair_time', self.min_wheelchair_time,
                                reason="The value is very large for a " \
                                       "transfer time and most likely " \
                                       "indicates an error.")
        elif self.min_wheelchair_time >= 3*3600:
          problems.InvalidValue('min_wheelchair_time', self.min_wheelchair_time,
                                type=problems_module.TYPE_WARNING,
                                reason="The value is large for a transfer " \
                                       "time and most likely indicates " \
                                       "an error.")
        else:
          problems.InvalidValue('min_wheelchair_time', self.min_wheelchair_time,
                                reason="This field cannot contain a negative " \
                                       "value.")
      else:
        # It has a value, but it is not an integer
        problems.InvalidValue('min_wheelchair_time', self.min_wheelchair_time,
                              reason="If present, this field should contain " \
                                "an integer value.")
        return False
    elif self.wheelchair_transfer == 1 and self.transfer_type == 2:
    	problems.InvalidValue('min_wheelchair_time', self.min_wheelchair_time,
                              reason="This field must be filled when " \
                                "wheelchair_transfer == 1 and " \
                                "transfer_type == 2.")
    return True

  def ValidateSuggestedBufferTime(self, problems):
    if not util.IsEmpty(self.suggested_buffer_time):
      if self.transfer_type != 2:
        problems.MinimumTransferTimeSetWithInvalidTransferType(
            self.transfer_type)

      # If min_transfer_time is negative, equal to or bigger than 24h, issue
      # an error. If smaller than 24h but bigger than 3h issue a warning.
      # These errors are not blocking, and should not prevent the transfer
      # from being added to the schedule.
      if (isinstance(self.suggested_buffer_time, int)):
        if self.suggested_buffer_time < 0:
          problems.InvalidValue('suggested_buffer_time', self.suggested_buffer_time,
                                reason="This field cannot contain a negative " \
                                       "value.")
        elif self.suggested_buffer_time >= 24*3600:
          problems.InvalidValue('suggested_buffer_time', self.suggested_buffer_time,
                                reason="The value is very large for a " \
                                       "transfer time and most likely " \
                                       "indicates an error.")
        elif self.suggested_buffer_time >= 3*3600:
          problems.InvalidValue('suggested_buffer_time', self.suggested_buffer_time,
                                type=problems_module.TYPE_WARNING,
                                reason="The value is large for a transfer " \
                                       "time and most likely indicates " \
                                       "an error.")
        else:
          problems.InvalidValue('suggested_buffer_time', self.suggested_buffer_time,
                                reason="This field cannot contain a negative " \
                                       "value.")
      else:
        # It has a value, but it is not an integer
        problems.InvalidValue('suggested_buffer_time', self.suggested_buffer_time,
                              reason="If present, this field should contain " \
                                "an integer value.")
        return False
    return True

  def GetTransferDistance(self):
    from_stop = self._schedule.stops[self.from_stop_id]
    to_stop = self._schedule.stops[self.to_stop_id]
    distance = util.ApproximateDistanceBetweenStops(from_stop, to_stop)
    return distance

  def ValidateFromStopIdIsValid(self, problems):
    if self.from_stop_id not in self._schedule.stops.keys():
      problems.InvalidValue('from_stop_id', self.from_stop_id)
      return False
    return True

  def ValidateToStopIdIsValid(self, problems):
    if self.to_stop_id not in self._schedule.stops.keys():
      problems.InvalidValue('to_stop_id', self.to_stop_id)
      return False
    return True

  def ValidateTransferDistance(self, problems):
    distance = self.GetTransferDistance()

    # MBTA-jfabi change: change error condition from 10'000m to 1'000m
    if distance > 1000:
      problems.TransferDistanceTooBig(self.from_stop_id,
                                      self.to_stop_id,
                                      distance)
    # MBTA-jfabi change: change warning condition from 2'000m to 200m
    elif distance > 200:
      problems.TransferDistanceTooBig(self.from_stop_id,
                                      self.to_stop_id,
                                      distance,
                                      type=problems_module.TYPE_WARNING)

  def ValidateTransferWalkingTime(self, problems):
    if util.IsEmpty(self.min_transfer_time):
      return

    if self.min_transfer_time < 0:
      # Error has already been reported, and it does not make sense
      # to calculate walking speed with negative times.
      return

    distance = self.GetTransferDistance()
    # If min_transfer_time + 120s isn't enough for someone walking very fast
    # (2m/s) then issue a warning.
    #
    # Stops that are close together (less than 240m appart) never trigger this
    # warning, regardless of min_transfer_time.
    FAST_WALKING_SPEED= 2 # 2m/s
    if self.min_transfer_time + 120 < distance / FAST_WALKING_SPEED:
      problems.TransferWalkingSpeedTooFast(from_stop_id=self.from_stop_id,
                                           to_stop_id=self.to_stop_id,
                                           transfer_time=self.min_transfer_time,
                                           distance=distance)

  def ValidateBeforeAdd(self, problems):
    result = True
    result = self.ValidateFromStopIdIsPresent(problems) and result
    result = self.ValidateToStopIdIsPresent(problems) and result
    result = self.ValidateTransferType(problems) and result
    result = self.ValidateMinimumTransferTime(problems) and result
    result = self.ValidateMinimumWalkTime(problems) and result
    result = self.ValidateMinimumWheelchairTime(problems) and result
    result = self.ValidateSuggestedBufferTime(problems) and result
    return result

  def ValidateAfterAdd(self, problems):
    valid_stop_ids = True
    valid_stop_ids = self.ValidateFromStopIdIsValid(problems) and valid_stop_ids
    valid_stop_ids = self.ValidateToStopIdIsValid(problems) and valid_stop_ids
    # We need both stop IDs to be valid to able to validate their distance and
    # the walking time between them
    if valid_stop_ids:
      self.ValidateTransferDistance(problems)
      self.ValidateTransferWalkingTime(problems)

  def Validate(self,
               problems=problems_module.default_problem_reporter):
    if self.ValidateBeforeAdd(problems) and self._schedule:
      self.ValidateAfterAdd(problems)

  def _ID(self):
    return tuple(self[i] for i in self._ID_COLUMNS)

  def AddToSchedule(self, schedule, problems):
    schedule.AddTransferObject(self, problems)
