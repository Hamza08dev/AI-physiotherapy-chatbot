from flask import Blueprint, request, jsonify
from models.context_retrieval import answer_question

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        print("Chat route hit")
        # Get the user query from the request
        data = request.get_json()
        user_query = data.get("query", "")

        if not user_query:
            return jsonify({"error": "Query is required"}), 400

        # Get the answer and context
        answer, context = answer_question(user_query)

        # Return the response as JSON
        return jsonify({"answer": answer, "context": context})
    except Exception as e:
        return jsonify({"error": str(e)}), 500