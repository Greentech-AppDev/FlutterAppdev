import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dashboard_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool rememberMe = false;
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  Future<void> _loginUser() async {
    // Change this URL if you run on emulator or device
    const String loginUrl = "https://backend-iot-appdev.onrender.com/api/login/";

    try {
      final response = await http.post(
        Uri.parse(loginUrl),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "username": _usernameController.text,
          "password": _passwordController.text,
        }),
      );

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Login successful!")),
        );

        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const DashboardScreen()),
        );
      } else {
        final errorData = jsonDecode(response.body);
        String errorMessage = 'Login failed';
        errorData.forEach((key, value) {
          errorMessage = "$key: ${value[0]}";
        });

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(errorMessage)),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: $e")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Positioned.fill(
            child: Image.asset(
              'assets/bg2.png',
              fit: BoxFit.cover,
            ),
          ),
          SafeArea(
            child: LayoutBuilder(
              builder: (context, constraints) {
                return SingleChildScrollView(
                  child: ConstrainedBox(
                    constraints: BoxConstraints(minHeight: constraints.maxHeight),
                    child: Column(
                      children: [
                        const SizedBox(height: 30),
                        Image.asset(
                          'assets/logo.png',
                          width: 120,
                        ),
                        const SizedBox(height: 10),
                        Text(
                          'Welcome Back',
                          style: TextStyle(
                            fontSize: 28,
                            fontWeight: FontWeight.bold,
                            color: Colors.green[900],
                          ),
                        ),
                        const SizedBox(height: 90),
                        _buildTextField('Username', _usernameController),
                        const SizedBox(height: 20),
                        _buildTextField('Password', _passwordController, isPassword: true),
                        const SizedBox(height: 15),
                        _buildOptions(),
                        const SizedBox(height: 20),
                        ElevatedButton(
                          onPressed: _loginUser,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFFDCF8C6),
                            foregroundColor: Colors.green[900],
                            padding: const EdgeInsets.symmetric(horizontal: 100, vertical: 18),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(20),
                            ),
                          ),
                          child: const Text(
                            'LOGIN',
                            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                          ),
                        ),
                        const SizedBox(height: 40),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTextField(String hintText, TextEditingController controller, {bool isPassword = false}) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 40),
      child: TextField(
        controller: controller,
        obscureText: isPassword,
        decoration: InputDecoration(
          filled: true,
          fillColor: const Color(0xFFDCF8C6),
          hintText: hintText,
          hintStyle: const TextStyle(color: Color(0xFF336633)),
          contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 18),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(20),
            borderSide: BorderSide.none,
          ),
        ),
      ),
    );
  }

  Widget _buildOptions() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 40),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Checkbox(
                value: rememberMe,
                onChanged: (value) {
                  setState(() {
                    rememberMe = value ?? false;
                  });
                },
              ),
              Text('Remember me', style: TextStyle(color: Colors.green[900])), // Changed to dark green
            ],
          ),
          TextButton(
            onPressed: () {},
            child: const Text(
              'Forgot Password',
              style: TextStyle(
                decoration: TextDecoration.underline,
                color: Colors.white, // If background is light, consider changing to dark color
              ),
            ),
          ),
        ],
      ),
    );
  }
}
