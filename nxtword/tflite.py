import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import os


class NextWordPredictor:

    def __init__(self, vocab_size=10000, max_sequence_len=30):
        self.vocab_size = vocab_size
        self.max_sequence_len = max_sequence_len
        self.tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
        self.model = None

    def prepare_data(self, texts):
        self.tokenizer.fit_on_texts(texts)
        input_sequences = []
        for text in texts:
            token_list = self.tokenizer.texts_to_sequences([text])[0]
            for i in range(1, len(token_list)):
                n_gram_sequence = token_list[:i+1]
                input_sequences.append(n_gram_sequence)
        padded_sequences = pad_sequences(input_sequences,
                                         maxlen=self.max_sequence_len,
                                         padding='pre')
        X = padded_sequences[:, :-1]
        y = padded_sequences[:, -1]
        y = tf.keras.utils.to_categorical(y, num_classes=self.vocab_size)
        return X, y

    def build_model(self, embedding_dim=100):
        self.model = Sequential([
            Embedding(self.vocab_size, embedding_dim,
                      input_length=self.max_sequence_len-1),
            LSTM(150, return_sequences=True),
            LSTM(100),
            Dense(self.vocab_size, activation='softmax')
        ])

        self.model.compile(loss='categorical_crossentropy',
                           optimizer='adam',
                           metrics=['accuracy'])

    def train(self, X, y, epochs=50, batch_size=64, validation_split=0.2):
        if self.model is None:
            raise ValueError("Model not built. Call build_model first.")

        history = self.model.fit(X, y,
                                 epochs=epochs,
                                 batch_size=batch_size,
                                 validation_split=validation_split)
        return history

    def convert_to_tflite(self, output_path='next_word_model.tflite'):
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        tflite_model = converter.convert()
        with open(output_path, 'wb') as f:
            f.write(tflite_model)

    def predict_next_word(self, text, n_words=5):
        interpreter = tf.lite.Interpreter(model_path='next_word_model.tflite')
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()   
        token_list = self.tokenizer.texts_to_sequences([text])[0]
        token_list = pad_sequences([token_list],
                                   maxlen=self.max_sequence_len-1,
                                   padding='pre')
        interpreter.set_tensor(input_details[0]['index'], token_list)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])
        top_n = np.argsort(predictions[0])[-n_words:][::-1]
        predicted_words = []
        for idx in top_n:
            for word, index in self.tokenizer.word_index.items():
                if index == idx:
                    predicted_words.append(word)
                    break

        return predicted_words
