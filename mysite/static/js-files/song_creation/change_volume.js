function changeVolume(audio, volumeCont) {
    
    volumeCont.addEventListener("input", () => {

        audio.volume = volumeCont.value;
    })
}