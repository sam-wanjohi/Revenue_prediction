import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Base URL of your deployed API
  static const String baseUrl = "https://revenue-prediction-api.onrender.com";

  /// Sends input data to the API and returns the predicted revenue as double
  Future<double?> predictRevenue(Map<String, dynamic> inputData) async {
    final url = Uri.parse("$baseUrl/predict");

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(inputData),
      );

      // Debugging: see response in console
      print("Status Code: ${response.statusCode}");
      print("Response Body: ${response.body}");

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        // Ensure the prediction is a numeric value
        final pred = data["prediction"];
        if (pred is num) {
          return pred.toDouble();
        } else if (pred is Map && pred.containsKey("value")) {
          return (pred["value"] as num).toDouble();
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
