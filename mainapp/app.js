import "react-native-url-polyfill/auto";
import { addLocData, readLocData } from "./firebase.js";
import { name as appName } from "./app.json";
import { StyleSheet } from "react-native";
import { getDocs, query, collection } from "firebase/firestore";
import React, { useState, useEffect, useRef } from "react";
import { View, TouchableOpacity, Text, Alert, Image, AppRegistry, LogBox } from "react-native";
import * as Location from "expo-location";
import * as Permissions from "expo-permissions";
import * as Notifications from "expo-notifications";
import MapView, { Marker } from "react-native-maps";
LogBox.ignoreLogs(["Warning: ..."]);
// LogBox.ignoreAllLogs();
console.disableYellowBox = true;
export default function App() {
    const [userLocation, setUserLocation] = useState(null);
    const mapRef = useRef(null);
    const [targetLocation, setTargetLocation] = useState(null);
    const [gunType, setGunType] = useState("");
    useEffect(() => {
        getLocationPermission();
        const fetchLocData = async () => {
            try {
                let data = await readLocData();
                setGunType(data.gunType);
                data = data.location;
                setTargetLocation(data);
            } catch (error) {
                console.error("Error fetching location data:", error);
            }
        };

        const zoomToUserLocation = async () => {
            try {
                const location = await getUserLocation();
                addLocData(location);
                setUserLocation(location);

                mapRef.current.animateToRegion({
                    ...location,
                    latitudeDelta: 0.01,
                    longitudeDelta: 0.01,
                });
            } catch (error) {
                console.error("Location error:", error);
            }
        };
        fetchLocData();
        zoomToUserLocation();
    }, []);
    async function handleButtonPress() {
        const location = await getUserLocation();
        setUserLocation(location);
        const distance = calculateDistance(location, targetLocation);

        if (distance <= 3000) {
            Alert.alert("Alert", "IN 3KM RADIUS");
        }
    }

    console.log(userLocation, targetLocation);
    return (
        <View style={styles.container}>
            <Text style={styles.textStyle}>{gunType}</Text>
            <MapView
                ref={mapRef}
                style={styles.map}
                region={userLocation ? { ...userLocation, latitudeDelta: 0.01, longitudeDelta: 0.01 } : null}
            >
                {userLocation && (
                    <>
                        <Marker coordinate={userLocation}>
                            <Image source={require("./assets/blue_dot.png")} style={styles.blueDot} />
                        </Marker>
                        <Marker coordinate={targetLocation}>
                            <Image source={require("./assets/red_dot.png")} style={styles.redDot} />
                        </Marker>
                    </>
                )}
            </MapView>
            <View>
                <TouchableOpacity onPress={handleButtonPress}>
                    <Text style={styles.testText}>aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
}
AppRegistry.registerComponent(appName, () => App);

const calculateDistance = (location1, location2) => {
    const earthRadius = 6371;

    const { latitude: lat1, longitude: lon1 } = location1;
    const { latitude: lat2, longitude: lon2 } = location2;

    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);

    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    const distance = earthRadius * c;
    return distance * 1000;
};

const getLocationPermission = async () => {
    const { status } = await Permissions.askAsync(Permissions.LOCATION);
    if (status !== "granted") {
        Alert.alert("Denied", "Enable location  permission in settings");
    }
};

const getUserLocation = async () => {
    const { coords } = await Location.getCurrentPositionAsync({});
    return { latitude: coords.latitude, longitude: coords.longitude };
};

const toRad = (value) => {
    return (value * Math.PI) / 180;
};

const sendNotification = async () => {
    await Notifications.scheduleNotificationAsync({
        content: {
            title: "Alert",
            body: "You are in a 3 kilometer radius of a gunshot.",
        },
        trigger: null,
    });
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#1E1E1E",
        paddingTop: 90,
        paddingBottom: 110,
        alignItems: "center",
        justifyContent: "center",
    },

    blueDot: {
        width: 50,
        height: 50,
    },

    redDot: {
        width: 17,
        height: 17,
    },

    testText: {
        color: "#1E1E1E",
    },

    textStyle: {
        fontSize: 26,
        fontWeight: 400,
        marginBottom: 10,
        color: "#ddd",
    },

    map: {
        width: "96%",
        aspectRatio: 1,
        borderWidth: 1.5,
        borderColor: "#ccc",
    },

    buttonText: {
        color: "#ddd",
        fontSize: 18,
        fontWeight: "bold",
    },
    marker: {
        width: 24,
        height: 24,
    },
});
