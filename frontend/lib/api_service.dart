import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = 'https://backend-iot-appdev.onrender.com';

  Future<void> fetchData() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/data'));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        print('✅ Data received: $data');
      } else {
        print('❌ Failed to fetch data. Status code: ${response.statusCode}');
      }
    } catch (e) {
      print('❌ Error occurred: $e');
    }
  }
}
