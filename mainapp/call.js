import React from 'react';
import { View, Text, TouchableOpacity, Alert } from 'react-native';
import Communications from 'react-native-communications';
import {decode as atob, encode as btoa} from 'base-64'


const App = () => {
  const twilioPhoneNumber = '+12179088838'; 
  const toPhoneNumber = '+916366060912'; 

  const handleCallButtonPress = () => {
    const twilioAPIBaseUrl = 'https://api.twilio.com/2010-04-01';
    const accountSid = 'ACc00dd309196ccc63c81655e4fef9c573'; 
    const authToken = '5c5a829c20de074f5cb0d07303422559'; 
    const twilioPhoneNumberFormatted = encodeURIComponent(twilioPhoneNumber);
    const toPhoneNumberFormatted = encodeURIComponent(toPhoneNumber);
    const callUrl = `${twilioAPIBaseUrl}/Accounts/${accountSid}/Calls.json`;

    const authHeader = {
      Authorization: 'Basic ' + btoa(`${accountSid}:${authToken}`),
      'Content-Type': 'application/x-www-form-urlencoded',
    };

    const formData = `To=${toPhoneNumberFormatted}&From=${twilioPhoneNumberFormatted}&Url=https://handler.twilio.com/twiml/EH4a24acea3c5df1809a3232e5dfea9320`;

    fetch(callUrl, {
      method: 'POST',
      headers: authHeader,
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to initiate the call.');
        }
        return response.json();
      })
      .then((data) => {
        const { sid } = data;
        console.log('Call SID:', sid);
      })
      .catch((error) => {
        console.error('Error making the call:', error);
        Alert.alert('Call Error', 'Sorry, an error occurred while making the call.');
      });
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <TouchableOpacity onPress={handleCallButtonPress}>
        <Text style={{ fontSize: 20, color: 'blue' }}>Make Call</Text>
      </TouchableOpacity>
    </View>
  );
};

export default App;
