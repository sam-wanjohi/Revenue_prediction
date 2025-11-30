import 'package:flutter/material.dart';
import 'api_service.dart';

void main() {
  runApp(const RevenueApp());
}

class RevenueApp extends StatelessWidget {
  const RevenueApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Revenue Prediction',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const PredictionScreen(),
    );
  }
}

class PredictionScreen extends StatefulWidget {
  const PredictionScreen({super.key});

  @override
  _PredictionScreenState createState() => _PredictionScreenState();
}

class _PredictionScreenState extends State<PredictionScreen> {
  final ApiService api = ApiService();

  final TextEditingController monthController = TextEditingController();
  final TextEditingController bedsController = TextEditingController();
  final TextEditingController unitsController = TextEditingController();

  double? prediction;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Revenue Prediction")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              controller: monthController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: "Month"),
            ),
            TextField(
              controller: bedsController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: "Beds Occupied"),
            ),
            TextField(
              controller: unitsController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: "Units Occupied"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                final input = {
                  "Month": double.parse(monthController.text),
                  "beds_occupied": double.parse(bedsController.text),
                  "units_occupied": double.parse(unitsController.text),
                };

                double? result = await api.predictRevenue(input);
                setState(() => prediction = result);
              },
              child: const Text("Predict Revenue"),
            ),
            const SizedBox(height: 20),
            prediction != null
                ? Text(
                    "Predicted Revenue: ${prediction!.toStringAsFixed(2)}",
                    style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  )
                : const SizedBox(),
          ],
        ),
      ),
    );
  }
}
