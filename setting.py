# 窗口大小，单位：像素
RESOLUTION = 700
FPS=20

# 种子
SEED = 110
# 世界的坐标系大小，单位：格/单位时间
WORLD_SIZE = 100
# 人数的多少
POP_SIZE = 1000
# 去往聚集区的概率
VISIT_CHANCE = 0
# 在聚集区呆的时间
VISIT_DURATION = 1 * FPS
# 每个人的行走速度
WALK_SPEED = WORLD_SIZE*.1


# 界面的背景颜色
BACKGROUND_COLOR = (200, 200, 200)

# 距离病人多少距离内有几率感染，单位：格
INFECTION_RADIUS = WORLD_SIZE*.04
# 接触病人后，有多少的几率被感染
INFECTION_CHANCE = .12
# 暂时无用，开启关闭隔离
QUARANTINE_FACTOR = 1
# 被发现并隔离的几率
QUARANTINE_CHANCE = 1
# 感染几天后才被隔离
QUARANTINE_INTERVAL = 4 * FPS


# 待在集中区被感染的概率
def visit_infected_chance(indicator):
    if sum(indicator) > 0:
        return INFECTION_CHANCE + (1 - INFECTION_CHANCE) * sum(indicator) / 6
    else:
        return 0