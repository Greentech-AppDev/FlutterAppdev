import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dashboard_screen.dart';

const String loginUrl = 'https://backendappdev.onrender.com/token';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _username = TextEditingController();   // ← actually for email input
  final _pwd      = TextEditingController();
  bool  _loading  = false;

  /* ───── LOGIN ───── */
  Future<void> _loginUser() async {
    setState(() => _loading = true);

    try {
      final res = await http.post(
        Uri.parse(loginUrl),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          // FastAPI OAuth2PasswordRequestForm expects **username** field, which is actually the email here
          'username'   : _username.text.trim(),
          'password'   : _pwd.text.trim(),
          'grant_type' : 'password',   // MUST be literally "password"
        },
      );

      setState(() => _loading = false);
      debugPrint('Login ► status: ${res.statusCode}');
      debugPrint('Login ► body  : ${res.body}');

      if (res.statusCode == 200) {
        final token = jsonDecode(res.body)['access_token'] as String? ?? '';
        // TODO: save token securely

        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Login successful')),
        );
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const DashboardScreen()),
        );
      } else {
        _showError(_extractError(res.body));
      }
    } catch (e) {
      setState(() => _loading = false);
      _showError('Network error: $e');
    }
  }

  String _extractError(String body) {
    try {
      final decoded = jsonDecode(body);
      if (decoded is Map) return decoded['detail']?.toString() ?? 'Login failed';
    } catch (_) {}
    return 'Login failed';
  }

  void _showError(String msg) =>
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));

  /* ───── UI ───── */
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Positioned.fill(child: Image.asset('assets/bg2.png', fit: BoxFit.cover)),
          SafeArea(
            child: LayoutBuilder(
              builder: (ctx, c) => SingleChildScrollView(
                child: ConstrainedBox(
                  constraints: BoxConstraints(minHeight: c.maxHeight),
                  child: Column(
                    children: [
                      const SizedBox(height: 30),
                      Image.asset('assets/logo.png', width: 120),
                      const SizedBox(height: 10),
                      Text('Welcome Back',
                          style: TextStyle(
                            fontSize: 28,
                            fontWeight: FontWeight.bold,
                            color: Colors.green[900],
                          )),
                      const SizedBox(height: 90),
                      _input('Email', _username),  // changed label here
                      const SizedBox(height: 20),
                      _input('Password', _pwd, isPassword: true),
                      const SizedBox(height: 30),
                      _loading
                          ? const CircularProgressIndicator()
                          : ElevatedButton(
                              onPressed: _loginUser,
                              style: ElevatedButton.styleFrom(
                                backgroundColor: const Color(0xFFDCF8C6),
                                foregroundColor: Colors.green[900],
                                padding: const EdgeInsets.symmetric(horizontal: 100, vertical: 18),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                              ),
                              child: const Text('LOGIN',
                                  style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                            ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _input(String hint, TextEditingController c, {bool isPassword = false}) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 40),
        child: TextField(
          controller: c,
          obscureText: isPassword,
          decoration: InputDecoration(
            filled: true,
            fillColor: const Color(0xFFDCF8C6),
            hintText: hint,
            hintStyle: const TextStyle(color: Color(0xFF336633)),
            contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 18),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(20),
              borderSide: BorderSide.none,
            ),
          ),
        ),
      );

  @override
  void dispose() {
    _username.dispose();
    _pwd.dispose();
    super.dispose();
  }
}
