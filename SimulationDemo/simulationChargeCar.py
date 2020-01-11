from random import seed, randint
import simpy

'''
    充电桩，仅考虑一辆车，一个充电桩
'''
class EVSE(object):
    def __init__(self, env):
        self.env = env
        self.EVSE_reactive = env.event()    # 激活充电桩事件
        self.EVSE_stop = env.event()        # 停止充电桩事件

    def drive(self):
        while True:
            print("car start:", (self.env.now))
            yield self.env.timeout(randint(30, 60))     # 开车中
            print("car stop: ", (self.env.now))
            self.EVSE_reactive.succeed()                # 开车完成
            self.EVSE_reactive = self.env.event()       # 激活充电桩充电
            yield self.env.timeout(randint(30, 50)) & self.EVSE_stop        # 车主回来并且充好电
            print("car over****", self.env.now)

    def charge(self):
        while True:
            print("EVSE is free:", (self.env.now))
            yield self.EVSE_reactive                    # 等待充电桩被激活
            print("start charging ", (self.env.now))
            yield self.env.timeout(randint(10, 30))     # 等待充电桩完成充电
            self.EVSE_stop.succeed()                    # 完成充电
            self.EVSE_stop = self.env.event()
            print("charge over****", self.env.now)



def main():
    env = simpy.Environment()
    evse = EVSE(env)
    env.process(evse.drive())
    env.process(evse.charge())
    env.run(until=1000)


if __name__ == '__main__':
    main()