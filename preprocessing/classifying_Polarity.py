from BERTClassifier import BERTClassifier  # BERTClassifier.py가 Colab 환경에 업로드된 후 임포트
from kobert_transformers import get_kobert_model, get_tokenizer
import torch
import numpy as np

csv_file = "/content/review_data_fin.csv"  # 업로드된 CSV 파일 경로
bert_classifier_file = "/content/BERTClassifier.py"  # 업로드된 BERTClassifier.py 경로
model_file = "/content/best_kobert_model_of_shop_review.pth"  # 업로드된 모델 파일 경로


# 모델 및 토크나이저 설정
bert_model = get_kobert_model()
model = BERTClassifier(bert=bert_model)
model.load_state_dict(torch.load(model_file, map_location=torch.device('cpu')))  # 업로드된 모델 파일을 사용
model.eval()  # 평가 모드로 설정

# 토크나이저 설정
tokenizer = get_tokenizer()

class Classifying_Polarity():

  def analyze_content(text, model, tokenizer, max_len=128, device='cpu'):
      # 입력 텍스트 토큰화 및 인코딩
      inputs = tokenizer(
          text,
          return_tensors='pt',
          truncation=True,
          padding='max_length',
          max_length=max_len,
          add_special_tokens=True
      )

      # 입력 텐서 추출
      input_ids = inputs['input_ids'].to(device)
      token_type_ids = inputs['token_type_ids'].to(device)
      attention_mask = inputs['attention_mask'].to(device)

      # 모델을 평가 모드로 설정하고 기울기 계산 비활성화
      model.to(device)
      model.eval()
      with torch.no_grad():
          # 모델에 입력을 통과시켜 예측 값 출력
          output = model(input_ids, attention_mask, token_type_ids)

          logits = output[0] if isinstance(output, tuple) else output

          # CPU로 이동 후 NumPy로 변환
          logits = logits.cpu().numpy()
          prediction = np.argmax(logits, axis=1) if logits.ndim == 2 else np.argmax(logits)

      return prediction