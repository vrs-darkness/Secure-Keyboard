import { useEffect } from 'react';
import * as tf from '@tensorflow/tfjs-react-native';
import { TFLiteModel } from 'react-native-tensorflow-lite';

export default function Model() {
  useEffect(() => {
    const loadModel = async () => {
      await tf.ready(); // Ensure TensorFlow.js is initialized
      await tf.setBackend('cpu'); // Set to CPU backend
      try {
        // Replace with your actual model path, for example, 'assets/model.tflite'
        const model = await TFLiteModel.fromAsset('model.tflite');
        console.log('Model loaded:', model);
        // You can run inference on the model now.
      } catch (error) {
        console.error('Error loading model:', error);
      }
    };
    
    loadModel();
  }, []);
  return (
    <View>
      <Text>Model Loaded Successfully</Text>
    </View>
  );
}
