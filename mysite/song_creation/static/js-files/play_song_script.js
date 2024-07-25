const neededDivs = document.querySelectorAll("div")

const sound = new Audio()

for (const div of neededDivs) {
    const musicButton = div.querySelector("button")
    musicButton.addEventListener('click', playSound)

    function playSound() {

        if (musicButton.textContent === "Play") {
            sound.pause()
            sound.src = div.getAttribute("value")
            sound.play()
            musicButton.textContent = "Stop"
        } else if (musicButton.textContent === "Stop") {
            sound.src = div.getAttribute("value")
            sound.pause()
            musicButton.textContent = "Play"
        }
        

    }
}