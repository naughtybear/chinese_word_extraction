"""
繼承pytorch的dataset
"""
import torch
from torch.utils.data import Dataset
from transformers import BertTokenizer  # bert斷詞，以字為單位
import pickle


class QADataset(Dataset):
    def __init__(self, tokenizer):
        """
        ipnut:
          tokenizer: 使用何種tokenizer
        """
        (self.full_question, self.tokenized_question, self.labeled_key,) = pickle.load(
            open("./pickle/train_data.pkl", "rb")
        )

        self.label2idx = {"O": 0, "B": 1, "I": 2}
        self.tokenizer = tokenizer
        self.len = len(self.tokenized_question)
        # print(self.key)

    def __getitem__(self, idx):
        """
        ipnut:
          idx:要的是第幾筆的資料
        output:
          question_ids: 將以斷詞的問題轉換成
          key_ids: 將標記後的結果轉換成對應的數字後輸出
        """
        question_ids = self.tokenizer.convert_tokens_to_ids(
            self.tokenized_question[idx]
        )

        mask_ids = [float(i > 0) for i in question_ids]

        key_ids = []
        for token in self.labeled_key[idx]:
            key_ids.append(self.label2idx[token])

        return (
            torch.tensor(question_ids, dtype=torch.long),
            torch.tensor(mask_ids, dtype=torch.long),
            torch.tensor(key_ids, dtype=torch.long),
            self.tokenized_question[idx],
            self.full_question[idx],
        )

    def __len__(self):
        """
        output: data總共有多少筆
        """
        return self.len


if __name__ == "__main__":
    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    dataset = QADataset(tokenizer=tokenizer)
    for i in range(20):
        print("------------")
        print(i)
        print(dataset.__getitem__(i)[0])
        # print(dataset.__getitem__(0))
