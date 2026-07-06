import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const MaterialApp(home: ChatScreen()));

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});
  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> _messages = [];

  Future<void> _sendMessage() async {
    if (_controller.text.isEmpty) return;
    String userText = _controller.text;
    setState(() { _messages.add({"sender": "user", "text": userText}); });
    _controller.clear();

    final response = await http.post(
      Uri.parse('http://10.0.2.2:8000/chat'),
      headers: {"Content-Type": "application/json"},
      body: json.encode({"text": userText}),
    );

    if (response.statusCode == 200) {
      setState(() { _messages.add({"sender": "ai", "text": json.decode(response.body)['reply']}); });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Мій AI Агент"), backgroundColor: Colors.blueAccent),
      body: Column(
        children: [
          Expanded(child: ListView.builder(
            itemCount: _messages.length,
            itemBuilder: (context, index) => Container(
              alignment: _messages[index]['sender'] == 'user' ? Alignment.centerRight : Alignment.centerLeft,
              padding: const EdgeInsets.all(10),
              child: Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: _messages[index]['sender'] == 'user' ? Colors.blue[100] : Colors.grey[300], borderRadius: BorderRadius.circular(15)),
                child: Text(_messages[index]['text']!),
              ),
            ),
          )),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(children: [
              Expanded(child: TextField(controller: _controller, decoration: const InputDecoration(hintText: "Питання..."))),
              IconButton(icon: const Icon(Icons.send), onPressed: _sendMessage)
            ]),
          )
        ],
      ),
    );
  }
}