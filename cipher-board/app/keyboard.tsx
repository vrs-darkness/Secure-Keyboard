import { Text, View, Dimensions, TextInput, TouchableOpacity, Image, StyleSheet, Vibration } from "react-native";
import React, { useState, useEffect } from 'react';
import { Int32 } from "react-native/Libraries/Types/CodegenTypes";
import Model from "./model";
import { LayersModel } from '@tensorflow/tfjs';

const { width, height } = Dimensions.get('window');  // Get the screen width and height

const Styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    flexDirection: 'column', // Align text input at the top and keyboard at the bottom
  },
  input: {
    width: '100%',
    padding: 10,
    backgroundColor: '#fff',
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#ccc',
    marginTop: 20,
    fontSize: 18,
    color: 'black',
    textAlign: 'center',
    maxHeight: 50, // Limiting height of the text input
  },
  keyboard: {
    width: '100%',
    backgroundColor: '#fff',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 10,
    position: 'absolute',
    bottom: 0,
    paddingHorizontal: 20,
    paddingVertical: 20,
    zIndex: 0, // Keep keyboard below text input
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 10, // Add some space between rows
  },
  key: {
    width: 26.5,  // Reduced key width
    height: 35, // Further reduced height for better proportions
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    margin: 5,  // Space between keys
    backgroundColor: '#f2f2f2',
  },
  keyText: {
    fontSize: 14,  // Slightly smaller font size for the keys
    fontWeight: 'bold',
    color: '#333',
  },
  caps: {
    width: 30,
    height: 35,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    margin: 5,
    backgroundColor: '#f2f2f2',
  },
  capsclicked: {
    width: 30,
    height: 35,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    margin: 5,
    backgroundColor: '#90D5FF',
  },
  img: {
    width: 20,
    height: 20,
  },
  space: {
    width: 120,  // Wider space key
    height: 50,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    margin: 5,
    backgroundColor: '#f2f2f2',
  },
  recommendationContainer: {
    padding: 10,
    marginBottom: 20,
  },
  recommendationText: {
    fontSize: 16,
    color: '#333',
  }
});

export default function Index() {
  const Upper_Letters = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['CAP', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'IMG1']
  ];
  const lower_Letters = [
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['CAP', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'IMG1']
  ];

  const [Input, setInput] = useState('');
  const [Caps, setCaps] = useState(0);
  const [Keys, setKeys] = useState(lower_Letters);
  const [recommend, setRecommend] = useState<string[]>([]);

  const handleKeyPressed = (key: string) => {
    setInput((prevInput) => prevInput + key);
    Recommend();
  };

  const deleteKeyPressed = () => {
    if (Input.length) {
      setInput(Input.slice(0, -1));
      Vibration.vibrate(100);  // Vibrates for 100 milliseconds on key press
    }
  };

  const CapPressed = (state: Int32) => {
    if (state === 1) {
      setCaps(0);
      setKeys(lower_Letters);
    } else {
      setCaps(1);
      setKeys(Upper_Letters);
    }
  };

  const Recommend = async () => {
    if (Input.length) {
      await Model(Input, setRecommend);
    }
  };

  const renderRecommendations = () => {
    // Conditionally render recommendations only if there are any
    console.log(recommend);
    if (recommend.length > 0) {
      return (
        <View style={Styles.recommendationContainer}>
          {recommend.map((val, index) => (
            <Text key={index} style={Styles.recommendationText}>{val}</Text>
          ))}
        </View>
      );
    }
    return <Text>hi</Text>; // Don't render anything if there are no recommendations
  };

  const handleKeys = (key: string) => {
    if (key === 'IMG1') {
      const icon = require('./static/bs.png');
      return (
        <TouchableOpacity style={Styles.key} onPress={deleteKeyPressed}>
          <Image source={icon} style={Styles.img} />
        </TouchableOpacity>
      );
    } else if (key === 'CAP') {
      const icon = require('./static/caps.png');
      return (
        <TouchableOpacity
          style={Caps === 0 ? Styles.caps : Styles.capsclicked}
          onPress={() => CapPressed(Caps)}
        >
          <Image source={icon} style={Styles.img} />
        </TouchableOpacity>
      );
    } else {
      return (
        <TouchableOpacity style={Styles.key} onPress={() => handleKeyPressed(key)}>
          <Text style={Styles.keyText}>{key}</Text>
        </TouchableOpacity>
      );
    }
  };

  return (
    <View style={Styles.container}>
      <TextInput
        style={Styles.input}
        value={Input}
        editable={false}
        placeholder="Type something..."
      />
      {renderRecommendations()} 
      {/*  Conditionally display recommendations */}
      <View style={Styles.keyboard}>
        {Keys.map((row, rowIndex) => (
          <View style={Styles.row} key={rowIndex}>
            {row.map((letter, index) => (
              <React.Fragment key={index}>{handleKeys(letter)}</React.Fragment>
            ))}
          </View>
        ))}
        <View style={Styles.row}>
          <TouchableOpacity style={Styles.key} onPress={() => handleKeyPressed(',')}>
            <Text style={Styles.keyText}>,</Text>
          </TouchableOpacity>
          <TouchableOpacity style={Styles.space} onPress={() => handleKeyPressed(' ')}>
            <Text style={Styles.keyText}>Space</Text>
          </TouchableOpacity>
          <TouchableOpacity style={Styles.key} onPress={() => handleKeyPressed('.')}>
            <Text style={Styles.keyText}>.</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}
