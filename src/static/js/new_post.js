navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
  handlerFunction(stream);
});

let blob = null;
function handlerFunction(stream) {
  rec = new MediaRecorder(stream);
  rec.ondataavailable = (e) => {
    audioChunks.push(e.data);
    if (rec.state == "inactive") {
      let blob_ = new Blob(audioChunks, { type: "audio/mp3" });
      recordedAudio.src = URL.createObjectURL(blob_);
      recordedAudio.controls = true;
      recordedAudio.autoplay = true;

      info.innerHTML = "Recording finished. Click to upload.";
      document.getElementById("submitBtnRecorded").hidden = false;
      document.getElementById("submitBtn").hidden = true;

      blob = blob_;
    }
  };
}
function submitRecorded() {
  sendData(blob);
}

function sendData(blob) {
  let formData = new FormData();
  formData.append("audio", blob);
  const description = document.getElementById("description").value;
  
  if(blob == null | blob == "" | blob == undefined) {
    alert("Please record a sound first.");
    return;
    }

  if (
    (description.length < 0) |
    (description == "") |
    (description == null) |
    (description == undefined)
  ) {
    alert("Please enter a description");
    return;
  }

  fetch("/new", {
    method: "POST",
    body: formData,
  }).then((response) => {
    if (response.ok) {
      window.location.href = "/";
    } else {
      alert("Something went wrong");
    }
  });
}

record.onclick = (e) => {
  record.disabled = true;
  record.style.backgroundColor = "blue";
  stopRecord.disabled = false;
  audioChunks = [];
  rec.start();
};
stopRecord.onclick = (e) => {
  record.disabled = false;
  stop.disabled = true;
  record.style.backgroundColor = "red";
  rec.stop();
};
