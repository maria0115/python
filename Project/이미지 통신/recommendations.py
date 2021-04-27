# Pearson correlation coefficient 
#from numpy import sqrt
from math import sqrt

# Euclidean Distance 
def sim_distance(prefs, person1, person2): 
    # 공통 항목 추출 
    si = dict() 
    
    for item in prefs[person1]: 
        if item in prefs[person2]: 
            si[item] = 1 
            
    # 공통 평가 항목이 없는 경우 0 리턴 
    if len(si) == 0: return 0 
    
    # person1의 item이 person2에서도 존재한다면, person1과 person2의 item 평점 차이의 제곱한 값을 더한 후 제곱 근을 계산 
    sum_of_squares = sum([(prefs[person1][item] - prefs[person2][item])**2 for item in prefs[person1] if item in prefs[person2]]) 
    
    return 1/(1+sqrt(sum_of_squares))

def sim_pearson(prefs, p1, p2): 
    # 같이 평가한 항목들의 목록을 구함 
    si = dict() 
    for item in prefs[p1]: 
        if item in prefs[p2]: 
            si[item] = 1 
    # 공통 항목 개수 
    n = len(si) 
    
    # 공통 항목이 없으면 0 리턴 
    if n==0: 
        return 0 
    # 모든 선호도를 합산 
    
    sum1 = sum([prefs[p1][it] for it in si]) 
    sum2 = sum([prefs[p2][it] for it in si])
    # 제곱의 합을 계산 
    sum1Sq = sum([(prefs[p1][it])**2 for it in si]) 
    sum2Sq = sum([(prefs[p2][it])**2 for it in si]) 
    # 곱의 합을 계산 
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si]) 
    # 피어슨 점수 계산
    num = pSum - (sum1*sum2/n) 
    den = sqrt((sum1Sq-pow(sum1,2)/n) * (sum2Sq-pow(sum2,2)/n)) 
    if den==0: 
        return 0 
    
    r = num/den 
    
    return r

# 선호도 dict에 최적의 상대편을 구함
# 결과 개수와 유사도 함수는 옵션
def top_matches(prefs, person, n=10, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other!=person]

    scores.sort()
    scores.reverse()
    return scores[:n]

# 다른 사람과의 순위의 가중 평균값을 이용해서 특정 사람을 추천
def get_recommendations(prefs, person, similarity=sim_pearson):
    totals = dict()
    simSums = dict()

    for other in prefs:
        # 나를 제외 하고
        if other == person: continue
        sim = similarity(prefs, person, other)  # person과 other 사이의 상관계수 점수를 구함

        # 0 이하 점수는 무시
        if sim<=0: continue

        for item in prefs[other]:   # ohter가 본 영화들의 list
            # 내가 보지 못한 영화만 대상
            if item not in prefs[person] or prefs[person][item] == 0:
                # 유사도 * 점수
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item]*sim  # other가 평가한 영화의 점수 * person과 other의 상관계수

                # 유사도 합계
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # 정규화된 목록 생성
    rankings = [ (total/simSums[item], item) for item, total in totals.items() ]

    # 정렬된 목록 리턴
    rankings.sort()
    rankings.reverse()
    return rankings

# 사람을 제품 기준으로 dict 변경
def transform_prefs(prefs):
    result = dict()

    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, dict())

            result[item][person] = prefs[person][item]

    return result
