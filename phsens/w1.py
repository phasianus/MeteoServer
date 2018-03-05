from phsens.sensors import Sensor

class KSensor(Sensor):
    
    def __init__ (self,sensor_id):
        self.id=sensor_id

    def open(self,data):
        return open("/sys/bus/w1/devices/%s/%s"  % (self.id,data), "r")

    def r(self, data):
        return self.open(data).readline()

    def o(self, data=()):
        pass
    
        

class Ds2438(KSensor):
    
    def temperature(self):
        return float(self.r("temperature")) / 256

    def vad(self):
        return float(self.r("vad")) / 100

    def vdd(self):
        return float(self.r("vdd")) / 100
    
    def measure(self):
        return self.temperature() 


class Hih50x(Ds2438):

    def humidity(self):
        """
        see: https://sensing.honeywell.com/index.php?ci_id=49692
	    """
        i = self.vdd()
        return (self.vad() - (.1515 * i)) / (.00636 * i * (1.0546 - .00216 * self.temperature()))
    
        #	return (self.vad() / self.vdd() - 0.16) / 0.0062 / (1.0546 - 0.00216 * self.temperature())

    def measure(self):
        return self.humidity()

class Ds18b20(KSensor):

    def temperature(self):
        f = self.open("w1_slave")
        if (f.readline().strip()[-3:] != 'YES'):
            return None
        return float(f.readline().split("t=")[1])/1000
    
    def measure(self):
        return self.temperature()c