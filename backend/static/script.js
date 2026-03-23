const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const output = document.getElementById("outputText");

let lastWord = "";

// Start camera
navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => {
    video.srcObject = stream;
})
.catch(err => {
    alert("Camera access denied or not working!");
    console.error(err);
});


// Speak detected word
function speakText(text){

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 1;

    window.speechSynthesis.speak(speech);

}


// Capture frame and send to backend
function captureFrame(){

    if(!video.videoWidth) return;

    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video,0,0);

    const imageData = canvas.toDataURL("image/jpeg");

    fetch("/predict",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({image:imageData})
    })
    .then(res=>res.json())
    .then(data=>{

        if(data.text && data.text !== "No Hand Detected"){

            if(data.text !== lastWord){

                output.value += data.text + " ";
                speakText(data.text);   // 🔊 Speak word

                lastWord = data.text;

            }

        }

    })
    .catch(err=>console.error(err));

}


// Run detection every 1.5 seconds
setInterval(captureFrame,1500);


// Copy text
function copyText(){

    output.select();
    document.execCommand("copy");

    alert("Text copied!");

}


// Clear text
function clearText(){

    output.value = "";
    lastWord = "";

}