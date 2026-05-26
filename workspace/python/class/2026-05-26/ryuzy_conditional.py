print("MBTI 간단 성격 유형 검사에 오신 걸 환영합니다!")

# 첫 번째 질문: 외향/내향
answer1 = input("Q1. 새로운 사람들과 만나는 걸 좋아하시나요? (y/n): ")
if answer1.lower() == 'y':
    # 외향형으로 진행
    print("외향형으로 분석 중...")
    answer2 = input("Q2. 주변 환경에 대해 자주 인지하고 있나요? (y/n): ")
    
    if answer2.lower() == 'y':
        # 감각형(외향, 감각)
        answer3 = input("Q3. 계획을 세우는 것을 좋아하시나요? (y/n): ")
        if answer3.lower() == 'y':
            print("당신의 성격 유형은 ESTJ입니다!")
        else:
            print("당신의 성격 유형은 ESFP입니다!")
    else:
        # 직관형(외향, 직관)
        answer3 = input("Q3. 큰 그림을 보는 것을 좋아하시나요? (y/n): ")
        if answer3.lower() == 'y':
            print("당신의 성격 유형은 ENFP입니다!")
        else:
            print("당신의 성격 유형은 ENTJ입니다!")
                
else:
    # 내향형으로 진행
    print("내향형으로 분석 중...")
    answer2 = input("Q2. 구체적인 정보나 사실을 중요하게 생각하시나요? (y/n): ")
    
    if answer2.lower() == 'y':
        # 감각형(내향, 감각)
        answer3 = input("Q3. 일정을 엄격하게 관리하는 것을 좋아하시나요? (y/n): ")
        if answer3.lower() == 'y':
            print("당신의 성격 유형은 ISTJ입니다!")
        else:
            print("당신의 성격 유형은 ISFP입니다!")
    else:
        # 직관형(내향, 직관)
        answer3 = input("Q3. 논리적인 문제 해결을 좋아하시나요? (y/n): ")
        if answer3.lower() == 'y':
            print("당신의 성격 유형은 INTP입니다!")
        else:
            print("당신의 성격 유형은 INFJ입니다!")