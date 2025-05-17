import 'package:flutter/material.dart';
import 'screens/welcome_screen.dart';

void main() => runApp(const GreenTechApp());

class GreenTechApp extends StatelessWidget {
  const GreenTechApp({Key? key}) : super(key: key); // Added key

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GreenTech',
      debugShowCheckedModeBanner: false,
      home: const WelcomeScreen(), // Added const
    );
  }
}
