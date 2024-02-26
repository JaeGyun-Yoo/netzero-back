  
# import openai

# openai.api_key="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"

# question_list=[]
# answer_list=[]
# cnt=0

# def post_to_gpt(system_content:str, user_content:str):
#     response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": f"{system_content}"},
#                 {"role": "user", "content": f"{user_content}"}
#             ],
#             temperature=0.5
#         )
#     output_text = response["choices"][0]["message"]["content"]
#     return output_text


# def train_gpt_as_interviewer(cover_letter:str):
#     interview_text=post_to_gpt("내가 다음으로 보내주는 자기소개서를 보고, 너가 면접관 역할을 해서 전공 관련 면접을 진행해줘. 전공 관련 질문 5개를 작성해서 1,2,3,4,5로 구분해줘.", cover_letter)
#     lines = interview_text.split("\n\n")
#     for line in lines:
#         if line[0].isdigit():
#             question_list.append(line)
#             answer_list.append(None)  # 추가: 질문에 대응되는 답변 자리를 None으로 만듭니다.
#     return question_list
    
    
# def get_question_from_gpt():
#     global cnt
#     cnt+=1
#     return post_to_gpt("너는 대기업에서 근무하는 면접관이야, 내가 보낸 질문 그대로 말해주면 돼", f"{question_list[cnt]}")
   


# def reply_to_gpt(reply:str):
#     answer_list.append(reply)
#     return post_to_gpt("너가 해준 질문에 대한 면접자의 대답을 알려줄테니까 꼬리질문이 필요하다고 생각이 들면 꼬리질문을 해주고, 너(면접관)가 보기에 지금까지 질문이 충분하다고 생각이 들면, \"종료\"라고 말해줘", reply)
    
# def get_feedback_from_gpt():
#     return post_to_gpt("지금까지 너가 질문한 질문들과, 그에 대한 피드백을 함께 작성해줘","실제 면접관 처럼 피드백을 줘")

# def get_question_answer_list():
#     return question_list, answer_list

# def test_to_gpt(test):
#     return post_to_gpt("지금 내가 보내줄거는 면접을 본 사용자의 감정 분석 결과야. 이에 대한 피드백을 너가 대기업 임원이라고 생각하고 남겨줘",test)


import openai

openai.api_key = "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"

question_list = []  # 질문 리스트
answer_list = []  # 답변 리스트
cnt = 0  # 현재 질문 번호

def post_to_gpt(system_content: str, user_content: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"{system_content}"},
            {"role": "user", "content": f"{user_content}"},
        ],
        temperature=0.5,
    )
    output_text = response["choices"][0]["message"]["content"]
    return output_text


def train_gpt_as_interviewer(cover_letter: str):
    interview_text = post_to_gpt(
        "내가 다음으로 보내주는 자기소개서를 보고, 너가 면접관 역할을 해서 전공 관련 면접을 진행해줘. 전공 관련 질문 5개를 작성해서 1,2,3,4,5로 구분해줘.",
        cover_letter,
    )
    lines = interview_text.split("\n\n")
    for line in lines:
        if line[0].isdigit():
            question_list.append(line)
            answer_list.append(None)  # 추가: 질문에 대응되는 답변 자리를 None으로 만듭니다.
    return question_list


def get_question_from_gpt():
    global cnt
    cnt += 1
    if cnt > len(question_list):
        return "면접이 종료되었습니다."
    return post_to_gpt(
        "너는 대기업에서 근무하는 면접관이야, 내가 보낸 질문 그대로 말해주면 돼", f"{question_list[cnt]}"
    )


def reply_to_gpt(reply: str):
    answer_list[cnt - 1] = reply  # 답변 리스트에 답변 저장
    
    # 꼬리질문 생성
    follow_up_question = post_to_gpt(
        "이전 질문에 대한 답변을 바탕으로 꼬리질문을 생성해줘.", reply
    )
    
    return post_to_gpt(
        "너가 해준 질문에 대한 면접자의 대답을 알려줄테니까 꼬리질문이 필요하다고 생각이 들면 꼬리질문을 해주고, 너(면접관)가 보기에 지금까지 질문이 충분하다고 생각이 들면, \"종료\"라고 말해줘",
        reply + "\n\n" + follow_up_question,
    )


def get_feedback_from_gpt(questions, answers):
    feedback_text = ""
    for question, answer in zip(questions, answers):
        feedback_text += f"질문: {question}\n"
        feedback_text += f"답변: {answer}\n\n"
    
    return post_to_gpt(
        "지금까지 진행된 면접 질문과 답변을 바탕으로 피드백을 작성해줘.", feedback_text
    )


def get_question_answer_list():
    return question_list, answer_list


def test_to_gpt(test):
    return post_to_gpt(
        "지금 내가 보내줄거는 면접을 본 사용자의 감정 분석 결과야. 이에 대한 피드백을 너가 대기업 임원이라고 생각하고 남겨줘",
        test,
    )

