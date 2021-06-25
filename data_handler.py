import os
import pandas as pd
import numpy as np

class DataHandler:
    def __init__(self, csv_path) -> None:
        self.csv_path = csv_path
        self.df = pd.read_csv(self.csv_path)
        self.df['image_text'] = self.df['image_text'].astype(str)
        # print(self.df['image_text'].dtype)
        # print(self.df.iloc[2]['image_text'])
        if 'label' not in self.df.columns:
            self.df.insert(loc=5, column='label', value=np.nan)
    
    def get_data_on_row(self, idx):
        index = idx - 1
        result_dic = self.df.iloc[index].to_dict()
        # print(result_dic)
        # print(self.df.iloc[index].at['image_text'])
        return result_dic

    def set_label_on_row(self, idx, label):
        assert isinstance(label, int)
        index = idx - 1
        self.df.loc[index, 'label'] = label

    def set_image_text_on_row(self, idx, text):
        assert isinstance(text, str)
        index = idx - 1
        self.df.loc[index, 'image_text'] = text
        
    def save_dataframe(self):
        self.df.to_csv(self.csv_path, index=False)



if __name__ == '__main__':
    dh = DataHandler('./sample_data_test.csv')
    dic = dh.get_data_on_row(1)
    dh.set_label_on_row(1, 1)
    dh.save_dataframe()
    
    if np.isnan(dic['image_text']):
        print('yes')