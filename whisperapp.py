from flask import Flask, request, render_template
import os
#import whisper
import replicate
import tempfile

app = Flask(__name__)
model = replicate.models.get("openai/whisper")
version = model.versions.get("30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    print("Received request!")
    file_bytes = request.files['file'].read()
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp3")
    temp_file.write(file_bytes)
    # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#input
    inputs = {
        # Audio file
        'audio': open(temp_file.name, "rb"),
        # Choose a Whisper model.
        'model': "base",
        # Choose the format for the transcription
        'transcription': "plain text",
        'translate': False,
        'temperature': 0,
        'suppress_tokens': "-1",
        'condition_on_previous_text': True,
        'temperature_increment_on_fallback': 0.2,
        'compression_ratio_threshold': 2.4,
        'logprob_threshold': -1,
        'no_speech_threshold': 0.6,
    }

    # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#output-schema
    output = version.predict(**inputs)
    temp_file.close()
    return output

# Initialize the model at the beginning to not have to load it at each request
#model = whisper.load_model("base")

@app.route('/')
def home():
    return render_template('index.html')

"""
@app.route('/transcribe', methods=['POST'])
def transcribe():

    # Read the file to bytes
    mp3_file = request.files["file"].read()

    # Write the bytes to a temporary mp3 file since the whisper command takes in a file path as input, not the actual file
    file_path = "./temp.mp3"
    with open(file_path, 'wb') as new_file:
        new_file.write(mp3_file)

    # Call whisper on the temporary file path and get transcription
    result = model.transcribe("./temp.mp3")

    # Remove the temporary file
    os.remove("./temp.mp3")

    # Return the transcript as a JSON response
    return jsonify({'transcript': result["text"]})
"""
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5020))
    app.run(debug=True, host='0.0.0.0', port=port)
