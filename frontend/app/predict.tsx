import { useState } from "react";
import Tflite from "tflite-react-native";
import RNFS from "react-native-fs";

const tflite = new Tflite();
const modelPath = `${RNFS.DocumentDirectoryPath}/trained_model.tflite`;

export default function PredictNextWord(input: string, setRecommend: Function) {
  const [prediction, setPrediction] = useState("");

  const loadModel = async () => {
    return new Promise((resolve, reject) => {
      tflite.loadModel(
        { model: modelPath, numThreads: 1 },
        (err, res) => (err ? reject(err) : resolve(res))
      );
    });
  };

  const predictNextWord = async () => {
    await loadModel();

    tflite.runModelOnText(
      { text: input, numResults: 1 },
      (err, res) => {
        if (err) console.error(err);
        else setPrediction(res[0].label);
      }
    );
  };
  setRecommend(prediction);
}
