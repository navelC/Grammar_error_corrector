class Encoder(tf.keras.Model):
    def __init__(self,inp_vocab_size,embedding_size,lstm_size,input_length):
        super().__init__()
        self.vocab_size = inp_vocab_size
        self.embedding_size = embedding_size
        self.lstm_units = lstm_size
        self.input_length = input_length


    def build(self, input_sequence):
        #self.embedding = Embedding(input_dim=self.vocab_size, output_dim=self.embedding_size, input_length=self.input_length, 
        #                           #embeddings_initializer=keras.initializers.Constant(in_embedding_matrix), mask_zero=True, 
        #                           weights = [in_embedding_matrix], mask_zero=True, 
        #                           trainable = False, name="embedding_layer_encoder")
        self.embedding = Embedding(input_dim=self.vocab_size, output_dim=self.embedding_size, input_length=self.input_length,
                           mask_zero=True, name="embedding_layer_encoder")
        self.lstm = LSTM(self.lstm_units, return_state=True, return_sequences=True, name="Encoder_LSTM")

    def call(self,input_sequence,states, training = True):
        input_embedding = self.embedding(input_sequence)   #(batch_size, length of input array, embedding_size)
        self.lstm_output, self.state_h, self.state_c = self.lstm(input_embedding, initial_state = states)         
        return self.lstm_output,self.state_h, self.state_c

    
    def initialize_states(self,batch_size):
      initializer = GlorotNormal()
      lstm_state_h = initializer(shape=(batch_size, self.lstm_units))#tf.zeros((batch_size, self.lstm_units), dtype=tf.dtypes.float32, name="Encoder_LSTM_hidden_state")
      lstm_state_c = initializer(shape=(batch_size, self.lstm_units))#tf.zeros((batch_size, self.lstm_units), dtype=tf.dtypes.float32, name="Encoder_LSTM_cell_state")
      return lstm_state_h, lstm_state_c

#DECODER
class Decoder(tf.keras.Model):
    def __init__(self,out_vocab_size,embedding_size,lstm_size,input_length):
        super().__init__()
        self.vocab_size = out_vocab_size
        self.embedding_size = embedding_size
        self.lstm_units = lstm_size
        self.input_length = input_length


    def build(self,input_sequence):
        #self.embedding = Embedding(input_dim=self.vocab_size, output_dim=self.embedding_size, input_length=self.input_length, 
        #                           #embeddings_initializer=keras.initializers.Constant(out_embedding_matrix), 
        #                           weights = [out_embedding_matrix], mask_zero=True, 
        #                           trainable = False, name="embedding_layer_decoder")
        self.embedding = Embedding(input_dim=self.vocab_size, output_dim=self.embedding_size, input_length=self.input_length,
                           mask_zero=True, name="embedding_layer_decoder") 
        self.lstm = LSTM(self.lstm_units, return_state=True, return_sequences=True, name="Decoder_LSTM")


    def call(self,input_sequence,initial_states, training = True):

        input_embedding = self.embedding(input_sequence)
        self.lstm_output, self.state_h, self.state_c = self.lstm(input_embedding, initial_state=initial_states)
        return self.lstm_output,self.state_h, self.state_c
class Encoder_decoder(tf.keras.Model):
    
    def __init__(self, encoder_inputs_length,decoder_inputs_length, output_vocab_size):

        super().__init__()
        self.encoder = Encoder(INPUT_VOCAB_SIZE, embedding_size = 256, lstm_size= 1200 , input_length= INPUT_ENCODER_LENGTH)
        self.decoder = Decoder(OUTPUT_VOCAB_SIZE, embedding_size = 256, lstm_size = 1200, input_length = None)
        self.dense = Dense(output_vocab_size)#, activation = 'softmax')
    
    def call(self,data):
        input, output = data[0], data[1]
        states = self.encoder.initialize_states(input.shape[0])
        encoder_output,encoder_final_state_h,encoder_final_state_c = self.encoder(input, states)
        decoder_output,decoder_state_h,decoder_state_c = self.decoder(output,[encoder_final_state_h,encoder_final_state_c])
        outputs = self.dense(decoder_output)

        return outputs
        