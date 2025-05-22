import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/material.dart';
import 'dashboard_screen.dart';  // Import your dashboard screen

class AuthService {
  final BuildContext context;

  AuthService(this.context);

  Future<void> registerUser(String email, String password) async {
    final res = await http.post(
      Uri.parse('https://backendappdev.onrender.com/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    if (res.statusCode == 200) {
      final data = jsonDecode(res.body);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('access_token', data['access_token']);
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => DashboardScreen()));
    } else {
      debugPrint("Registration failed: ${res.body}");
    }
  }
}
