import streamlit as st
import librosa
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model(r"C:\Users\Pc\Downloads\audio_classification_model.h5")

# Feature extraction function
def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=18)
    mfccs_mean = mfccs.mean(axis=1)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=y).mean()
    combined_features = np.concatenate([mfccs_mean, [spectral_centroid, zero_crossing_rate]])
    return combined_features

# Prediction function
def predict_gender(features):
    features = features.reshape(1, -1)
    prediction = model.predict(features)
    return "Female" if prediction > 0.5 else "Male"
# Add custom background CSS
page_bg_img = '''
<style>
body {
    background-image: url("file:///C:/jj/background.jpg"); /* Replace background.jpg with your image file name */
    background-size: cover; /* Cover the entire screen */
    background-repeat: no-repeat; /* Prevent repeating */
    background-attachment: fixed; /* Fix the background */
    color: white; /* Adjust text color for better readability */
}
</style>
'''

# Apply the background CSS
st.markdown(page_bg_img, unsafe_allow_html=True)


# Streamlit App UI
st.title("Gender Detection Using Voice")
st.write("Upload a WAV file to predict the speaker's gender.")

# File uploader
uploaded_file = st.file_uploader("Choose a WAV file", type="wav")

if uploaded_file is not None:
    # Save the uploaded file
    with open("uploaded_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Play the uploaded audio file
    st.audio("uploaded_audio.wav", format="audio/wav")
    
    # Extract features from the uploaded audio file
    features = extract_features("uploaded_audio.wav")
    
    # Predict the gender
    gender = predict_gender(features)
    
    st.success(f"The predicted gender is: **{gender}**")
