import os
from openai import OpenAI
import json
import pandas as pd
from decouple import config
from tqdm import tqdm


class TextEmbedding:
    def __init__(self):
        self.client = OpenAI(
            organization=config('ORGANIZATION'),
            api_key=config('API_KEY'),
        )

    def get_embedding(self,text, model="text-embedding-ada-002"):
        text = text.replace("\n", " ")
        response = self.client.embeddings.create(input = [text], model=model)
        embedding_list = response.data[0].embedding
        return embedding_list

    def add_embedded_column_to_df(self, df, column_name_to_embed):
        if column_name_to_embed in df.columns:
            tqdm.pandas(desc="Computing embeddings")
            df['Embedding'] = df[column_name_to_embed].progress_apply(lambda x: self.get_embedding(x))
        else:
            raise ValueError(f"Column {column_name_to_embed} not found in DataFrame")

        return df