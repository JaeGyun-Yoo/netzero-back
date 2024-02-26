import openai

import openai

openai.api_key="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"

def post_to_gpt_test():
    response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "지금부터 너는 대기업에 근무하는 인사담당자야. 오늘은 면접관으로 역할을 할거야. 내가 자소서를 너한테 보내주면, 너는 그 직무에 맞는 질문을 생성해줘"},
                {"role": "user", "content": '경험 국민연금공단에서의 인턴 기간 동안, 기초연금 수령인의 수가 줄어들었던 문제에 직면하였습니다. 이 문제를 해결하고자 동료들과 협업하여 해결책을 찾았습니다. 여러 아이디어와 의견을 공유한 끝에 방문접수를 통해 수령인을 증가시키자는 결론을 도출하였고, 각자 역할을 분담하여 실행에 옮겼습니다.배운 점팀워크의 중요성: 이 경험을 통해 협업과 팀워크의 중요성을 깨달았습니다. 다양한 의견을 수렴하고 토론을 거친 끝에 팀 전체가 동의한 방향으로 나아가는 것은 성공적인 결과를 이루는 핵심입니다.결단력과 실행: 문제 해결을 위한 계획 수립 이후, 우리 팀은 실행 단계에서도 훌륭한 조화를 이뤘습니다. 결과적으로, 방문접수를 통해 전년도 대비 약 7%의 연금 수령인 증가를 달성하였습니다. 이것은 계획을 수립하고 실행하는 중요성을 강조합니다.이러한 경험을 통해, 팀워크, 실행능력, 그리고 문제 해결 능력을 향상시키고, 이러한 역량을 IBK에서도 팀과 협업하며 본 경험에서 얻은 교훈을 적극적으로 활용하여 성공적인 결과를 창출하고, 더 나아가 금융 분야에서의 경력을 향상시키기 위해 노력하겠습니다.대학생 대외활동 공모전 채용 사이트 링커리어 https://linkareer.com'}
                ],
        )
    output_text = response["choices"][0]["message"]["content"]
    return output_text


def post_to_gpt(system_content:str, user_content:str):
    print(f"\n\n\n\n\nsystem content: {system_content}\n\n\n\n")
    print(f"\n\n\n\n\n\nuser-content: {user_content}\n\n\n\n\n")
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{system_content}"},
                {"role": "user", "content": f"{user_content}"}
            ],
        )
    output_text = response["choices"][0]["message"]["content"]
    return output_text