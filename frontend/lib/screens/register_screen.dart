import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'dashboard_screen.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _username = TextEditingController();
  final _email    = TextEditingController();
  final _password = TextEditingController();

  static const String registerUrl = 'https://backendappdev.onrender.com/register';

  Future<void> _registerUser() async {
    debugPrint('Register button tapped');
    try {
      final res = await http.post(
        Uri.parse(registerUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': _username.text.trim(),
          'email'   : _email.text.trim(),
          'password': _password.text.trim(),
        }),
      );

      debugPrint('Register ► status: ${res.statusCode}');
      debugPrint('Register ► body  : ${res.body}');

      if (!mounted) return;

      if (res.statusCode == 200 || res.statusCode == 201) {
        final data = jsonDecode(res.body);
        final token = data['access_token'] as String?;
        if (token != null) {
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('access_token', token);
        }

        ScaffoldMessenger.of(context)
            .showSnackBar(const SnackBar(content: Text('Registered successfully!')));
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const DashboardScreen()),
        );
      } else {
        _showError(_extractError(res.body));
      }
    } catch (e) {
      _showError('Error: $e');
    }
  }

  String _extractError(String body) {
    try {
      final decoded = jsonDecode(body);
      if (decoded is Map && decoded.isNotEmpty) return decoded.values.first.toString();
    } catch (_) {}
    return 'Registration failed';
  }

  void _showError(String msg) =>
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));

  @override
  void dispose() {
    _username.dispose();
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final deco = InputDecoration(
      filled: true,
      fillColor: const Color(0xFFDCF8C6),
      hintStyle: const TextStyle(color: Colors.green, fontSize: 18, fontWeight: FontWeight.bold),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(20), borderSide: BorderSide.none),
      contentPadding: const EdgeInsets.symmetric(vertical: 18, horizontal: 24),
    );

    return Scaffold(
      body: Stack(
        children: [
          Positioned.fill(child: Image.asset('assets/bg2.png', fit: BoxFit.cover)),
          SafeArea(
            child: Column(
              children: [
                Align(
                  alignment: Alignment.centerLeft,
                  child: IconButton(
                    icon: const Icon(Icons.arrow_back, color: Colors.white),
                    onPressed: () => Navigator.pop(context),
                  ),
                ),
                const SizedBox(height: 10),
                Expanded(
                  child: SingleChildScrollView(
                    child: Column(
                      children: [
                        Image.asset('assets/logo.png', width: 140),
                        const SizedBox(height: 10),
                        const Text('Register',
                            style: TextStyle(
                              fontSize: 28,
                              fontWeight: FontWeight.bold,
                              color: Color.fromARGB(255, 19, 82, 21),
                            )),
                        const SizedBox(height: 60),
                        _textField(deco, 'Username', _username),
                        const SizedBox(height: 20),
                        _textField(deco, 'Email', _email),
                        const SizedBox(height: 20),
                        _textField(deco, 'Password', _password, obscure: true),
                        const SizedBox(height: 30),
                        ElevatedButton(
                          onPressed: _registerUser,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green[900],
                            padding: const EdgeInsets.symmetric(horizontal: 100, vertical: 25),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                          ),
                          child: const Text('REGISTER',
                              style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold, color: Colors.white)),
                        ),
                        const SizedBox(height: 40),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _textField(InputDecoration deco, String hint, TextEditingController c,
          {bool obscure = false}) =>
      Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30),
        child: TextField(
          controller: c,
          obscureText: obscure,
          decoration: deco.copyWith(hintText: hint),
        ),
      );
}
