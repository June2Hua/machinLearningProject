"""
服务站示例
场景介绍:
  一个有特定服务提供工作站，客户服务时长不一，工作机器数有限。
  Client接受服务步骤：Client到达工作站，若有空闲的机器就立刻接受服务，如果没有，就等待直到其他机器空闲下来。
  每个接受过服务的Client都有一个完成满意度（或者为进度）实时统计服务客户数和完成满意进度。
"""
import random
import simpy

# 可接受输入参数
RANDOM_SEED = 0         # 不设置
NUM_MACHINES = 2        # 可以同时处理的机器数（类似工作工位数）
TIME_CONSUMING = 5      # 单任务耗时 (可以设计成随机数)
TIME_INTERVAL = 5       # 来车的间隔时间约5分钟   (可以设计成随机数)
SIM_TIME = 1000         # 仿真总时间
CLIENT_NUMBER = 2       # 初始时已经占用机器数


class WorkStation(object):
    """
    一个工作站，拥有特定数量的机器数。 一个客户首先申请服务。在对应服务时间完成后结束并离开工作站
    """
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime
        self.allClient = 0
        self.accomplishClient = 0

    def wash(self, car):
        """服务流程"""
        yield self.env.timeout(random.randint(2, 10))  # 假设服务时间为随机数（2~10）
        self.allClient += 1
        per = random.randint(50, 99)
        print("%s's 任务完成度：%d%%." % (car, per))
        if per > 80:
            self.accomplishClient += 1

        print("工作站服务客户数：%d,"
              "工作站服务达标率：%.2f。" % (self.allClient, float(self.accomplishClient) / float(self.allClient)))


def Client(env, name, cw):
    """
    客户到达动作站接受服务，结束后离开
    """

    print('%s 到达工作站 at %.2f.' % (name, env.now))
    with cw.machine.request() as request:
        yield request
        print('%s 接受服务   at %.2f.' % (name, env.now))
        yield env.process(cw.wash(name))
        print('%s 离开服务站 at %.2f.' % (name, env.now))


def setup(env, num_machines, washtime, t_inter, clientNumber):
    """创建一个工作站，几个初始客户，然后持续有客户到达. 每隔t_inter - 2, t_inter + 3分钟（可以自定义）."""
    # 创建工作站
    workstation = WorkStation(env, num_machines, washtime)

    # 创建clientNumber个初始客户
    for i in range(clientNumber):
        env.process(Client(env, 'Client_%d' % i, workstation))

    # 在仿真过程中持续创建客户
    while True:
        yield env.timeout(random.randint(t_inter - 2, t_inter + 3))  # 3-8分钟
        i += 1
        env.process(Client(env, 'Client_%d' % i, workstation))


# 初始化并开始仿真任务
print('开始仿真')

# 初始化seed，指定数值的时候方正结果可以复现
random.seed()

# 创建一个环境并开始仿真
env = simpy.Environment()
env.process(setup(env, NUM_MACHINES, TIME_CONSUMING, TIME_INTERVAL, CLIENT_NUMBER))

# 开始执行!
env.run(until=SIM_TIME)

