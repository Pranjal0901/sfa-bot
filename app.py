from flask import Flask, render_template, jsonify, request

# -------------------------------------------------------------------------
# Initialize Flask app
# -------------------------------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------------------------------
# Flask Routes
# -------------------------------------------------------------------------
@app.route("/")
def index():
    """Render main chatbot interface"""
    return render_template("chatbot.html")

@app.route("/ask", methods=["POST"])
def ask():
    """Handle user query and return RAG-generated response"""
    user_input = request.json.get("message", "")
    if not user_input.strip():
        return jsonify({"response": "Please enter a valid question."})
    
    print(f"[USER] {user_input}")
    # answer = rag_pipeline.search_and_summarize(user_input)
    # print(f"[BOT] {answer}")
    # return jsonify({"response": answer})


# -------------------------------------------------------------------------
# Run app
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
