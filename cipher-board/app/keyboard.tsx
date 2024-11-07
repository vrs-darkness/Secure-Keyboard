import { Text, View } from "react-native";
import React, { useState } from 'react';
import { Image, TextInput , TouchableOpacity, StyleSheet} from "react-native";
import { Int32 } from "react-native/Libraries/Types/CodegenTypes";
import { SafeAreaView } from "react-native-safe-area-context";



const Styles = StyleSheet.create({
  keyboard:{
    paddingTop: 450
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 8,
  },
  key: {
    width: 33.5,
    height: 35,
    borderStyle: 'solid',
    borderWidth:1,
    borderBlockColor: 'black',
    borderColor: 'black',
    flexDirection: 'row',
    justifyContent: 'center'
  },
  space: {
    width: 100,
    borderStyle: 'solid',
    borderWidth:1,
    borderBlockColor: 'black',
    borderColor: 'black',
    flexDirection: 'row',
    justifyContent: 'center'
  },
  caps: {
    width: 30,
    borderStyle: 'solid',
    borderWidth:1,
    borderBlockColor: 'black',
    borderColor: 'black',
    flexDirection: 'row',
    justifyContent: 'center'
  },
  capsclicked:{
    width: 30,
    borderStyle: 'solid',
    borderWidth:1,
    borderBlockColor: 'black',
    borderColor: 'black',
    flexDirection: 'row',
    justifyContent: 'center',
    backgroundColor: '#90D5FF'
  },
  img: {
    width: 25,
    height: 10,
    marginTop: 5
  }
})
export default function Index() {
  const Upper_Letters = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                    ['CAP','z','x','c','v','b','n','m' , 'IMG1']];
  const lower_Letters = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                  ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                ['CAP','z','x','c','v','b','n','m' , 'IMG1']];
  const [Input, setInput] = useState<string>('');
  const [Caps, setCaps] = useState<Int32>(0);
  const [Keys, setKeys] = useState<string[][]>(lower_Letters);
  const handlekeyPressed = (key: string) => {
    setInput(Input+ key);
  }
  const deletekeyPressed = () =>{
    if (Input.length){
      setInput(Input.slice(0 ,-1));
    }
  }
  const Cappressed = (state: Int32) => {
    if (state===1){
      setCaps(0);
      setKeys(Upper_Letters);
    }
    else{
      setCaps(1);
      setKeys(lower_Letters);
    }
  }
  const Handle_keys = (key: string) =>{
    if(key==='IMG1'){
      const icon = require('./static/bs.png');
      return(
        <TouchableOpacity style={Styles.key}onPress={() => deletekeyPressed()}>
          <Image source={icon} style={Styles.img}></Image>
        </TouchableOpacity>
      );
    }
    else if(key==='CAP'){
      const icon = require('./static/caps.png');
      if (Caps==1){
        return(
          <TouchableOpacity style={Styles.caps}onPress={() => Cappressed(Caps)}>
            <Image source={icon} style={Styles.img}></Image>
          </TouchableOpacity>
        );
      }
      else{
        return(
          <TouchableOpacity style={Styles.capsclicked}onPress={() => Cappressed(Caps)}>
            <Image source={icon} style={Styles.img}></Image>
          </TouchableOpacity>
        );
      }
    }
    else{
      return (
        <TouchableOpacity style={Styles.key}onPress={() => handlekeyPressed(key)}>
          <Text>{key}</Text>
        </TouchableOpacity>
      );
    }

  }
  console.log(typeof(Keys));
  
  return (
    <View>
    <View>
      <TextInput placeholder={Input} editable={false}></TextInput>
    </View>
    <View style={Styles.keyboard}>
     
      {Keys.map((row) => (
        <View style={Styles.row}>
          {row.map((letter)=> (
                  Handle_keys(letter)))}
         </View> 
      ) )}
      <View style={Styles.row} >
       <TouchableOpacity style={Styles.key} onPress={() => handlekeyPressed(',')}><Text>,</Text></TouchableOpacity>
       <TouchableOpacity style={Styles.space} onPress={() => handlekeyPressed(' ')}><Text> </Text></TouchableOpacity>
       <TouchableOpacity style={Styles.key} onPress={() => handlekeyPressed('.')}><Text>.</Text></TouchableOpacity>
      </View>
    </View>
    </View>
  );
}
