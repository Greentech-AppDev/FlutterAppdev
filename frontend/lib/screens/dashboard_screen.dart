import 'package:flutter/material.dart';
import 'welcome_screen.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: Stack(
        children: [
          Positioned.fill(child: Image.asset('assets/bg2.png', fit: BoxFit.cover)),
          SafeArea(
            child: SingleChildScrollView(
              child: Column(
                children: [
                  // HOME button
                  Align(
                    alignment: Alignment.centerLeft,
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: ElevatedButton.icon(
                        onPressed: () => Navigator.pushAndRemoveUntil(
                          context,
                          MaterialPageRoute(builder: (_) => const WelcomeScreen()),
                          (_) => false,
                        ),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF0B4F13), // dark‑green
                          foregroundColor: Colors.white,
                          shape:
                              RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
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
                  _card(icon: 'assets/watertemplogo.png', label: 'Water Temperature', value: '22°C'),
                  const SizedBox(height: 20),
                  _card(icon: 'assets/airtemplogo.png', label: 'Air Temperature', value: '26°C'),
                  const SizedBox(height: 40),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _title(String t) => Center(
        child: Text(t,
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Colors.green[900],
              letterSpacing: 1.2,
            )),
      );

  Widget _card({required String icon, required String label, required String value}) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(color: Colors.green[500], borderRadius: BorderRadius.circular(20)),
          child: Row(
            children: [
              Image.asset(icon, width: 40),
              const SizedBox(width: 20),
              Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(label,
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
                const SizedBox(height: 5),
                Text(value,
                    style: const TextStyle(
                        color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18)),
              ]),
            ],
          ),
        ),
      );
}
