# 窗口大小，单位：像素
RESOLUTION = 700
BIN_X = 50
BIN_Y = 50
assert RESOLUTION % BIN_X == 0
FPS=20 # 每单位时间

# 种子
SEED = 110
# 世界的坐标系大小，单位：格/单位时间
WORLD_SIZE = 50
# 人数的多少
POP_SIZE = 500
# 去往聚集区的概率
VISIT_CHANCE = 0
# 在聚集区呆的时间
VISIT_DURATION = 1
# 每个人的行走速度
WALK_SPEED = WORLD_SIZE*.07
# 每个人是否保持社交距离，应为0到1的值，0为不，0.5表示有一半的人遵守
KEEP_DIST = 0
# 初始时有多少比例的人口感染
INITIAL_CHANCE = .01

# 是否进行更改社交距离的测试
KEEP_DIST_CHANGE = True
KEEP_DIST_CHANGE_TIME = 0
# 是否进行复工测试
BACK_TO_WORK = True


# 界面的背景颜色
BACKGROUND_COLOR = (200, 200, 200)

RADIUS_FACTOR = .025
# 距离病人多少距离内有几率感染，单位：格
INFECTION_RADIUS = int(RESOLUTION * RADIUS_FACTOR)
# INFECTION_RADIUS = 1
# 接触病人后，有多少的几率被感染
INFECTION_CHANCE = .2
# 暂时无用，开启关闭隔离
QUARANTINE_FACTOR = 1
# 被发现并隔离的几率
QUARANTINE_CHANCE = .8
# 感染几天后才被隔离
QUARANTINE_INTERVAL = 7

PI = 3.1416



# 待在集中区被感染的概率
def visit_infected_chance(indicator):
    if sum(indicator) > 0:
        res = INFECTION_CHANCE + (1 - INFECTION_CHANCE) * sum(indicator) / 6
        return round(res, 2)
    else:
        return 0