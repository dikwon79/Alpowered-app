
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
    xhr.open("POST", "http://127.0.0.1/upload", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log("파일 업로드 완료");
                // 여기에 서버로부터의 응답을 처리하는 코드를 추가할 수 있습니다.
            } else {
                console.error("파일 업로드 실패:", xhr.status);
                // 여기에 파일 업로드가 실패했을 때의 처리 코드를 추가할 수 있습니다.
            }
        }
    };
    xhr.send(formData);
}


document.getElementById("startButton").addEventListener("click", startRecording);
document.getElementById("stopButton").addEventListener("click", stopRecording);
