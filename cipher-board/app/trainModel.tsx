import { useEffect, useState } from "react";
import { View, Text, Button } from "react-native";
import * as tf from "@tensorflow/tfjs-react-native";
import { loadTextFile, tokenizeText, generateTrainingData } from "./dataLoader";
import RNFS from "react-native-fs";

// Load and train the model
export default function TrainModel() {
  const [training, setTraining] = useState(false);
  const [modelSaved, setModelSaved] = useState(false);
  const modelPath = `${RNFS.DocumentDirectoryPath}/trained_model.tflite`;

  useEffect(() => {
    const initTF = async () => {
      await tf.ready();
      console.log("TensorFlow.js Ready!");
    };
    initTF();
  }, []);

  const trainModel = async () => {
    setTraining(true);

    // Load text and preprocess it
    const text = await loadTextFile();
    const words = tokenizeText(text);
    const { inputSequences, outputWords, wordIndex } = generateTrainingData(words);

    // Convert data to tensors
    const xs = tf.tensor2d(inputSequences);
    const ys = tf.oneHot(tf.tensor1d(outputWords, "int32"), Object.keys(wordIndex).length);

    // Define model
    const model = tf.sequential();
    model.add(tf.layers.embedding({ inputDim: Object.keys(wordIndex).length, outputDim: 50 }));
    model.add(tf.layers.lstm({ units: 128, returnSequences: false }));
    model.add(tf.layers.dense({ units: Object.keys(wordIndex).length, activation: "softmax" }));

    model.compile({
      optimizer: "adam",
      loss: "categoricalCrossentropy",
      metrics: ["accuracy"],
    });

    // Train model
    await model.fit(xs, ys, {
      epochs: 10,
      batchSize: 16,
      callbacks: {
        onEpochEnd: (epoch, logs) => console.log(`Epoch ${epoch}: Loss = ${logs?.loss}`),
      },
    });

    console.log("Training complete!");

    // Save model locally
    const modelJSON = await model.save(tf.io.withSaveHandler(async (artifacts) => {
      const modelData = JSON.stringify(artifacts.modelTopology);
      await RNFS.writeFile(modelPath, modelData, "utf8");
      console.log("Model saved successfully!");
      setModelSaved(true);
    }));

    setTraining(false);
  };

  return (
    <View>
      <Text>Training Status: {training ? "Training..." : "Idle"}</Text>
      <Button title="Train Model" onPress={trainModel} disabled={training} />
      {modelSaved && <Text>✅ Model saved successfully!</Text>}
    </View>
  );
}
