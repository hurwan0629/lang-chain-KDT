# AI 기술들에 대한 간단한 정리
## LLM
`Large Language Model`로, 텍스트를 여러 차원의 벡터로 임베딩하여 단어(토큰)간의 관계를 설정하고, 문장에서 다음 문장에 올 단어의 확률을 예측하는 모델

## CNN
`Concolutioinial Neural Network`로 합성곱 신경망이라는 뜻. 이미지/영상 공간 구조가 있는 데이터를 잘 처리하는 신경망 구조. LeCun 계열의 문서 인식 연구에서 대표적으로 알려짐

## RAG
`Retrieval-Augmented Generation`로 모델이 바로 답하지 않고, 문서/DB를 검색한 뒤 그 내용을 근거로 답하게 하는 방식. 원 논문에서는 사전학습 모델의 내부 지식과 외부 검색 인덱스를 결합

## LBM
`Large Behavior Model`로 대중적으로 고정된 단어는 아니지만 로봇의 센서 데이터와 명령쪽을 받아 출력하는 모델 계열

## GAN
`Generative Adversarial Networks`로 적대적 생성 신경망이라는 뜻. 두개의 인공지능이 서로 경쟁하며 실제와 같은 가짜 데이터를 만들어내는 머신러닝 프레임워크 (위조범과 판별자의 경쟁 같은 느낌)

## VAE
`Variational Autoencoder`을 뜻하는 변분 오토 인코더로 입력 데이터를 압축하여 핵십 특징만 담긴 확률 분포로 변환

## VLM
`Vision-Language Model`으로 이미지 설명과 시각 질의응답을 하는 모델

## LoRA
적은 파라미터만 학습해 비용 절감  