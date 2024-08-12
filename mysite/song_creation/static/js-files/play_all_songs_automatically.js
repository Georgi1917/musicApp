const musicDivs = document.querySelectorAll("div")
const playAllButton = document.getElementById("play-all")


playAllButton.addEventListener("click", () => {
    let currIndex = 0
    const neededAudio = new Audio()

    function playNext() {
        if (currIndex < musicDivs.length) {
            neededAudio.src = musicDivs[currIndex].getAttribute("value");
            neededAudio.play();
            currIndex++;
        }
    }

    neededAudio.addEventListener("ended", playNext);

    playNext();
})