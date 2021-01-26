SECONDS_IN_MINUTE = 60
MAX_SECONDS = 5400
MIN_SECONDS = 0


class MicrowaveBase:
    def __init__(self):
        self.time = 0

    @staticmethod
    def _check_time(time):
        if time > MAX_SECONDS:
            time = MAX_SECONDS
        elif time < MIN_SECONDS:
            time = MIN_SECONDS
        return time

    @staticmethod
    def convert_to_seconds(time):
        if time[-1] == 's':
            return int(time[:-1])
        elif time[-1] == 'm':
            return int(time[:-1])*SECONDS_IN_MINUTE

    @staticmethod
    def convert_to_output(time):
        minutes = str(time // SECONDS_IN_MINUTE).rjust(2, '0')
        seconds = str(time % SECONDS_IN_MINUTE).rjust(2, '0')
        return minutes + ':' + seconds

    def set_time(self, time):
        min_sec = time.split(':')
        self.time = self._check_time(self.convert_to_seconds(min_sec[0]+'m') + self.convert_to_seconds(min_sec[1]+'s'))

    def add_time(self, time):
        self.time = self._check_time(self.time + self.convert_to_seconds(time))

    def del_time(self, time):
        self.time = self._check_time(self.time - self.convert_to_seconds(time))

    def show_time(self):
        raise NotImplementedError


class Microwave1(MicrowaveBase):

    def show_time(self):
        return '_' + self.convert_to_output(self.time)[1:]


class Microwave2(MicrowaveBase):

    def show_time(self):
        return self.convert_to_output(self.time)[:-1] + '_'


class Microwave3(MicrowaveBase):

    def show_time(self):
        return self.convert_to_output(self.time)


class RemoteControl:
    def __init__(self, device):
        self.device = device

    def set_time(self, time):
        self.device.set_time(time)

    def add_time(self, time):
        self.device.add_time(time)

    def del_time(self, time):
        self.device.del_time(time)

    def show_time(self):
       return self.device.show_time()


microwave_1 = Microwave1()
microwave_2 = Microwave2()
microwave_3 = Microwave3()

remote_control_1 = RemoteControl(microwave_1)
remote_control_1.set_time("01:00")

remote_control_2 = RemoteControl(microwave_2)
remote_control_2.add_time("90s")

remote_control_3 = RemoteControl(microwave_3)
remote_control_3.del_time("300s")
remote_control_3.add_time("100s")

print(remote_control_1.show_time()) #== "_1:00"
print(remote_control_2.show_time()) # == "01:3_"
print(remote_control_3.show_time()) #== "01:40"
