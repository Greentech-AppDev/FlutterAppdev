import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'welcome_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  double? waterTemp;
  double? airTemp;
  late Timer _timer;

  static const _url = 'https://backendappdev.onrender.com/temperature/latest';
  static const _bearer =
      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzQ3NzczMjkwfQ.z5Jo1DeGbP8RUyD91VwcsmcgAN6bT0KUo86AVbBIxvk';

  @override
  void initState() {
    super.initState();
    _fetch();
    _timer = Timer.periodic(
      const Duration(seconds: 3), (_) => _fetch());
  }

  Future<void> _fetch() async {
    try {
      final res = await http.get(Uri.parse(_url), headers: {
        'Authorization': 'Bearer $_bearer',
      });
      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        setState(() {
          waterTemp = data['water_temperature']?.toDouble();
          airTemp = data['air_temperature']?.toDouble();
        });
      } else {
        debugPrint('HTTP ${res.statusCode}');
      }
    } catch (e) {
      debugPrint('Fetch error: $e');
    }
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(children: [
        Positioned.fill(
          child: Image.asset(
            'assets/bg2.png',
            fit: BoxFit.cover,
          ),
        ),
        SafeArea(
          child: Container(
            height: MediaQuery.of(context).size.height,
            width: double.infinity,
            child: SingleChildScrollView(
              child: Column(children: [
                Align(
                  alignment: Alignment.centerLeft,
                  child: Padding(
                    padding: const EdgeInsets.all(8),
                    child: ElevatedButton.icon(
                      onPressed: () => Navigator.pushAndRemoveUntil(
                          context,
                          MaterialPageRoute(
                              builder: (_) => const WelcomeScreen()),
                          (_) => false),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF0B4F13),
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(20)),
                      ),
                      icon: const Icon(Icons.home),
                      label: const Text('HOME'),
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                Image.asset('assets/logo.png', width: 70),
                const SizedBox(height: 20),
                _title('TEMPERATURE'),
                const SizedBox(height: 30),
                _card(
                  icon: 'assets/watertemplogo.png',
                  label: 'Temperature',
                  value: waterTemp != null
                      ? '${waterTemp!.toStringAsFixed(1)}°C'
                      : '—'),
                const SizedBox(height: 20),
                _card(
                  icon: 'assets/airtemplogo.png',
                  label: 'Humidity',
                  value: airTemp != null
                      ? '${airTemp!.toStringAsFixed(1)}°C'
                      : '—'),
                const SizedBox(height: 40),
              ]),
            ),
          ),
        ),
      ]),
    );
  }

  Widget _title(String t) => Center(
        child: Text(t,
            style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.green[900],
                letterSpacing: 1.2)),
      );

  Widget _card({
    required String icon,
    required String label,
    required String value,
  }) =>
      Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
              color: Colors.green[500],
              borderRadius: BorderRadius.circular(20)),
          child: Row(children: [
            Image.asset(icon, width: 40),
            const SizedBox(width: 20),
            Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(label,
                  style: const TextStyle(
                      color: Colors.white, fontWeight: FontWeight.w600)),
              const SizedBox(height: 5),
              Text(value,
                  style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      fontSize: 18)),
            ]),
          ]),
        ),
      );
}
