import torch
from torch import nn

class BERTClassifier(nn.Module):
  def __init__(self, bert, hidden_size=768, num_classes=2, dr_rate=None, params=None):
      super(BERTClassifier, self).__init__()
      self.bert = bert
      self.dr_rate = dr_rate

      # Use "regressor" instead of "classifier" to match the saved model
      self.regressor = nn.Linear(hidden_size, num_classes)
      if dr_rate:
          self.dropout = nn.Dropout(p=dr_rate)

  def gen_attention_mask(self, token_ids, valid_length):
    attention_mask = torch.zeros_like(token_ids)
    for i, v in enumerate(valid_length):
      attention_mask[i][:v] = 1
    return attention_mask.float()

  def forward(self, input_ids, attention_mask, token_type_ids):
      _, pooler_output = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids, return_dict=False)
      if self.dr_rate:
          out = self.dropout(pooler_output)
      else:
          out = pooler_output
      return self.regressor(out)  # Use "regressor" instead of "classifier"