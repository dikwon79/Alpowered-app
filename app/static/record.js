
let audioContext;
let recorder;

async function startRecording() {
    audioContext = new AudioContext();
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const input = audioContext.createMediaStreamSource(stream);
    recorder = new Recorder(input);
    recorder.record();
    document.getElementById("startButton").disabled = true;
    document.getElementById("stopButton").disabled = false;
}

function stopRecording() {
    recorder.stop();
    audioContext.close().then(() => {
        recorder.exportWAV(function(blob) {
            const url = URL.createObjectURL(blob);
            const audio = document.getElementById("audio");
            audio.src = url;
            uploadBlob(blob);
        });
    });
    document.getElementById("startButton").disabled = false;
    document.getElementById("stopButton").disabled = true;
}

function uploadBlob(blob) {
    const formData = new FormData();
    formData.append("audio", blob, "recording.wav");

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "https://hammerhead-app-6i4de.ondigitalocean.app/upload", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log("success to send the audio files");
                console.log(xhr.responseText);
            } else {
                console.error("fail to send the audio files:", xhr.status);
                
            }
        }
    };
    xhr.send(formData);
}


document.getElementById("startButton").addEventListener("click", startRecording);
document.getElementById("stopButton").addEventListener("click", stopRecording);
