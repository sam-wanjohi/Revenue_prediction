import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "https://revenue-prediction-api.onrender.com";

  Future<double?> predictRevenue(Map<String, dynamic> inputData) async {
    final url = Uri.parse("$baseUrl/predict");

    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(inputData),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data["prediction"];
    } else {
      print("Error: ${response.body}");
      return null;
    }
  }
}
