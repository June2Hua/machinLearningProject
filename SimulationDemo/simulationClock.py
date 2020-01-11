import simpy


# define the clock
def clock(env, name, tick):
    while True:
        print(name, env.now)
        yield env.timeout(tick)


env = simpy.Environment()
env.process(clock(env, "fast", 0.5))
env.process(clock(env, "slow", 1))
env.run(until=6.01)