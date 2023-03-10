from Encoder import Encoder as encoder
from Decoder import Decoder as decoder
from tensorflow.keras import layers as ksl
import tensorflow as tf
class model:
    def __init__(self,inputSize,decoderVocabSize,latentDim = 256):
        self.inputSize = inputSize
        self.latentDim = latentDim
        self.decoderVocabSize = decoderVocabSize
    def buildModel(self):
        encoderInput = ksl.Input(self.inputSize[0])
        x = ksl.Embedding(self.inputSize[0],
                        self.latentDim,
                        mask_zero=False)(encoderInput)
        x = ksl.BatchNormalization()(x)
        encoderOutput = encoder()(x)

        decoderInput = ksl.Input(self.inputSize[0])
        x  = ksl.Embedding(self.decoderVocabSize,
                           self.latentDim,
                           mask_zero = False)(decoderInput)
        x = decoder()([x,encoderOutput])
        x = ksl.BatchNormalization()(x)
        x = ksl.Dense(self.decoderVocabSize,activation = 'softmax')(x)
        model = tf.keras.Model([encoderInput,decoderInput],x)
        return model
    def compileModel(self):
        from tensorflow.keras import optimizers as optim
        opt = optim.SGD(lr=0.1)  
        Loss = tf.keras.losses.SparseCategoricalCrossentropy()
        self.net.compile(optimizer = opt,loss = Loss,
                         metrics = ['accuracy'])
        self.net.summary()    
    def trainModel(self,trainData,batchSize = 128,epochs = 10,validationData = None):
        self.net.fit(trainData[:-1],trainData[-1],epochs = epochs,batch_size=batchSize,
                     validation_data = validationData)
    def saveModel(self,addr):
        self.net.save_model(addr)
    def plotHistory(self):
        from matplotlib import pyplot as plt
        plt.plot(self.hist['accuracy'])
        plt.plot(self.hist['val_accuracy'])
        plt.title('Model accuracy')
        plt.show()
        plt.plot(self.hist['loss'])
        plt.plot(self.hist['val_loss'])
        plt.title('Model losses')