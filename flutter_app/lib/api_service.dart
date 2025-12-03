import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "https://revenue-prediction-api.onrender.com";

  Future<double?> predictRevenue(Map<String, dynamic> inputData) async {
    final url = Uri.parse("$baseUrl/predict");

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(inputData),
      );

      print("Status Code: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        // FIXED: match API field name
        final pred = data["predicted_revenue"];

        if (pred is num) {
          return pred.toDouble();
        } else {
          print("Unexpected prediction format: $pred");
          return null;
        }
      } else {
        print("API Error: ${response.body}");
        return null;
      }
    } catch (e) {
      print("Exception occurred while calling API: $e");
      return null;
    }
  }
}
