const playAllButton = document.getElementById("play-all");

const allAudioFiles = []
const newAudio = new Audio()
let currAudioIndex = 0

for (const d of neededDivs) {
    
    const src = d.getAttribute("value")
    allAudioFiles.push(src)
    
}

function loadTrack(index) {
    
    newAudio.src = allAudioFiles[index];

    index + 1 >= allAudioFiles.length ? currAudioIndex = 0 : currAudioIndex++; 
}

function playNextTrack() {

    loadTrack(currAudioIndex)

    newAudio.play()
    
}

playAllButton.addEventListener("click", () => {

    if (playAllButton.textContent == "Play Playlist") {
        loadTrack(currAudioIndex);
        newAudio.addEventListener("ended", playNextTrack)
        newAudio.play();
        playAllButton.textContent = "Stop Playlist"
    } else {
        console.log(1)
        newAudio.pause()
        playAllButton.textContent = "Play Playlist"
    }
    
})