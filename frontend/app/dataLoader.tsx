import RNFS from "react-native-fs";

// Load text data from a file
export async function loadTextFile(): Promise<string> {
  const filePath = `${RNFS.DocumentDirectoryPath}/input.txt`;

  try {
    const exists = await RNFS.exists(filePath);
    if (!exists) {
      console.error("File not found:", filePath);
      return "";
    }
    const data = await RNFS.readFile(filePath, "utf8");
    return data;
  } catch (error) {
    console.error("Error reading text file:", error);
    return "";
  }
}

// Tokenize text into words
export function tokenizeText(text: string): string[] {
  return text.toLowerCase().replace(/[^a-zA-Z ]/g, "").split(" ");
}

// Generate training data (X, y)
export function generateTrainingData(words: string[], sequenceLength = 3) {
  let inputSequences: number[][] = [];
  let outputWords: number[] = [];
  let wordIndex: Record<string, number> = {};
  let indexWord: Record<number, string> = {};
  let index = 1;

  words.forEach((word) => {
    if (!(word in wordIndex)) {
      wordIndex[word] = index;
      indexWord[index] = word;
      index++;
    }
  });

  for (let i = 0; i < words.length - sequenceLength; i++) {
    let inputSeq = words.slice(i, i + sequenceLength).map((w) => wordIndex[w]);
    let output = wordIndex[words[i + sequenceLength]];
    inputSequences.push(inputSeq);
    outputWords.push(output);
  }

  return { inputSequences, outputWords, wordIndex, indexWord };
}
