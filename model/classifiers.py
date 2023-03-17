import re
import random

import torch
import torch.nn.functional as F
from torch import nn
from transformers import AutoTokenizer, AutoModelForMaskedLM
from tokenizers import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing

import textdistance as td
import nltk

nltk.download("stopwords")

regextokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
stemmer = nltk.stem.PorterStemmer()

emotions = ['fear', 'love', 'instability', 'disgust', 'disappointment',
          'shame', 'anger', 'jealous', 'sadness', 'envy', 'joy', 'guilt']
emotion2int = dict(zip(emotions, list(range(len(emotions)))))

labels = ['not_s', 's']
label2int = dict(zip(labels, list(range(len(labels)))))

class ClassificationModel(nn.Module):
    def __init__(self, base_model, n_classes, base_model_output_size=768, dropout=0.05):
        super().__init__()
        self.base_model = base_model
        
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(base_model_output_size, base_model_output_size),
            nn.Mish(),
            nn.Dropout(dropout),
            nn.Linear(base_model_output_size, n_classes)
        )
        
        for layer in self.classifier:
            if isinstance(layer, nn.Linear):
                layer.weight.data.normal_(mean=0.0, std=0.02)
                if layer.bias is not None:
                    layer.bias.data.zero_()

    def forward(self, input_):
        X, attention_mask = input_
        hidden_states = self.base_model(X, attention_mask=attention_mask)
        
        return self.classifier(hidden_states[0][:, 0, :])

with torch.no_grad():
  emo_model = ClassificationModel(AutoModelForMaskedLM.from_pretrained("roberta-base").base_model, len(emotions))
  emo_model.load_state_dict(torch.load('RoBERTa_12_emotions.pt', map_location=torch.device('cpu')))
  s_model = ClassificationModel(AutoModelForMaskedLM.from_pretrained("roberta-base").base_model, len(labels))
  s_model.load_state_dict(torch.load('RoBERTa_s_intention.pt', map_location=torch.device('cpu')))

def get_classification(text, model_type):
  text = re.sub(r'[^\w\s]', '', text)
  text = text.lower()

  t = ByteLevelBPETokenizer(
            "tokenizer/vocab.json",
            "tokenizer/merges.txt"
        )
  t._tokenizer.post_processor = BertProcessing(
            ("</s>", t.token_to_id("</s>")),
            ("<s>", t.token_to_id("<s>")),
        )
  t.enable_truncation(512)
  t.enable_padding(pad_id=t.token_to_id("<pad>"))
  tokenizer = t

  encoded = tokenizer.encode(text)
  sequence_padded = torch.tensor(encoded.ids).unsqueeze(0)
  attention_mask_padded = torch.tensor(encoded.attention_mask).unsqueeze(0)
   
  if model_type == "emo":
      output = emo_model((sequence_padded, attention_mask_padded))
      _, top_class = output.topk(1, dim=1)
      label = int(top_class[0][0])
      label_map = {v: k for k, v in emotion2int.items()}
  else:
      output = s_model((sequence_padded, attention_mask_padded))
      top_p, top_class = output.topk(1, dim=1)
      label = int(top_class[0][0])
      label_map = {v: k for k, v in label2int.items()}

  return label_map[label]

def get_distance(s_1, s_2):
    """
    Computes a distance score between utterances calculated as the overlap
    distance between unigrams, plus the overlap distance squared over bigrams,
    plus the overlap distance cubed over trigrams, etc (up to a number of ngrams
    equal to the length of the shortest utterance)
    """
    s_1 = re.sub(r'[^\w\s]', '', s_1.lower())  #preprocess
    s_2 = re.sub(r'[^\w\s]', '', s_2.lower())
    s1_ws = regextokenizer.tokenize(s_1)  #tokenize to count tokens later
    s2_ws = regextokenizer.tokenize(s_2)
    max_n = len(s1_ws) if len(s1_ws) < len(s2_ws) else len(s2_ws)
    ngram_scores = []
    for i in range(1, max_n + 1):
        s1grams = nltk.ngrams(s_1.split(), i)
        s2grams = nltk.ngrams(s_2.split(), i)
        ngram_scores.append((td.overlap.normalized_distance(s1grams,
                                                            s2grams))**i)
    normalised_dis = sum(ngram_scores) / (max_n)  #normalised
    return normalised_dis

def compute_distances(sentence, dataframe):
    """
    Computes a list of distances score between an utterance and all the
    utterances in a dataframe
    """
    distances = []
    for index, _ in dataframe.iterrows():
        df_s = dataframe['sentences'][
            index]  #assuming the dataframe column is called 'sentences'
        distance = get_distance(df_s.lower(), sentence)
        distances.append(distance)
    return distances

def novelty_score(sentence, dataframe):
    """
    Computes the mean of the distances beween an utterance
    and each of the utterances in a given dataframe
    """
    if dataframe.empty:
        score = 1.0
    else:
        d_list = compute_distances(sentence, dataframe)
        d_score = sum(d_list)
        score = d_score / len(d_list)
    return round(score, 2)

def get_sentence_score(sentence, dataframe):
    """
    Calculates how fit a sentence is based on its weighted empathy, fluency
    and novelty values
    """
    scores = sentence.split('<')[1].split('>')[0]
    empathy = float(scores.split(',')[0])
    fluency = float(scores.split(', ')[1])
    novelty = novelty_score(sentence, dataframe)
    score = empathy + 0.75 * fluency + 2 * novelty
    return score
