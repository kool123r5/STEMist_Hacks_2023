import React, { useEffect, useState } from "react";
import { KeyboardAvoidingView, StyleSheet, Text, TextInput, TouchableOpacity, View } from "react-native";
import { createUser, loginUser } from "./firebase";

const User = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    return (
        <KeyboardAvoidingView style={stylesUser.container} behavior="padding">
            <View style={stylesUser.inputContainer}>
                <TextInput
                    placeholder="Email"
                    value={email}
                    onChangeText={(text) => setEmail(text)}
                    style={stylesUser.input}
                />
                <TextInput
                    placeholder="Password"
                    value={password}
                    onChangeText={(text) => setPassword(text)}
                    style={stylesUser.input}
                    secureTextEntry
                />
            </View>

            <View style={stylesUser.buttonContainer}>
                <TouchableOpacity onPress={() => loginUser(email, password)} style={stylesUser.button}>
                    <Text style={stylesUser.buttonText}>Login</Text>
                </TouchableOpacity>
                <TouchableOpacity
                    onPress={() => createUser(email, password)}
                    style={[stylesUser.button, stylesUser.buttonOutline]}
                >
                    <Text style={stylesUser.buttonOutlineText}>Register</Text>
                </TouchableOpacity>
            </View>
        </KeyboardAvoidingView>
    );
};

export default User;

const stylesUser = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "black",
    },
    inputContainer: {
        width: "80%",
    },
    input: {
        backgroundColor: "#ddd",
        paddingHorizontal: 15,
        paddingVertical: 10,
        borderRadius: 10,
        marginTop: 5,
    },
    buttonContainer: {
        width: "60%",
        justifyContent: "center",
        alignItems: "center",
        marginTop: 40,
    },
    button: {
        backgroundColor: "lightblue",
        width: "100%",
        padding: 15,
        borderRadius: 10,
        alignItems: "center",
    },
    buttonOutline: {
        backgroundColor: "white",
        marginTop: 5,
        borderColor: "lightblue",
        borderWidth: 2,
    },
    buttonText: {
        color: "white",
        fontWeight: "700",
        fontSize: 16,
    },
    buttonOutlineText: {
        color: "lightblue",
        fontWeight: "700",
        fontSize: 16,
    },
});
