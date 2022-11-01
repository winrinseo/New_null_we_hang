import { StatusBar } from 'expo-status-bar';
import axios from 'axios';
import { useEffect,useRef } from 'react';
import { Pressable, PermissionsAndroid, StyleSheet, Text, View ,TouchableOpacity} from 'react-native';
import React, { useState } from 'react';
// import { RNCamera } from 'react-native-camera';
import {Camera, CameraType} from 'expo-camera';

export default function App() {
  //카메라 권한
  const [ok , setOk] = useState(true);

  const [type, setType] = useState(CameraType.back);
  const camera = useRef();
  const [go , setGo] = useState(-1);
  const [result,setResult] = useState("시작해주세요");
  useEffect(() =>{
    cameraPermission();
  },[]);

  useEffect(() =>{
    requestImg();
  },[go]);
  const cameraPermission = async () => {
    try {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setOk(status === 'granted');
      
      console.log(status);
      if (status === PermissionsAndroid.RESULTS.GRANTED) {
        console.log("You can use the camera");
      } else {
        console.log("Camera permission denied");
      }
    } catch (err) {
      console.warn(err);
    }
  }

  const requestImg = async () => {
    if(ok && go > 0){
      while(go > 0){
        if(go < 0) break;
        let flag = false;
        if(camera){
          const options = { quality: 0.5, base64: true };
          let photo = await camera.current.takePictureAsync(options);
          let fetchOptions = {
            method : "POST",
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
            },
            body : JSON.stringify({
              img:photo
            }),
          };
          await fetch("http://14.42.190.185:6974/inferance/",fetchOptions).then((response)=>response.json()).
          then(json => {
            console.log(json);
            if(json.result != 0) {
              flag = true;
              setResult(json.text);
            }
          });
          if(flag) break;
        }else{
          console.log("카메라가 존재하지 않습니다.");
          break;
        }
      } 
    }else{
      setResult("시작해주세요");
    }
  }
  
  return (
    <TouchableOpacity style={styles.container} onPress = {() =>{
      setGo(go*-1);
      console.log(go);
    }}>
      <View style={styles.nav}>
        <Text style={styles.ft}>{go > 0 ? "스캔중":"스캔 시작"}</Text>
      </View>
      <View style={styles.bd}>
        <Camera style={styles.camera} 
        type={type}
        ref={camera}>
        </Camera>
      </View>
      <View style={styles.bot}>
        <Text style={{fontSize : 50}}>{result}</Text>

      </View>
      
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  nav:{
    flex : 1,
    justifyContent: 'center',
    
  },
  bd:{
    flex:3,
    
    justifyContent: 'center',
    
  },
  bot:{
    flex:1,
    
  },
  ft:{
    fontSize: 50,
    fontWeight : 'bold',
  },
  camera: {
    flex: 1,
    alignItems: 'center',
  },
});
