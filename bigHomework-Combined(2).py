import random
import numpy
import json
def StandardMode_to_CountingMode(standard_list):
    counted_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(13):
        counted_list[i] = sum([(1 if 4*i+j in standard_list else 0) for j in range(4)])
    if 52 in standard_list: counted_list[-2] = 1
    if 53 in standard_list: counted_list[-1] = 1
    return counted_list


def king_analyse(counted_list):
    return counted_list[13:]


def bomb_analyse(counted_list):
    count = 0
    bomb_list = []

    if king_analyse(counted_list) == [1, 1]:
        count += 1
        bomb_list.append(13)
    for j in range(13):
        if counted_list[j] == 4:
            count += 1
            bomb_list.append(j)

    if count == 0: return [0,[]]
    else: return [count, bomb_list]


def aeroplane_analyse(counted_list):
    for j in range(12):
        if counted_list[j] == 4 and counted_list[j+1] == 4:
            return 1
    return 0


def plane_analyse(counted_list):
    count = 0
    j = 0
    plane_set = set()
    while j < 11:
        if counted_list[j] >= 3 and counted_list[j+1] >= 3:
            count += 1
            plane_set.add(j)
            plane_set.add(j+1)
        j += 1
    plane_list = list(plane_set)
    plane_list.sort()
    if count == 0: return [0,[]]
    return [1, plane_list]


def dragon_analyse(counted_list1):
    counted_list=counted_list1.copy()
    most_lists = []
    dragon_len = 0
    longest = []
    for i in range(13):       # 不能有2（index从0到11）
        if counted_list[i] <= 0 or i == 12:
            if dragon_len >= 5:     # 最少5张牌才能形成龙
                if (not longest) or dragon_len > longest[1]-longest[0]+1:     # 更新最长:
                    longest = [i-dragon_len, i-1]
            dragon_len = 0
        else:
            dragon_len += 1
    if longest:
        dragon_len = 0
        go_on = True        # 循环终止标记；如果循环一轮一条龙都没找到就不再寻找
        while go_on:
            go_on = False
            merged = False
            for i in range(11, -2, -1):     # 从后往前
                if dragon_len == 5:     # 已经形成龙（这种断开方法会让小的龙更长，因为残缺的龙会接在小龙的后面）
                    most_lists.append([i+1, i+5])
                    go_on = True
                    dragon_len = 0
                    break
                elif dragon_len > 0 and (counted_list[i] <= 0 or i == -1):      # 没能形成龙就断了
                    for j in range(len(most_lists)):
                        if i+dragon_len >= most_lists[j][0]-1 >= i+1:   # 若能，接到某一条龙的后面(有交集即可)
                            for k in range(most_lists[j][0], i + dragon_len + 1):  # 没用上的加回来
                                counted_list[k] += 1
                            most_lists[j][0] = i+1
                            go_on = True
                            merged = True
                            break
                    if not merged:
                        for k in range(i+1, i+dragon_len+1):    # 没用上, 加回来
                            counted_list[k] += 1
                    dragon_len = 0
                    merged = False
                elif counted_list[i] > 0 and i != -1:       # 还在接龙， 一个个减一
                    dragon_len += 1
                    counted_list[i] -= 1

    most_lists.reverse()
    if not longest:
        return [0,[],[]]
    else:
        return [len(most_lists), most_lists, longest]


def double_dragon_analyse(counted_list1):
    counted_list=counted_list1.copy()
    most_lists = []
    dragon_len = 0
    longest = []
    for i in range(13):       # 不能有2（index从0到11）
        if counted_list[i] <= 1 or i == 12:
            if dragon_len >= 3:     # 最少3对牌才能形成龙
                if (not longest) or dragon_len > longest[1]-longest[0]+1:   # 更新最长
                    longest = [i-dragon_len, i-1]
            dragon_len = 0
        else:
            dragon_len += 1

    if longest:
        dragon_len = 0
        go_on = True        # 循环终止标记；如果循环一轮一条龙都没找到就不再寻找
        merged = False
        while go_on:
            go_on = False
            for i in range(11, -2, -1):     # 从后往前
                if dragon_len == 3:     # 已经形成龙（这种断开方法会让小的龙更长，因为残缺的龙会接在小龙的后面）
                    most_lists.append([i+1, i+3])
                    go_on = True
                    dragon_len = 0
                    break
                elif dragon_len > 0 and (counted_list[i] <= 1 or i == -1):  # 没能形成龙就断了
                    for j in range(len(most_lists)):
                        if i + dragon_len >= most_lists[j][0] - 1 >= i + 1:  # 若能，接到某一条龙的后面 (刚好接上/有交集)
                            for k in range(most_lists[j][0], i + dragon_len + 1):  # 没用上的加回来
                                counted_list[k] += 1
                            most_lists[j][0] = i + 1
                            go_on = True
                            merged = True
                            break
                    if not merged:
                        for k in range(i + 1, i + dragon_len + 1):  # 没用上, 加回来
                            counted_list[k] += 1
                    dragon_len = 0
                    merged = False
                elif counted_list[i] > 1 and i != -1:       # 还在接龙， 一个个减二
                    dragon_len += 1
                    counted_list[i] -= 2

    most_lists.reverse()
    if not longest:
        return [0,[],[]]
    else:
        return [len(most_lists), most_lists, longest]


def triplet_analyse(counted_list):
    tri = []
    for i in range(15):
        if counted_list[i] >= 3:
            tri.append(i)
    return tri


def pair_analyse(counted_list):
    pair = []
    tmp = 0
    for i in range(11):     # 在3到J里面找
        if counted_list[i] == 2:
            tmp += 1
        elif tmp < 3:       # 没有达到连续三个对子，即不是双龙
            for x in range(i-tmp, i):
                pair.append(x)
            tmp = 0
    if counted_list[12] == 2:       # 两张2一定构成孤对
        pair.append(12)
    return pair


def single_analyse(counted_list):
    single_list = []
    if counted_list[13] == 1: single_list.append(13)
    if counted_list[14] == 1: single_list.append(14)
    have_set = set(j for j in range(13) if counted_list[j] >= 1)
    one_set = set(j for j in range(13) if counted_list[j] == 1)
    #print('Debugging have_set:',have_set)
    for j in one_set:
        lst = [{j-4+k, j-3+k, j-2+k, j-1+k, j+k}.issubset(have_set) for k in range(5)]
        if True not in lst:
            single_list.append(j)
    single_list.sort()
    return single_list


def check_type(standard_list):
    l = len(standard_list)
    count_mode = StandardMode_to_CountingMode(standard_list)

    if l == 0:      # 过
        return 0
    if l == 1:    # 单
        return 1
    if l == 2:    # 对子/王炸（火箭）
        if 2 in count_mode:
            return 2
        else:
            return 17
    if l == 3:      # 三张
        return 3
    if l == 4:      # 炸弹/三带一
        if 4 in count_mode:
            return 6
        else:
            return 4
    if l == 5:      # 三带二/单顺（龙）
        if 3 in count_mode:
            return 5
        else:
            return 9
    if l == 6:      # 四带二单/飞机不带翼/双顺/单顺
        if 4 in count_mode:
            return 7
        elif 3 in count_mode:
            return 11
        elif 2 in count_mode:
            return 10
        else:
            return 9
    if l == 7:  # 单顺
        return 9
    if l == 8:      # 航天飞机不带翼/四带二对/飞机带小翼/双顺/单顺
        if 4 in count_mode:     # 四带二对/航飞无翼
            if 2 in count_mode:
                return 8
            else:
                return 14
        elif 3 in count_mode:   # 飞机带小翼
            return 12
        elif 2 in count_mode:   # 双顺
            return 10
        else:                   # 单顺
            return 9
    if l == 9:      # 飞机无翼/单顺
        if 3 in count_mode:
            return 11
        else:
            return 9
    if l == 10:     # 飞机带大翼/双顺/单顺
        if 3 in count_mode:
            return 16
        elif 2 in count_mode:
            return 10
        else:
            return 9
    if l == 11:     # 单顺
        return 9
    if l == 12:
        if 4 in count_mode:     # 航飞带小翼/航飞不带翼
            if 1 in count_mode:
                return 15
            else:
                return 14
        elif 3 in count_mode:   # 飞机带小翼/飞机不带翼
            if 1 in count_mode:
                return 12
            else:
                return 11
        elif 2 in count_mode:   # 双顺
            return 10
        else:
            return 9
    if l == 14:     # 双顺
        return 10
    if l == 15:     # 飞机带大翼/飞机无翼
        if 2 in count_mode:
            return 13
        else:
            return 11
    if l == 16:
        if 4 in count_mode:     # 航飞带大翼/航飞无翼
            if 2 in count_mode:
                return 16
            else:
                return 11
        elif 3 in count_mode:   # 飞机带小翼
            return 12
        else:       # 双顺
            return 10
    if l >= 17:
        return 20


def Pre_Judgement(standard_list):
    '''第一个位置是类型的编号，最后一个位置可能是“炸弹返回值”，中间是特征的输出'''
    Type = check_type(standard_list)
    count_mode = StandardMode_to_CountingMode(standard_list)
    if Type == 0: return [Type]
    elif Type == 1:
        c = count_mode.index(1)
        if c == 14: return [Type, 14, [0]]
        return [Type, c]
    elif Type == 2:
        c = count_mode.index(2)
        if c == 12: return [Type, 12, [0]]
        return [Type, c]
    elif Type <= 5:
        c = count_mode.index(3)
        if c == 12: return [Type, 12, [0]]
        return [Type, c]
    elif Type == 6:
        c = count_mode.index(4)
        return [Type, c, [c+1]]
    elif Type <= 8:
        c = count_mode.index(4)
        if c == 12: return [Type, 12, [0]]
        return [Type, c]
    elif Type == 9:
        len_dragon = count_mode.count(1)
        first_index = count_mode.index(1)
        if count_mode[11] == 1: return [Type, len_dragon, first_index, [0]]
        return [Type, len_dragon, first_index]
    elif Type == 10:
        len_double_dragon = count_mode.count(2)
        first_index = count_mode.index(2)
        if count_mode[11] == 2: return [Type, len_double_dragon, first_index, [0]]
        return [Type, len_double_dragon, first_index]
    elif Type <= 13:
        len_plane = count_mode.count(3)
        first_index = count_mode.index(3)
        if count_mode[11] == 3: return [Type, len_plane, first_index, [0]]
        return [Type, len_plane, first_index]
    elif Type <= 16:
        len_aeroplane = count_mode.count(4)
        first_index = count_mode.index(4)
        if count_mode[11] == 4: return [Type, len_aeroplane, first_index, [0]]
        return [Type, len_aeroplane, first_index]
    else:
        return [Type, [-1]]


def ableToControl(my_list, enemy_list):
    '''mylist是countingMode，enemylist是standardMode'''
    Type = check_type(enemy_list)
    counted_enemy_list = StandardMode_to_CountingMode(enemy_list)
    n1, list1, list2 = None, [], []
    bomb_num = bomb_analyse(my_list)[0]
    if bomb_num >= 1:
        list2 = bomb_analyse(my_list)[1]

    if Type == 1:  # 单
        c = counted_enemy_list.index(1)
        normal_ability = 0
        normal_control_list = []
        for j in range(c + 1, 15):
            if my_list[j] > 0:
                normal_ability = 1
                normal_control_list.append([(0 if i != j else 1) for i in range(15)])
        if bomb_num == 0 and normal_ability == 0:
            return [0, [], []]
        if bomb_num == 0 and normal_ability == 1:
            return [1, normal_control_list, []]
        if bomb_num > 0 and normal_ability == 0:
            return [1, [], bomb_analyse(my_list)[1]]
        if bomb_num > 0 and normal_ability == 1:
            return [1, normal_control_list, bomb_analyse(my_list)[1]]

    if Type == 2:  # 对
        c = counted_enemy_list.index(2)
        normal_ability = 0
        normal_control_list = []
        for j in range(c + 1, 15):
            if my_list[j] > 1:
                normal_ability = 1
                normal_control_list.append([(0 if i != j else 2) for i in range(15)])
        if bomb_num == 0 and normal_ability == 0:
            return [0, [], []]
        if bomb_num == 0 and normal_ability == 1:
            return [1, normal_control_list, []]
        if bomb_num > 0 and normal_ability == 0:
            return [1, [], bomb_analyse(my_list)[1]]
        if bomb_num > 0 and normal_ability == 1:
            return [1, normal_control_list, bomb_analyse(my_list)[1]]

    if Type == 3 or Type == 4 or Type == 5:     # 三带
        tri = triplet_analyse(my_list)
        possible_main = []
        given_main = counted_enemy_list.index(3)  # 对方牌的大小
        for indx in tri:
            if indx > given_main:
                possible_main.append(indx)

        if (not possible_main) and (not list2):
            n1 = 0      # 没更大的三条,也没炸，管不了
        else:
            n1 = 1
        if possible_main:

            if Type == 3:     # 三带零（三条）
                for indx in possible_main:
                    tmp = [0 for _ in range(15)]
                    tmp[indx] = 3
                    list1.append(tmp)
            if Type == 4:     # 三带一
                possible_sgl = []
                for i in range(15):
                    if my_list[i] >= 1:
                        possible_sgl.append(i)
                for indx in possible_main:  # indx必然也在possible_sgl里面
                    if len(possible_sgl) >= 2:
                        possible_sgl.remove(indx)
                        for sgl in possible_sgl:
                            tmp = [0 for _ in range(15)]
                            tmp[indx], tmp[sgl] = 3, 1
                            list1.append(tmp)
                        possible_sgl.append(indx)

            if Type == 5:       # 三带对
                possible_dbl = []
                for i in range(15):
                    if my_list[i] >= 2:
                        possible_dbl.append(i)
                for indx in possible_main:  # indx必然也在possible_dbl里面
                    if len(possible_dbl) >= 2:
                        possible_dbl.remove(indx)
                        for dbl in possible_dbl:
                            tmp = [0 for _ in range(15)]
                            tmp[indx], tmp[dbl] = 3, 2
                            list1.append(tmp)
                        possible_dbl.append(indx)

        return [n1, list1, list2]

    if Type == 6: # 炸弹
         c = counted_enemy_list.index(4)
         if bomb_num == 0:
             return [0, [], []]
         if bomb_num >= 1:
             bomb_list = [x for x in bomb_analyse(my_list)[1] if x > c]
             if bomb_list != []:
                 return [1, [], bomb_list]
             return [0, [], []]

    if Type == 7 or Type == 8:      # 四带
        if bomb_num == 0:
            n1 = 0      # 没四条(炸)也没火箭，管不了
        else:
            n1 = 1
            given_main = counted_enemy_list.index(4)
            possible_main = []
            for indx in list2:
                if indx != 13 and indx > given_main:
                    possible_main.append(indx)

            if possible_main:
                if Type == 7:       # 四带二单
                    possible_twoSgl = []
                    for i in range(15):
                        if my_list[i] >= 1:
                            possible_twoSgl.append(i)
                    for indx in possible_main:      # indx必然也在possible_twoSgl里面
                        if len(possible_twoSgl) >= 3:
                            possible_twoSgl.remove(indx)
                            for j in range(len(possible_twoSgl)):
                                one = possible_twoSgl[j]
                                for k in range(j+1, len(possible_twoSgl)):
                                    another = possible_twoSgl[k]
                                    tmp = [0 for _ in range(15)]
                                    tmp[indx], tmp[one], tmp[another] = 4, 1, 1
                                    list1.append(tmp)
                            possible_twoSgl.append(indx)

                if Type == 8:       # 四带二对
                    possible_twoDbl = []
                    for i in range(15):
                        if my_list[i] >= 2:
                            possible_twoDbl.append(i)

                    for indx in possible_main:  # indx必然也在possible_twoDbl里面
                        if len(possible_twoDbl) >= 3:
                            possible_twoDbl.remove(indx)
                            for j in range(len(possible_twoDbl)):
                                one = possible_twoDbl[j]
                                for k in range(j + 1, len(possible_twoDbl)):
                                    another = possible_twoDbl[k]
                                    tmp = [0 for _ in range(15)]
                                    tmp[indx], tmp[one], tmp[another] = 4, 2, 2
                                    list1.append(tmp)
                            possible_twoDbl.append(indx)

        return [n1, list1, list2]

    if Type == 9:  # 龙
        dragon_length = sum(counted_enemy_list)
        dragon_head = counted_enemy_list.index(1)
        normal_ability = 0
        normal_control_list = []
        for j in range(dragon_head + 1, 12 - dragon_length):
            count = 0
            for i in range(dragon_length):
                if my_list[j + i] >= 1:
                    count += 1
            if count == dragon_length:
                normal_control_list.append([(1 if k in range(j, j + dragon_length) else 0) for k in range(15)])
                normal_ability = 1
        if bomb_num == 0 and normal_ability == 0:
            return [0, [], []]
        if bomb_num == 0 and normal_ability == 1:
            return [1, normal_control_list, []]
        if bomb_num > 0 and normal_ability == 0:
            return [1, [], bomb_analyse(my_list)[1]]
        if bomb_num > 0 and normal_ability == 1:
            return [1, normal_control_list, bomb_analyse(my_list)[1]]

    if Type == 10:  # 连对
        double_dragon_length = counted_enemy_list.count(2)
        double_dragon_head = counted_enemy_list.index(2)
        normal_ability = 0
        normal_control_list = []
        for j in range(double_dragon_head + 1, 12 - double_dragon_length):
            count = 0
            for i in range(double_dragon_length):
                if my_list[j + i] >= 2:
                    count += 1
            if count == double_dragon_length:
                normal_control_list.append([(2 if k in range(j, j + double_dragon_length) else 0) for k in range(15)])
                normal_ability = 1
        if bomb_num == 0 and normal_ability == 0:
            return [0, [], []]
        if bomb_num == 0 and normal_ability == 1:
            return [1, normal_control_list, []]
        if bomb_num > 0 and normal_ability == 0:
            return [1, [], bomb_analyse(my_list)[1]]
        if bomb_num > 0 and normal_ability == 1:
            return [1, normal_control_list, bomb_analyse(my_list)[1]]

    if Type == 11 or Type == 12 or Type == 13:      # 飞机
        given_main = plane_analyse(counted_enemy_list)[1]
        possible = plane_analyse(my_list)
        if possible[0] == 0 and (not list2):
            n1 = 0      # 没飞机也没炸，管不了
        else:
            n1 = 1
        if possible[0] == 1:
            possible_main = possible[1]
            given_start = min(given_main)
            given_len = len(given_main)
            for i in range(len(possible_main) - given_len + 1):
                if possible_main[i] > given_start and possible_main[i+given_len-1] == possible_main[i] + given_len - 1:
                    list1.append([possible_main[x] for x in range(i, i+given_len)])
        return [n1, list1, list2]

    if Type == 14 or Type == 15 or Type == 16:      # 航天飞机
        given_main = bomb_analyse(counted_enemy_list)[1]
        if bomb_num == 0:
            n1 = 0  # 没四条(炸)，管不了
        else:
            n1 = 1
            possible_main = bomb_analyse(my_list)[1]
            for x in range(len(possible_main)):     # 去掉火箭
                if possible_main[x] == 13:
                    possible_main.pop(x)
            given_start = min(given_main)
            given_len = len(given_main)
            for i in range(len(possible_main) - given_len + 1):
                if possible_main[i] > given_start and possible_main[i + given_len - 1] == possible_main[i] + given_len - 1:
                    list1.append([possible_main[x] for x in range(i, i + given_len)])
        return [n1, list1, list2]

    if Type == 17:  # 王炸
        return [0, [], []]

def emergency1(myLst,number1,number2,remaining,robotid):
    #上一个出牌的对手牌数已经小于等于4的情形，myLst为自己的手牌，number1与number2是出牌者与另一人的余牌数，remaining是两个对手剩下的牌的并集，robotid 是自己的编号
    if number2<7:#另一人不多于6张
        return 1
    elif max(remaining)>=number1 or max(remaining)>=3:#可以单次出完或是三带一
        return 1
    elif remaining[-1]==1 and remaining[-2]==1:#对王的存在性
        return 1
    else:
        mxs1=0
        mxs2=0
        mxd1=0
        mxd2=0
        for i in range(15):
            if remaining[i]>=2:
                mxd1=i
                mxs1=i
            elif remaining[i]==1:
                mxs1=i
            if myLst[i]>=2:
                mxd2=i
                mxs2=i
            elif myList[i]==1:
                mxs2=i
        if mxs1>=mxs2 or mxd1>=mxd2:#不可能存在更大的单或是更大的对
            return 1
        else:
            if number1<=3 and max(remaining)>=2:#可以打对然后只剩一张（危）
                return 1
            elif number1<=2:#对手仅有两张而且还是先手，危
                return 1
            else:
                randnumber=random.random()#倾向于出，但是还是听天由命
                if randnumber>0.3:
                    return 1
                else:
                    return 0


def emergency2(myLst,number1,number2,remaining,robotid):
    #用于近战，当三个人中非上轮出牌者的人牌数小于等于4时，定义同上。
    if number2==1:
        return 1
    elif number1<7:
        return 1
    elif number2==2 and max(remaining)>=2:
        return 1
    elif max(remaining)>=number2 or max(remaining)>=3:#可以单次出完或是三带一
        return 1
    elif remaining[-1]==1 and remaining[-2]==1:#对王的存在性
        return 1
    else:
        mxs1 = 0
        mxs2 = 0
        mxd1 = 0
        mxd2 = 0
        for i in range(15):
            if remaining[i] >= 2:
                mxd1 = i
                mxs1 = i
            elif remaining[i] == 1:
                mxs1 = i
            if myLst[i] >= 2:
                mxd2 = i
                mxs2 = i
            elif myList[i] == 1:
                mxs2 = i
        if mxs1 >= mxs2 or mxd1 >= mxd2:  # 不可能存在更大的单或是更大的对
            return 1
        else:
            return 0


def raiseValue(myLst,number1,number2,remaining,robotid,lengthOfCard,cardList):
    #在判断好了要出牌以后，判断要出多大的牌，0代表最小，3代表最大
    if number1==1:
        return 3
    elif number1>=lengthOfCard or number2>=lengthOfCard:
        if ableToControl(remaining, cardList)[0]==0:
            return 0
        else:
            if len(ultraThreat)!=0:
                return 1
            else:
                return 2
    else:
        return 0


def bomb_protection(my_list,number1,number2,remaining,cardList):
    #控制一下是否要出炸弹，需要尽量谨慎一点。。。
    cdvalue=0
    urgent=0
    powvalue=0
    nessvalue=0
    solutionList=ableToControl(my_list,cardList)
    if solutionList[0]==1 and len(solutionList[1])==0:
        cdvalue=1
    if len(ultraThreat)!=0:
        urgent=1
        if max(ultraThreat)<max(solutionList[2]):
            powvalue=1
    temp1=dragon_analyse(remaining)
    temp2=plane_analyse(remaining)
    temp3=double_dragon_analyse(remaining)
    warningvalue=0
    if temp1!=[0]:
        warningvalue+=1
    if temp2!=0:
        warningvalue+=1
    if temp3!=0:
        warningvalue+=1
    if number1<=6:
        nessvalue+=1
    if number2<=6:
        nessvalue+=1
    if number1<=4:
        nessvalue+=1
    if nessvalue>=3:
        if cdvalue==1:
            return 3
        else:
            if warningvalue>=1:
                return 2
            else:
                return 1
    elif nessvalue==2:
        if cdvalue==1:
            if warningvalue>0:
                return 3
            else:
                if max(remaining)>=3:
                    return 3
                else:
                    return 2
        else:
            if urgent==1:
                return 2
            else:
                return 1
    elif nessvalue<=1:
        if cdvalue==1:
            return 1
        else:
            return 0


def size(ctn_List):#返回一个countingList的牌数
    e=0
    for i in range(15):
        e=e+ctn_List[i]
    return e


def minusing(my_list,card_List):
    temportoryList=[]
    for i in range(15):
        temportoryList.append(my_list[i]-card_List[i])
    return temportoryList


def Undefeated(my_List,enemyList,number1,number2):
    #0代表可以被管，1代表无敌
    if size(my_List)==4 and max(my_List)==4:
        k=-1
        for i in range(15):
            if my_List[i]==4:
                k=i
                break
        for i in range(k,15):
            if enemyList[i]==4:
                k=-2
                break
        if k==-2 and max(number1,number2)>3:
            return 0
        elif enemyList[14]==1 and enemyList[13]==1 and max(number1,number2)>1:
            return 0
        else:
            return 1
    elif my_List[13]==1 and my_List[14]==1:
        return 0
    elif max(enemyList)==4 or min(enemyList[13],enemyList[14])==1:
        return 0
    else:
        x=ableToControl(enemyList,my_List)
        if x[0]==1 and size(x[1][0])<=max(number1,number2):
            return 0
        else:
            return 1


def myTurnToGo(my_List1,enemyList1,number1,number2):#自己得到先手之后自己出牌的策略，一般是自己牌数较大时。
    temportory=[]
    my_List=my_List1.copy()
    enemyList=enemyList1.copy()
    try1=plane_analyse(my_List)
    try2=double_dragon_analyse(my_List)
    try3=dragon_analyse(my_List)
    try4=triplet_analyse(my_List)
    try5=bomb_analyse(my_List)[1]
    if 13 in try5:
        try5.remove(13)
    if 1 not in my_List[:13] and 2 not in my_List[:13] and 3 not in my_List[:13] and king_analyse(my_List)[0]==king_analyse(my_List)[1]:
        ttList=[]
        for i in range(15):
            ttList.append(0)
        for i in range(15):
            if my_List[i]==4:
                ttList[i]=4
                break
        return ttList
    elif 1 not in my_List[:13] and 2 not in my_List[:13] and king_analyse(my_List)[0]==king_analyse(my_List)[1]:
        ttList=[]
        for i in range(15):
            ttList.append(0)
        for i in range(15):
            if my_List[i]==3:
                ttList[i]=3
                break
        return ttList
    elif 1 not in my_List[:13] and 2 not in my_List[:13]:
        ttList=[]
        for i in range(15):
            ttList.append(0)
        for i in range(15):
            if my_List[i]==3:
                ttList[i]=3
                break
        if my_List[13]==1:
            ttList[13]=1
        elif my_List[14]==1:
            ttList[14]=1
        return ttList
    if try1[0]==1:
        length=len(try1[1])
        for i in range(length-1):
            if try1[1][i]==try1[1][i+1]-1:
                temportory=my_List
                temportory[try1[1][i]]-=3
                temportory[try1[1][i+1]] -= 3
                k1=bomb_analyse(my_List)[0]-bomb_analyse(temportory)[0]
                k2=len(single_analyse(my_List))-len(single_analyse(temportory))
                k3=len(pair_analyse(my_List))-len(pair_analyse(temportory))
                if k1==2:
                    continue
                else:
                    if k2+k3<-2:
                        continue
                    else:
                        x1=single_analyse(temportory)
                        x2=pair_analyse(temportory)
                        wings1=[]
                        wings2=[]
                        totalList=[]
                        for m in range(15):
                            totalList.append(0)
                        if len(x1)>=2:
                            for j in x1:
                                if j!=try1[1][i] and j!=try1[1][i+1]:
                                    wings1.append(j)
                                if len(wings1)==2:
                                    break
                        if len(x2)>=2:
                            for j in x2:
                                if j!=try1[1][i] and j!=try1[1][i+1]:
                                    wings2.append(j)
                                if len(wings2)==2:
                                    break
                        if wings1[1]<=8:
                            totalList[wings1[0]]=1
                            totalList[wings1[1]]=1
                            totalList[try1[1][i]]=3
                            totalList[try1[1][i+1]] = 3
                            return totalList
                        elif wings2[1]<=8:
                            totalList[wings2[0]]=2
                            totalList[wings2[1]]=2
                            totalList[try1[1][i]]=3
                            totalList[try1[1][i+1]] = 3
                            return totalList
                        else:
                            if k2+k3>=0:
                                totalList[try1[1][i]] = 3
                                totalList[try1[1][i + 1]] = 3
                                return totalList
    my_List = my_List1.copy()
    if try2[0]!=0:
        if try2[0]>=2:
            x1=try2[1][0]
            totalList = []
            for m in range(15):
                totalList.append(0)
            for n in range(x1[0],x1[1]+1):
                totalList[n]=2
            return totalList
        else:
            temportory = my_List
            for i in bomb_analyse(myList):
                if i!=13:
                    temportory[i]=0
            try22=double_dragon_analyse(temportory)
            if try22[0]==1:
                x1=try22[1][0]
                totalList = []
                for m in range(15):
                    totalList.append(0)
                for n in range(x1[0], x1[1] + 1):
                    totalList[n] = 2
                return totalList
    my_List = my_List1.copy()
    if try3[0]!=0:
        if try3[0]>=2:
            x1=try3[1][0]
            totalList = []
            for m in range(15):
                totalList.append(0)
            for n in range(x1[0],x1[1]+1):
                totalList[n]=1
            return totalList
        else:
            temportory = my_List
            for i in bomb_analyse(myList):
                if i!=13:
                    temportory[i]=0
            try32=dragon_analyse(temportory)
            if try32[0]==1:
                x1=try32[1][0]
                totalList = []
                for m in range(15):
                    totalList.append(0)
                for n in range(x1[0], x1[1] + 1):
                    totalList[n] = 1
                return totalList
            else:
                temportory1=my_List
                totalList = []
                for m in range(15):
                    totalList.append(0)
                for n in range(try3[1][0][0],try3[1][0][1]+1):
                    temportory1[n]-=1
                    totalList[n] = 1
                if len(triplet_analyse(my_List))-len(triplet_analyse(temportory1))<=1 and len(single_analyse(my_List))-len(single_analyse(temportory1))>=-2:
                    return totalList
    my_List = my_List1.copy()
    if len(try4)>0:
        for i in try4:
            temportory2=my_List
            if my_List[i]==3 and i<10:
                temportory2[i]=0
                if len(single_analyse(my_List))-len(single_analyse(temportory2))>=-1 and len(single_analyse(temportory2))>0:
                    k=single_analyse(temportory2)[0]
                    if k<i:
                        totalList = []
                        for m in range(15):
                            totalList.append(0)
                        totalList[i]=3
                        totalList[k]=1
                        return totalList
                if len(pair_analyse(my_List))-len(pair_analyse(temportory2))>=-1 and len(pair_analyse(temportory2))>0:
                    k=pair_analyse(temportory2)[0]
                    if k<i:
                        totalList = []
                        for m in range(15):
                            totalList.append(0)
                        totalList[i]=3
                        totalList[k]=2
                        return totalList
    my_List = my_List1.copy()
    if len(try5)>0 and len(ultraThreat)==0:
        maxium1=0
        maxium2=0
        for kk in enemyList:
            if kk!=0:
                maxium1=kk
        for kk in my_List:
            if kk!=0 and kk not in try5:
                maxium2=kk
        if maxium2>=maxium1 or len(try5)>1:
            x51=single_analyse(my_List)
            x52=pair_analyse(my_List)
            if len(x51)>=3 and x51[2]<=8 and try5[0]<9:
                totalList = []
                for m in range(15):
                    totalList.append(0)
                totalList[try5[0]]=4
                totalList[x51[0]]=1
                totalList[x51[1]]=1
                return totalList
            if len(x52)>=3 and x52[2]<=8 and try5[0]<9:
                totalList = []
                for m in range(15):
                    totalList.append(0)
                totalList[try5[0]]=4
                totalList[x52[0]]=2
                totalList[x52[1]]=2
                return totalList
    try6=single_analyse(my_List)
    my_List = my_List1.copy()
    if try6!=[] and try6[0]<8:
        totalList = []
        for m in range(15):
            totalList.append(0)
        totalList[try6[0]]=1
        return totalList
    try7=pair_analyse(my_List)
    my_List = my_List1.copy()
    if try7!=[] and try7[0]<8:
        totalList = []
        for m in range(15):
            totalList.append(0)
        totalList[try7[0]]=2
        return totalList
    else:
        for i in try4:
            if i in try5:
                try4.remove(i)
        if try2[0]!=0:
            totalList = []
            for m in range(15):
                totalList.append(0)
            h=try2[1][0][0]
            hh=try2[1][0][1]
            xxx=min(max(h+2,9),hh)
            for j in range(h ,xxx+1):
                totalList[j]=2
            return totalList
        elif  try3[0]!=0:
            totalList = []
            for m in range(15):
                totalList.append(0)
            h=try3[1][0][0]
            hh=try3[1][0][1]
            xxx=min(max(h+4,9),hh)
            for j in range(h ,xxx+1):
                totalList[j]=1
            return totalList
        elif len(try4)!=0 and try4[0]<10:
            x1=single_analyse(my_List)
            x2=pair_analyse(my_List)
            if x1!=[]:
                if x2!=[]:
                    if x1[0]<=x2[0] and x1[0]<10:
                        totalList = []
                        for m in range(15):
                            totalList.append(0)
                        totalList[try4[0]]=3
                        totalList[x1[0]]=1
                        return totalList
                    elif x1[0]>=x2[0] and x2[0]<10:
                        totalList = []
                        for m in range(15):
                            totalList.append(0)
                        totalList[try4[0]]=3
                        totalList[x2[0]]=2
                        return totalList
                    else:
                        totalList = []
                        for m in range(15):
                            totalList.append(0)
                        totalList[try4[0]] = 3
                        return totalList
                else:
                    if x1[0]<10:
                        totalList = []
                        for m in range(15):
                            totalList.append(0)
                        totalList[try4[0]] = 3
                        totalList[x1[0]]=1
                        return totalList
                    else:
                        totalList = []
                        for m in range(15):
                            totalList.append(0)
                        totalList[try4[0]] = 3
                        return totalList
            else:
                totalList = []
                for m in range(15):
                    totalList.append(0)
                totalList[try4[0]] = 3
                return totalList
        else:
            k1=-1
            k2=0
            for i in range(13):
                if my_List[i]>0 and my_List[i]!=4:
                    k1=i
                    k2=my_List[i]
                    break
            totalList = []
            for m in range(15):
                totalList.append(0)
            if k1==-1 and 13 in bomb_analyse(my_List)[1]:
                xxxx=bomb_analyse(my_List)[1][0]
                if xxxx<=12:
                    totalList[xxxx]=4
                else:
                    totalList[13]=1
                    totalList[14]=1
                return totalList
            elif k1==-1:
                if my_List[13]==1:
                    totalList[13]=1
                    return totalList
                elif my_List[14]==1:
                    totalList[14]=1
                    return totalList
                else:
                    xxxx = bomb_analyse(my_List)[1][0]
                    totalList[xxxx] = 4
                    return totalList
            else:
                totalList[k1]=k2
                return totalList


def myTurnToGoPlus(my_List1,enemyList1,number1,number2): #牌比较少时，自己的牌少于6。
    lengthOfMyList=size(my_List1)
    totalList = []
    for m in range(15):
        totalList.append(0)
    tempLsMe=[]
    tempLsEnemy=[]
    for i in range(15):
        if my_List1[i]!=0:
            tempLsMe.append([i,my_List1[i]])
        if enemyList1[i]!=0:
            tempLsEnemy.append([i,enemyList1[i]])
    if lengthOfMyList==1:
        totalList=my_List1
        return totalList
    elif lengthOfMyList==2:
        if max(my_List1)==2 or king_analyse(my_List1)==[1,1]:
            totalList=my_List1
            return totalList
        else:
            if min(number1,number2)==1:
                k=tempLsMe[-1][0]
                totalList[k]=1
                return totalList
            elif tempLsMe[-1][0]>=tempLsEnemy[-1][0] and len(ultraThreat)==0:
                k = tempLsMe[-1][0]
                totalList[k] = 1
                return totalList
            else:
                k=tempLsMe[0][0]
                return totalList
    elif lengthOfMyList==3:
        if max(my_List1)==3:
            return my_List1
        elif max(my_List1)==2:
            ttList1=my_List1.copy()
            kk1=0
            kk2=0
            for i in range(15):
                if ttList1[i]==1:
                    ttList1[i]=0
                    kk1=i
                    break
            if Undefeated(ttList1,enemyList1,number1,number2)==1:
                return ttList1
            ttList2 = my_List1.copy()
            for i in range(15):
                if ttList2[i] == 2:
                    ttList2[i] = 0
                    kk2=i
                    break
            if Undefeated(ttList2,enemyList1,number1,number2)==1:
                return ttList2
            if min(number1,number2)==1:
                return ttList1
            else:
                if kk1>kk2:
                    return ttList2
                else:
                    return ttList1
        else:
            if king_analyse(my_List1)==[1,1]:
                totalList[13]=1
                totalList[14]=1
                return totalList
            elif tempLsMe[-1][0]>tempLsEnemy[-1][0] and len(ultraThreat)==0 and min(number1,number2)>=2:
                totalList[tempLsMe[0][0]]=1
                return totalList
            elif min(number1,number2)==1:
                totalList[tempLsMe[-1][0]] = 1
                return totalList
    elif lengthOfMyList==4:
        if max(my_List1)>=3:
            return my_List1
        elif king_analyse(my_List1)==[1,1]:
            if min(number1,number2)==1 and max(my_List1)==2:
                totalList[13]=1
                totalList[14]=1
                return totalList
            elif tempLsMe[1][0]>tempLsEnemy[0][0]:
                totalList[tempLsMe[1][0]]=1
                return totalList
            else:
                totalList[13] = 1
                totalList[14] = 1
                return totalList
        elif max(my_List1)==2:
            if min(my_List1)==2:
                ttlist=totalList.copy()
                ttlist[tempLsMe[1][0]]=2
                if Undefeated(ttlist,enemyList1,number1,number2)==1:
                    return ttlist
                elif number1==2 or number2==2:
                    return ttlist
                else:
                    ttlist = totalList.copy()
                    ttlist[tempLsMe[0][0]] = 2
                    return ttlist
            else:
                ttlist = totalList.copy()
                if tempLsMe[0][1]==2:
                    if number1==2 or number2==2:
                        ttlist[tempLsMe[1][0]]=1
                        if Undefeated(ttlist,enemyList1,number1,number2)==1:
                            return ttlist
                        ttlist[tempLsMe[1][0]] = 0
                        ttlist[tempLsMe[0][0]] = 2
                        if Undefeated(ttlist,enemyList1,number1,number2)==1:
                            return ttlist
                        ttlist[tempLsMe[0][0]] = 0
                        ttlist[tempLsMe[2][0]] = 1
                        if Undefeated(ttlist, enemyList1, number1, number2) == 0:
                            ttlist[tempLsMe[0][0]] = 2
                            ttlist[tempLsMe[2][0]] = 0
                            return ttlist
                        else:
                            if min(number1,number2)==1:
                                return ttlist
                            else:
                                ttlist[tempLsMe[0][0]] = 1
                                return ttlist
                    else:
                        ttlist = totalList.copy()
                        ttlist[tempLsMe[0][0]] = 2
                        if Undefeated(ttlist, enemyList1, number1, number2) == 0:
                            ttlist[tempLsMe[0][0]] = 0
                            ttlist[tempLsMe[1][0]] = 1
                            if Undefeated(ttlist, enemyList1, number1, number2) == 0:
                                ttlist = totalList.copy()
                                ttlist[tempLsMe[0][0]] = 2
                                return ttlist
                            else:
                                return ttlist
                        else:
                            return ttlist
                elif tempLsMe[1][1] == 2:
                    ttlist[tempLsMe[1][0]] = 2
                    if Undefeated(ttlist, enemyList1, number1, number2) == 1:
                        return ttlist
                    elif min(number1,number2)==1:
                        return ttlist
                    else:
                        ttlist0=ttlist.copy()
                        ttlist0[tempLsMe[2][0]]=1
                        ttlist0[tempLsMe[1][0]]=0
                        if Undefeated(ttlist0, enemyList1, number1, number2) == 1:
                            ttlist[tempLsMe[1][0]]=0
                            ttlist[tempLsMe[0][0]]=1
                            return ttlist
                        else:
                            return ttlist
                else:
                    if min(number1,number2)==1:
                        ttlist[tempLsMe[2][0]] = 2
                        return ttlist
                    elif tempLsMe[-1][0]<tempLsEnemy[-1][0]:
                        ttlist[tempLsMe[2][0]] = 2
                        return ttlist
                    else:
                        ttlist[tempLsMe[0][0]] = 1
                        return ttlist
        else:
            ttlist = totalList.copy()
            if min(number1,number2)==1:
                ttlist[tempLsMe[-1][0]]=1
                return ttlist
            else:
                ttlist[tempLsMe[0][0]] = 1
                return ttlist
    else:#手里有五张牌
        ttList=totalList.copy()
        if max(my_List1)==4:
            if tempLsMe[0][1]==4:
                ttList[tempLsMe[0][0]]=4
                if Undefeated(ttList, enemyList1, number1, number2) == 1:
                    return ttList
                elif min(number1,number2)==1:
                    return ttList
                else:
                    ttList[tempLsMe[0][0]] = 0
                    ttList[tempLsMe[1][0]] = 1
                    return ttList
            else:
                ttList[tempLsMe[1][0]] = 4
                if Undefeated(ttList, enemyList1, number1, number2) == 1:
                    return ttList
                elif min(number1, number2) == 1:
                    return ttList
                else:
                    ttList[tempLsMe[1][0]] = 0
                    ttList[tempLsMe[0][0]] = 1
                    return ttList
        elif max(my_List1)==3:
            if 2 in my_List1:
                return my_List1
            elif king_analyse(my_List1)==[1,1]:
                totalList[13]=1
                totalList[14]=1
                return totalList
            else:
                if tempLsMe[0][1]==3:
                    ttList=totalList.copy()
                    ttList[tempLsMe[-1][0]]=1
                    if Undefeated(ttList, enemyList1, number1, number2) == 1:
                        return ttList
                    else:
                        ttList[tempLsMe[-1][0]] = 0
                        ttList[tempLsMe[0][0]] = 3
                        ttList[tempLsMe[1][0]] = 1
                        return ttList
                elif tempLsMe[1][1] == 3:
                    ttList = totalList.copy()
                    ttList[tempLsMe[-1][0]] = 1
                    if Undefeated(ttList, enemyList1, number1, number2) == 1:
                        return ttList
                    else:
                        ttList[tempLsMe[-1][0]] = 0
                        ttList[tempLsMe[1][0]] = 3
                        ttList[tempLsMe[0][0]] = 1
                        return ttList
                else:
                    ttList[tempLsMe[2][0]] = 3
                    ttList[tempLsMe[0][0]] = 1
                    if Undefeated(ttList, enemyList1, number1, number2) == 1:
                        return ttList
                    elif min(number1,number2)<=2:
                        return ttList
                    else:
                        ttList[tempLsMe[2][0]] = 0
                        return ttList


        elif max(my_List1)==2:
            ttList = totalList.copy()
            if len(tempLsMe)==3:
                if tempLsMe[0][1]==2:
                    ttList[tempLsMe[0][0]]=2
                    if Undefeated(ttList,enemyList1,number1,number2)==1 or min(number1,number2)==1:
                        return ttList
                    elif min(number1,number2)>2:
                        return ttList
                    else:
                        if tempLsMe[1][1]==2:
                            ttList[tempLsMe[0][0]] = 0
                            ttList[tempLsMe[1][0]] = 2
                            if Undefeated(ttList,enemyList1,number1,number2)==1:
                                return ttList
                            else:
                                ttList[tempLsMe[1][0]] = 0
                                ttList[tempLsMe[2][0]] = 1
                                return ttList
                        else:
                            ttList[tempLsMe[0][0]] = 0
                            ttList[tempLsMe[1][0]]=1
                            return ttList
                else:
                    ttList[tempLsMe[1][0]] = 2
                    if Undefeated(ttList,enemyList1,number1,number2)==1 or min(number1,number2)==1:
                        return ttList
                    elif min(number1,number2)>2:
                        return ttList
                    else:
                        if min(number1,number2)==2 and tempLsMe[-1][0]>tempLsEnemy[-1][0]:
                            ttList[tempLsMe[1][0]] = 0
                            ttList[tempLsMe[0][0]] = 1
                            return ttList
                        else:
                            ttList[tempLsMe[1][0]] = 0
                            ttList[tempLsMe[2][0]] = 2
                            return ttList
            else:
                if min(number1,number2)!=2:
                    kk=-1
                    for i in range(15):
                        if my_List1[i]==2:
                            kk=i
                            break
                    ttList[kk]=2
                    return ttList
                else:
                    kk = -1
                    for i in range(15):
                        if my_List1[i] == 2:
                            kk = i
                            break
                    ttList[kk] = 2
                    if Undefeated(ttList,enemyList1,number1,number2)==1:
                        return ttList
                    else:
                        ttList=totalList.copy()
                        if tempLsMe[-1][0]>tempLsEnemy[-1][0]:
                            if tempLsMe[0][1]==2:
                                ttList[tempLsMe[1][0]]=1
                                return ttList
                            else:
                                ttList[tempLsMe[0][0]]=1
                                return ttList
                        else:
                            kk = -1
                            for i in range(15):
                                if my_List1[i] == 2:
                                    kk = i
                                    break
                            ttList[kk] = 2
                            return ttList
        else:
            ttList=totalList.copy()
            if dragon_analyse(my_List1)[0]!=0:
                return my_List1
            elif king_analyse(my_List1)==[1,1]:
                if min(number1,number2)==1 and tempLsEnemy[-1][0]>tempLsMe[2][0]:
                    ttList[13]=1
                    ttList[14]=1
                    return ttList
                else:
                    ttList[tempLsMe[2][0]]=1
                    return ttList
            else:
                if min(number1,number2)==1:
                    ttList[tempLsMe[-1][0]]=1
                    return ttList
                else:
                    ttList[tempLsMe[0][0]]=1
                    return ttList


full_input = json.loads(input()) # dict
use_info = full_input["requests"][0] # dict # keys:"own","history","publiccard"
requests = full_input["requests"] # list

#下面确定robotID
robotID = 0
if use_info["history"] == [[],[]]: # 地主
    robotID = 0
elif use_info["history"][0] == []: # 农民1
    robotID = 1
else:                            # 农民2
    robotID = 2

my_initial_list = StandardMode_to_CountingMode(use_info["own"]) # 这是counted模式

#为了方便，我们引入一个函数如下。
def StandardMode_To_PositioningMode(standard_list):
    '''输入standard_list，输出position_list，表示归位的模式'''
    position_list = []
    for i in range(0,52,4):
        position_list.append([x for x in range(i,i+4) if x in standard_list])
    if 52 in standard_list:
        position_list.append([52])
    else:
        position_list.append([])
    if 53 in standard_list:
        position_list.append([53])
    else:
        position_list.append([])
    return position_list
position_my_initial_list = StandardMode_To_PositioningMode(use_info["own"]) # 我的初始手牌的position模式

#下面确定，此时此刻另外两家的手牌有哪些（即所有牌中去掉我的手牌，去掉已经落地的牌）
all_poker = set([x for x in range(54)])
my_initial_poker = set(use_info["own"])
other_two_poker = all_poker - my_initial_poker #差集，此时表示的是另两家初始有哪些手牌
l = len(requests) # 回合数
for i in range(l): # 这部分用于去掉过程中另两家打出的牌
    a,b = set(requests[i]["history"][0]),set(requests[i]["history"][1])
    other_two_poker = other_two_poker - (a | b) # a|b 表示并集，现在，other_two_poker即表示此时此刻另两家手中的牌
other_two_counted_list = StandardMode_to_CountingMode(list(other_two_poker))

#下面确定另外两家此时此刻还有几张牌
if robotID == 0:
    number_remained_up = 17
    number_remained_upup = 17
elif robotID == 1:
    number_remained_up = 20
    number_remained_upup = 17
else:
    number_remained_up = 17
    number_remained_upup = 20
l = len(requests) # 回合数
for i in range(l):
    up_out_num = len(requests[i]["history"][1]) # 第i回合上家出了多少牌
    upup_out_num = len(requests[i]["history"][0]) # 第i回合上上家出了多少牌
    number_remained_up = number_remained_up - up_out_num
    number_remained_upup = number_remained_upup - upup_out_num

#下面确定此时此刻我还有哪些牌
my_now_set = set(use_info["own"])
for i in full_input["responses"]:
    my_now_set = my_now_set - set(i)
my_now_standard_list = list(my_now_set)
my_now_counted_list = StandardMode_to_CountingMode(my_now_standard_list)
my_now_position_list = StandardMode_To_PositioningMode(my_now_standard_list)

#下面确定当前回合另外两家都出了啥牌
ls_up = requests[-1]["history"][1] # standard模式
ls_upup = requests[-1]["history"][0] # standard模式
this_round_up = StandardMode_to_CountingMode(requests[-1]["history"][1]) # counted模式
this_round_upup = StandardMode_to_CountingMode(requests[-1]["history"][0]) # counted模式

#下面定义一个函数判断当前时刻，另外两家是否有炸弹/王炸，如果有，输出坐标的列表，没有就输出空表
def Bomb_Outside(other_two_counted_list, number_remained_up, number_remained_upup):
    bomb_outside_list = [] # 另两家可能存在的炸弹列表
    if other_two_counted_list[13:] == [1,1] and max(number_remained_up, number_remained_upup) >= 2:
        bomb_outside_list.append(13)

    if max(number_remained_up, number_remained_upup) < 4:
        pass
    else:
        for i in range(13):
            if other_two_counted_list[i] == 4:
                bomb_outside_list.append(i)
    bomb_outside_list.sort()
    return bomb_outside_list


myList=my_initial_list.copy()
l1=ls_up#上家输入
l2=ls_upup#上上家输入
inputList1=StandardMode_to_CountingMode(l1)
inputList2=StandardMode_to_CountingMode(l2)
remainingList=other_two_counted_list#对手还剩什么牌（总共）,为count_list型
numberRemainedUp=number_remained_up#对手1还剩几张牌（下下家）
numberRemainedUpUp=number_remained_upup#对手2还剩几张牌（下家）
ultraThreat=Bomb_Outside(other_two_counted_list,number_remained_up,number_remained_upup)#对手可能拥有的所有炸弹类型

publiccards = use_info["publiccard"]
def f(x):
    if x in publiccards:
        return 1
    else:
        return 0
def finalOutput(positionList,finallist):
    out_list = []  # 要出的牌，standard模式
    for i in range(15):
        if finallist[i]!=0:
            lss=sorted(positionList[i],key=f)
            for j in range(finallist[i]):
                a=lss.pop()
                out_list.append(a)
    out_list.sort()
    return out_list

#接下来就要好戏开场了。。。
finalListOfAnswer=[]
for i in range(15):
    finalListOfAnswer.append(0)
finalListOfAnswer11=finalListOfAnswer.copy()
try:
    semifinalList = []
    for i in range(15):
        semifinalList.append(0)
    if size(myList)>0:
        if size(inputList1)==0 and size(inputList2)==0:
            if size(myList)>=6:
                semifinalList=myTurnToGo(myList,remainingList,numberRemainedUp,numberRemainedUpUp)
            else:
                semifinalList=myTurnToGoPlus(myList,remainingList,numberRemainedUp,numberRemainedUpUp)
        else:
            firstofChoice=[]
            if size(inputList1) != 0:
                firstofChoice = ableToControl(myList, inputList1)
            else:
                firstofChoice = ableToControl(myList, inputList2)
            if firstofChoice[0]==1:
                if size(myList)==len(l1) and len(l1)!=0 and firstofChoice[1]!=[]:
                    finalListOfAnswer11=myList
                elif size(myList)==len(l2) and len(l1)==0 and firstofChoice[1]!=[]:
                    finalListOfAnswer11 = myList
                elif size(myList)==4 and firstofChoice[2][0]<13:
                    finalListOfAnswer11 = myList
                elif size(myList)==2 and firstofChoice[2][0]==13:
                    finalListOfAnswer11 = myList
            typeOfCard=0
            if size(inputList1)!=0:
                access = 0
                if numberRemainedUp <= 4:
                    access = access + emergency1(myList, numberRemainedUp, numberRemainedUpUp, remainingList, 0)
                if numberRemainedUpUp <= 4:
                    access = access + emergency2(myList, numberRemainedUp, numberRemainedUpUp, remainingList, 0)
                typeOfCard = check_type(l1)
            else:
                access = 0
                if numberRemainedUp <= 4:
                    access = access + emergency1(myList, numberRemainedUpUp, numberRemainedUp, remainingList, 0)
                if numberRemainedUpUp <= 4:
                    access = access + emergency2(myList, numberRemainedUpUp, numberRemainedUp, remainingList, 0)
                typeOfCard = check_type(l2)
            if firstofChoice[0]!=0:
                if size(inputList1)!=0:
                    lengthOfCard=size(inputList1)
                    necessity=raiseValue(myList,numberRemainedUp,numberRemainedUpUp,remainingList,0,lengthOfCard,inputList1)
                else:
                    lengthOfCard = size(inputList2)
                    necessity = raiseValue(myList, numberRemainedUpUp, numberRemainedUp, remainingList, 0, lengthOfCard,inputList2)
                necessityOfBomb=max(bomb_protection(myList,numberRemainedUp,numberRemainedUpUp,remainingList,inputList1),bomb_protection(myList,numberRemainedUpUp,numberRemainedUp,remainingList,inputList1))
                if len(firstofChoice[1])==0:
                    if necessityOfBomb+2*access>=4 or necessityOfBomb==3:
                        if firstofChoice[2][0]<=12:
                            semifinalList[firstofChoice[2][0]]=4
                        elif firstofChoice[2][0]==13:
                            semifinalList[13]=1
                            semifinalList[14]=1
                else:
                    if access == 2:
                        if 2*access+necessityOfBomb>=5 and len(firstofChoice[2])>0:
                            if firstofChoice[2][0] <= 12:
                                semifinalList[firstofChoice[2][0]] = 4
                            elif firstofChoice[2][0] == 13:
                                semifinalList[13] = 1
                                semifinalList[14] = 1
                        else:
                            if typeOfCard not in [11,12,13,14,15,16]:
                                if necessity*2+necessityOfBomb>=7 and len(firstofChoice[2])>0:
                                    if firstofChoice[2][0] <= 12:
                                        semifinalList[firstofChoice[2][0]] = 4
                                    elif firstofChoice[2][0] == 13:
                                        semifinalList[13] = 1
                                        semifinalList[14] = 1
                                else:
                                    if necessity>=2:
                                        semifinalList=firstofChoice[1][-1]
                                    else:
                                        semifinalList=firstofChoice[1][0]
                            else:
                                if necessity*2+necessityOfBomb>=7 and len(firstofChoice[2])>0:
                                    if firstofChoice[2][0] <= 12:
                                        semifinalList[firstofChoice[2][0]] = 4
                                    elif firstofChoice[2][0] == 13:
                                        semifinalList[13] = 1
                                        semifinalList[14] = 1
                                else:
                                    if typeOfCard==11:
                                        if necessity >= 3:
                                            semifinalList = firstofChoice[1][-1]
                                        else:
                                            semifinalList = firstofChoice[1][0]
                                    elif typeOfCard==12:
                                        if necessity >= 3 or len(firstofChoice[1])==1:
                                            semifinalList = firstofChoice[1][-1]
                                            c=size(semifinalList)//3
                                            selectList=minusing(myList,semifinalList)
                                            k=[]
                                            for i in range(13):
                                                if selectList[i]==1 and semifinalList[i]==0:
                                                    k.append(i)
                                                    c=c-1
                                                if c==0:
                                                    break
                                            if c>0:
                                                for i in range(13):
                                                    if selectList[i]>1 and selectList[i]!=4 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                            if c>0 and len(firstofChoice[2])>0:
                                                semifinalList = []
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if firstofChoice[2][0] <= 12:
                                                    semifinalList[firstofChoice[2][0]] = 4
                                                elif firstofChoice[2][0] == 13:
                                                    semifinalList[13] = 1
                                                    semifinalList[14] = 1
                                            elif c>0:
                                                for i in range(13,15):
                                                    if selectList[i]==1:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                                for j in k:
                                                    semifinalList[j]=1
                                            else:
                                                for j in k:
                                                    semifinalList[j]=1
                                        else:
                                            if len(firstofChoice[1])>1:
                                                semifinalList = firstofChoice[1][0]
                                                c = size(semifinalList) // 3
                                                selectList = minusing(myList, semifinalList)
                                                k = []
                                                for i in range(13):
                                                    if selectList[i] == 1 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                                if c > 0:
                                                    for i in range(13):
                                                        if selectList[i] > 1 and selectList[i] != 4 and semifinalList[i] == 0:
                                                            k.append(i)
                                                            c = c - 1
                                                        if c == 0:
                                                            break
                                                if c > 0 and len(firstofChoice[2]) > 0:
                                                    semifinalList = []
                                                    for i in range(15):
                                                        semifinalList.append(0)
                                                    if firstofChoice[2][0] <= 12:
                                                        semifinalList[firstofChoice[2][0]] = 4
                                                    elif firstofChoice[2][0] == 13:
                                                        semifinalList[13] = 1
                                                        semifinalList[14] = 1
                                                elif c > 0:
                                                    for i in range(13, 15):
                                                        if selectList[i] == 1:
                                                            k.append(i)
                                                            c = c - 1
                                                        if c == 0:
                                                            break
                                                    for j in k:
                                                        semifinalList[j] = 1
                                                else:
                                                    for j in k:
                                                        semifinalList[j] = 1
                                    elif typeOfCard==13:
                                        if necessity >= 3 or len(firstofChoice[1])==1:
                                            semifinalList = firstofChoice[1][-1]
                                            c=size(semifinalList)//3
                                            selectList=minusing(myList,semifinalList)
                                            k=[]
                                            for i in range(13):
                                                if selectList[i]==2 and semifinalList[i]==0:
                                                    k.append(i)
                                                    c=c-1
                                                if c==0:
                                                    break
                                            if c>0:
                                                for i in range(13):
                                                    if selectList[i]>2 and selectList[i]!=4 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                            if c>0 and len(firstofChoice[2])>0:
                                                semifinalList = []
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if firstofChoice[2][0] <= 12:
                                                    semifinalList[firstofChoice[2][0]] = 4
                                                elif firstofChoice[2][0] == 13:
                                                    semifinalList[13] = 1
                                                    semifinalList[14] = 1
                                            elif c==0:
                                                for j in k:
                                                    semifinalList[j]=2
                                        else:
                                            if len(firstofChoice[1])>1:
                                                semifinalList = firstofChoice[1][0]
                                                c = size(semifinalList) // 3
                                                selectList = minusing(myList, semifinalList)
                                                k = []
                                                for i in range(13):
                                                    if selectList[i] == 2 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                                if c > 0:
                                                    for i in range(13):
                                                        if selectList[i] > 2 and selectList[i] != 4 and semifinalList[i] == 0:
                                                            k.append(i)
                                                            c = c - 1
                                                        if c == 0:
                                                            break
                                                if c > 0 and len(firstofChoice[2]) > 0:
                                                    semifinalList = []
                                                    for i in range(15):
                                                        semifinalList.append(0)
                                                    if firstofChoice[2][0] <= 12:
                                                        semifinalList[firstofChoice[2][0]] = 4
                                                    elif firstofChoice[2][0] == 13:
                                                        semifinalList[13] = 1
                                                        semifinalList[14] = 1
                                                elif c > 0:
                                                    for i in range(13, 15):
                                                        if selectList[i] == 1:
                                                            k.append(i)
                                                            c = c - 1
                                                        if c == 0:
                                                            break
                                                    for j in k:
                                                        semifinalList[j] = 2
                                                elif c==0:
                                                    for j in k:
                                                        semifinalList[j] = 2
                                    else:
                                        tmpsin=single_analyse(myList)
                                        tmppair=pair_analyse(myList)
                                        tmpsinUltra=[]
                                        for i in range(13):
                                            if myList[i]==1:
                                                tmpsinUltra.append(i)
                                        tmppairUltra=[]
                                        for i in range(13):
                                            if myList[i]==2:
                                                tmppairUltra.append(i)
                                        tmptriUltra=[]
                                        for i in range(13):
                                            if myList[i]==3:
                                                tmptriUltra.append(i)
                                        if typeOfCard==14:
                                            if necessityOfBomb>=1 and firstofChoice[2][0]<13:
                                                semifinalList[firstofChoice[2][0]]=4
                                            elif necessityOfBomb>=2 and king_analyse(myList)==[1,1]:
                                                semifinalList[13]=1
                                                semifinalList[14]=1
                                        elif typeOfCard==15:
                                            c0=lengthOfCard//6
                                            if len(tmpsinUltra)>=2*c0:
                                                semifinalList=firstofChoice[1][0]
                                                for k in range(2*c0):
                                                    semifinalList[tmpsinUltra[k]]=1
                                            elif len(tmpsinUltra)>c0 and len(tmpsinUltra)+len(tmppairUltra)>=2*c0:
                                                semifinalList = firstofChoice[1][0]
                                                ss=2*c0
                                                for i in tmpsinUltra:
                                                    semifinalList[i]=1
                                                    ss=ss-1
                                                for i in range(ss):
                                                    semifinalList[tmppairUltra[i]]=1
                                            else:
                                                semifinalList=[]
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if necessityOfBomb>=1 and necessity>0:
                                                    semifinalList[bomb_analyse(myList)[0]]=4
                                        elif typeOfCard==16:
                                            c0 = lengthOfCard // 8
                                            if len(tmppairUltra) >= 2 * c0:
                                                semifinalList = firstofChoice[1][0]
                                                for i in range(2*c0):
                                                    semifinalList[tmppairUltra[i]] = 2
                                            else:
                                                semifinalList = []
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if necessityOfBomb >= 1 and necessity > 0:
                                                    semifinalList[bomb_analyse(myList)[0]] = 4

                    elif access==1:
                        if necessityOfBomb==3 and len(firstofChoice[2])>0:
                            if firstofChoice[2][0] <= 12:
                                semifinalList[firstofChoice[2][0]] = 4
                            elif firstofChoice[2][0] == 13:
                                semifinalList[13] = 1
                                semifinalList[14] = 1
                        else:
                            if typeOfCard not in [11,12,13,14,15,16]:
                                if necessity*2+necessityOfBomb>=8 and len(firstofChoice[2])>0:
                                    if firstofChoice[2][0] <= 12:
                                        semifinalList[firstofChoice[2][0]] = 4
                                    elif firstofChoice[2][0] == 13:
                                        semifinalList[13] = 1
                                        semifinalList[14] = 1
                                else:
                                    if necessity>=3:
                                        semifinalList=firstofChoice[1][-1]
                                    else:
                                        semifinalList=firstofChoice[1][0]
                            else:
                                if necessity*2+necessityOfBomb>=7 and len(firstofChoice[2])>0:
                                    if firstofChoice[2][0] <= 12:
                                        semifinalList[firstofChoice[2][0]] = 4
                                    elif firstofChoice[2][0] == 13:
                                        semifinalList[13] = 1
                                        semifinalList[14] = 1
                                else:
                                    if typeOfCard==11:
                                        if necessity >= 3:
                                            semifinalList = firstofChoice[1][-1]
                                        else:
                                            semifinalList = firstofChoice[1][0]
                                    elif typeOfCard==12:
                                        if necessity >= 3 or len(firstofChoice[1])==1:
                                            semifinalList = firstofChoice[1][-1]
                                            c=size(semifinalList)//3
                                            selectList=minusing(myList,semifinalList)
                                            k=[]
                                            for i in range(13):
                                                if selectList[i]==1 and semifinalList[i]==0:
                                                    k.append(i)
                                                    c=c-1
                                                if c==0:
                                                    break
                                            if c>0:
                                                for i in range(13):
                                                    if selectList[i]>1 and selectList[i]!=4 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                            if c>0 and len(firstofChoice[2])>0:
                                                semifinalList = []
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if firstofChoice[2][0] <= 12:
                                                    semifinalList[firstofChoice[2][0]] = 4
                                                elif firstofChoice[2][0] == 13:
                                                    semifinalList[13] = 1
                                                    semifinalList[14] = 1
                                            elif c>0:
                                                for i in range(13,15):
                                                    if selectList[i]==1:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                                for j in k:
                                                    semifinalList[j]=1
                                            elif c==0:
                                                for j in k:
                                                    semifinalList[j]=1
                                        else:
                                            if len(firstofChoice[1])>1:
                                                semifinalList = firstofChoice[1][0]
                                                c = size(semifinalList) // 3
                                                selectList = minusing(myList, semifinalList)
                                                k = []
                                                for i in range(13):
                                                    if selectList[i] == 1 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                                if c > 0 and len(firstofChoice[2]) > 0:
                                                    semifinalList = []
                                                    for i in range(15):
                                                        semifinalList.append(0)
                                                    if firstofChoice[2][0] <= 11:
                                                        semifinalList[firstofChoice[2][0]] = 4
                                                elif c==0:
                                                    for j in k:
                                                        semifinalList[j] = 1
                                    elif typeOfCard==13:
                                        semifinalList=[]
                                        for i in range(15):
                                            semifinalList.append(0)
                                        if necessity >= 3 or len(firstofChoice[1])==1:
                                            semifinalList = firstofChoice[1][-1]
                                            c=size(semifinalList)//3
                                            selectList=minusing(myList,semifinalList)
                                            k=[]
                                            for i in range(13):
                                                if selectList[i]==2 and semifinalList[i]==0:
                                                    k.append(i)
                                                    c=c-1
                                                if c==0:
                                                    break
                                            if c>0:
                                                for i in range(13):
                                                    if selectList[i]>2 and selectList[i]!=4 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                            if c>0 and len(firstofChoice[2])>0:
                                                semifinalList = []
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if firstofChoice[2][0] <= 12:
                                                    semifinalList[firstofChoice[2][0]] = 4
                                                elif firstofChoice[2][0] == 13:
                                                    semifinalList[13] = 1
                                                    semifinalList[14] = 1
                                            elif c==0:
                                                for j in k:
                                                    semifinalList[j]=1
                                        else:
                                            if len(firstofChoice[1])>1:
                                                semifinalList = firstofChoice[1][0]
                                                c = size(semifinalList) // 3
                                                selectList = minusing(myList, semifinalList)
                                                k = []
                                                for i in range(13):
                                                    if selectList[i] == 2 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                                if c > 0 and len(firstofChoice[2]) > 0:
                                                    semifinalList = []
                                                    for i in range(15):
                                                        semifinalList.append(0)
                                                    if firstofChoice[2][0] <= 12:
                                                        semifinalList[firstofChoice[2][0]] = 4
                                                elif c==0:
                                                    for j in k:
                                                        semifinalList[j] = 2
                                    else:
                                        tmpsin=single_analyse(myList)
                                        tmppair=pair_analyse(myList)
                                        tmpsinUltra=[]
                                        for i in range(13):
                                            if myList[i]==1:
                                                tmpsinUltra.append(i)
                                        tmppairUltra=[]
                                        for i in range(13):
                                            if myList[i]==2:
                                                tmppairUltra.append(i)
                                        tmptriUltra=[]
                                        for i in range(13):
                                            if myList[i]==3:
                                                tmptriUltra.append(i)
                                        if typeOfCard==14:
                                            if necessityOfBomb>=1 and firstofChoice[2][0]<13:
                                                semifinalList[firstofChoice[2][0]]=4
                                            elif necessityOfBomb>=2 and king_analyse(myList)==[1,1]:
                                                semifinalList[13]=1
                                                semifinalList[14]=1
                                        elif typeOfCard==15:
                                            c0=lengthOfCard//6
                                            if len(tmpsinUltra)>=2*c0:
                                                semifinalList=firstofChoice[1][0]
                                                for k in range(2*c0):
                                                    semifinalList[tmpsinUltra[k]]=1
                                            elif len(tmpsinUltra)>c0 and len(tmpsinUltra)+len(tmppairUltra)>=2*c0:
                                                semifinalList = firstofChoice[1][0]
                                                ss=2*c0
                                                for i in tmpsinUltra:
                                                    semifinalList[i]=1
                                                    ss=ss-1
                                                for i in range(ss):
                                                    semifinalList[tmppairUltra[i]]=1
                                            else:
                                                semifinalList=[]
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if necessityOfBomb>=1 and necessity>0:
                                                    semifinalList[bomb_analyse(myList)[0]]=4
                                        elif typeOfCard==16:
                                            c0 = lengthOfCard // 8
                                            if len(tmppairUltra) >= 2 * c0:
                                                semifinalList = firstofChoice[1][0]
                                                for i in range(2*c0):
                                                    semifinalList[tmppairUltra[i]] = 2
                                            else:
                                                semifinalList = []
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if necessityOfBomb >= 1 and necessity > 0:
                                                    semifinalList[bomb_analyse(myList)[0]] = 4
                    else:
                        if necessityOfBomb==3 and len(firstofChoice[2])>0:
                            if firstofChoice[2][0] <= 12:
                                semifinalList[firstofChoice[2][0]] = 4
                            elif firstofChoice[2][0] == 13:
                                semifinalList[13] = 1
                                semifinalList[14] = 1
                        else:
                            if typeOfCard not in [11,12,13,14,15,16]:
                                if necessity*2+necessityOfBomb>=8 and len(firstofChoice[2])>0:
                                    if firstofChoice[2][0] <= 12:
                                        semifinalList[firstofChoice[2][0]] = 4
                                    elif firstofChoice[2][0] == 13:
                                        semifinalList[13] = 1
                                        semifinalList[14] = 1
                                else:
                                    semifinalList=firstofChoice[1][0]
                            else:
                                if necessity*2+necessityOfBomb>=7 and len(firstofChoice[2])>0:
                                    if firstofChoice[2][0] <= 12:
                                        semifinalList[firstofChoice[2][0]] = 4
                                    elif firstofChoice[2][0] == 13:
                                        semifinalList[13] = 1
                                        semifinalList[14] = 1
                                else:
                                    if typeOfCard==11:
                                        if necessity >= 3:
                                            semifinalList = firstofChoice[1][-1]
                                        else:
                                            semifinalList = firstofChoice[1][0]
                                    elif typeOfCard==12:
                                        if necessity >= 3 or len(firstofChoice[1])==1:
                                            semifinalList = firstofChoice[1][-1]
                                            c=size(semifinalList)//3
                                            selectList=minusing(myList,semifinalList)
                                            k=[]
                                            for i in range(13):
                                                if selectList[i]==1 and semifinalList[i]==0:
                                                    k.append(i)
                                                    c=c-1
                                                if c==0:
                                                    break
                                            if c>0:
                                                for i in range(13):
                                                    if selectList[i]==2 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                            if c>0 and len(firstofChoice[2])>0:
                                                semifinalList = []
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if firstofChoice[2][0] <= 11:
                                                    semifinalList[firstofChoice[2][0]] = 4
                                            elif c==0:
                                                for j in k:
                                                    semifinalList[j]=1
                                        else:
                                            if len(firstofChoice[1])>1:
                                                semifinalList = firstofChoice[1][0]
                                                c = size(semifinalList) // 3
                                                selectList = minusing(myList, semifinalList)
                                                k = []
                                                for i in range(13):
                                                    if selectList[i] == 1 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                                if c > 0 and len(firstofChoice[2]) > 0:
                                                    semifinalList = []
                                                    for i in range(15):
                                                        semifinalList.append(0)
                                                    if firstofChoice[2][0] <= 11:
                                                        semifinalList[firstofChoice[2][0]] = 4
                                                elif c==0:
                                                    for j in k:
                                                        semifinalList[j] = 1
                                    elif typeOfCard==13:
                                        if necessity >= 3 or len(firstofChoice[1])==1:
                                            semifinalList = firstofChoice[1][-1]
                                            c=size(semifinalList)//3
                                            selectList=minusing(myList,semifinalList)
                                            k=[]
                                            for i in range(13):
                                                if selectList[i]==2 and semifinalList[i]==0:
                                                    k.append(i)
                                                    c=c-1
                                                if c==0:
                                                    break
                                            if c==1:
                                                for i in range(13):
                                                    if selectList[i]>2 and selectList[i]!=4 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                            if c>0 and len(firstofChoice[2])>0:
                                                semifinalList = []
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if firstofChoice[2][0] <= 12:
                                                    semifinalList[firstofChoice[2][0]] = 4
                                                elif firstofChoice[2][0] == 13:
                                                    semifinalList[13] = 1
                                                    semifinalList[14] = 1
                                            elif c==0:
                                                for j in k:
                                                    semifinalList[j]=2
                                        else:
                                            if len(firstofChoice[1])>1:
                                                semifinalList = firstofChoice[1][0]
                                                c = size(semifinalList) // 3
                                                selectList = minusing(myList, semifinalList)
                                                k = []
                                                for i in range(13):
                                                    if selectList[i] == 2 and semifinalList[i] == 0:
                                                        k.append(i)
                                                        c = c - 1
                                                    if c == 0:
                                                        break
                                                if c==1:
                                                    for i in range(13):
                                                        if selectList[i]==3 and semifinalList[i] == 0:
                                                            k.append(i)
                                                            c = c - 1
                                                        if c == 0:
                                                            break
                                                if c > 0 and len(firstofChoice[2]) > 0:
                                                    semifinalList = []
                                                    for i in range(15):
                                                        semifinalList.append(0)
                                                    if firstofChoice[2][0] <= 12:
                                                        semifinalList[firstofChoice[2][0]] = 4
                                                elif c==0:
                                                    for j in k:
                                                        semifinalList[j] = 2
                                    else:
                                        tmpsin=single_analyse(myList)
                                        tmppair=pair_analyse(myList)
                                        tmpsinUltra=[]
                                        for i in range(13):
                                            if myList[i]==1:
                                                tmpsinUltra.append(i)
                                        tmppairUltra=[]
                                        for i in range(13):
                                            if myList[i]==2:
                                                tmppairUltra.append(i)
                                        tmptriUltra=[]
                                        for i in range(13):
                                            if myList[i]==3:
                                                tmptriUltra.append(i)
                                        if typeOfCard==14:
                                            if necessityOfBomb>=1 and firstofChoice[2][0]<13:
                                                semifinalList[firstofChoice[2][0]]=4
                                            elif necessityOfBomb>=2 and king_analyse(myList)==[1,1]:
                                                semifinalList[13]=1
                                                semifinalList[14]=1
                                        elif typeOfCard==15:
                                            c0=lengthOfCard//6
                                            if len(tmpsinUltra)>=2*c0:
                                                semifinalList=firstofChoice[1][0]
                                                for k in range(2*c0):
                                                    semifinalList[tmpsinUltra[k]]=1
                                            elif len(tmpsinUltra)>c0 and len(tmpsinUltra)+len(tmppairUltra)>=2*c0:
                                                semifinalList = firstofChoice[1][0]
                                                ss=2*c0
                                                for i in tmpsinUltra:
                                                    semifinalList[i]=1
                                                    ss=ss-1
                                                for i in range(ss):
                                                    semifinalList[tmppairUltra[i]]=1
                                            else:
                                                semifinalList=[]
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if necessityOfBomb>=1 and necessity>0:
                                                    semifinalList[bomb_analyse(myList)[0]]=4
                                        elif typeOfCard==16:
                                            c0 = lengthOfCard // 8
                                            if len(tmppairUltra) >= 2 * c0:
                                                semifinalList = firstofChoice[1][0]
                                                for i in range(2*c0):
                                                    semifinalList[tmppairUltra[i]] = 2
                                            else:
                                                semifinalList = []
                                                for i in range(15):
                                                    semifinalList.append(0)
                                                if necessityOfBomb >= 1 and necessity > 0:
                                                    semifinalList[bomb_analyse(myList)[0]] = 4

    if robotID==0:
        if size(finalListOfAnswer11)!=0:
            finalListOfAnswer=finalListOfAnswer11
        else:
            finalListOfAnswer=semifinalList
    elif robotID==1:
        if size(finalListOfAnswer11)!=0:
            finalListOfAnswer=finalListOfAnswer11
        else:
            finalListOfAnswer=semifinalList
        totalList=[]
        for i in range(15):
            totalList.append(0)
        if size(inputList1)==0 and size(inputList2)==0:
            if numberRemainedUpUp==2 and numberRemainedUp>=2:
                if size(finalListOfAnswer)>2:
                    k=0
                    for i in range(13):
                        if myList[i]<=3:
                            k=i
                            break
                    if myList[k]==1:
                        totalList[k]=1
                        finalListOfAnswer=totalList
                    elif myList[k]>1:
                        totalList[k]=2
                        finalListOfAnswer = totalList
            elif numberRemainedUpUp==1:
                if size(finalListOfAnswer)>1:
                    k=0
                    for i in range(13):
                        if myList[i]<=3:
                            k=i
                            break
                    totalList[k]=1
                    finalListOfAnswer = totalList
        elif size(inputList1)==0 and size(inputList2)>0:
            if numberRemainedUpUp<=2:
                finalListOfAnswer=totalList
            elif 4 in finalListOfAnswer:
                finalListOfAnswer=totalList
            elif finalListOfAnswer[13]==1 and finalListOfAnswer[14]==1:
                finalListOfAnswer=totalList
    else:
        if size(finalListOfAnswer11)!=0:
            finalListOfAnswer=finalListOfAnswer11
        else:
            finalListOfAnswer=semifinalList
        totalList=[]
        for i in range(15):
            totalList.append(0)
        if size(inputList1)>0:
            if 4 in finalListOfAnswer:
                finalListOfAnswer=totalList
            elif finalListOfAnswer[13]==1 and finalListOfAnswer[14]==1:
                finalListOfAnswer=totalList
            elif numberRemainedUp<=2 and size(inputList1)>2:
                finalListOfAnswer=totalList
    finalop=finalOutput(my_now_position_list,finalListOfAnswer)
    print(json.dumps({"response":finalop}))
except:
    if size(inputList1)==0 and size(inputList2)==0:
        for i in range(15):
            if len(my_now_position_list[i])!=0:
                print(json.dumps({"response": my_now_position_list[i]}))
                break
    else:
        print(json.dumps({"response": []}))

