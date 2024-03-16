function viewResolution() {
  let reso = document.getElementById("resolution-option");

  reso.classList.toggle("hidden");
  // if(reso.className!="hidden"){
  //   reso.style.borderColor
  // }
}
function viewQuality() {
  let qual = document.getElementById("quality-option");

  qual.classList.toggle("hidden");
}
function viewMusic() {
  let mus = document.getElementById("music-option");

  mus.classList.toggle("hidden");
}
function viewTransition() {
  let trans = document.getElementById("transition-option");

  trans.classList.toggle("hidden");
}

function viewSetTime(){
  let st = document.getElementById("set-time-options");

  st.classList.toggle("hidden");
}

var currentAudio = null;

        function toggleMusic(track) {
            if (currentAudio !== null && !currentAudio.paused) {
                currentAudio.pause();
                if (currentAudio.src.endsWith(track)) {
                    currentAudio = null;
                    return;
                }
            }
            playMusic(track);
        }

        function playMusic(track) {
            var audio = new Audio("static/Assets/audio/" + track);
            audio.play();
            currentAudio = audio;
        }

        function toggleMusicOptions() {
            var musicOptions = document.getElementById("music-option");
            musicOptions.classList.toggle("hidden");
        }



const selectedImages = [];

function dragOverHandler(event) {
  event.preventDefault();
  document.getElementById('drop-area').style.border = '2px dashed green';
}

function dropHandler(event) {
  event.preventDefault();
  document.getElementById('drop-area').style.border = '2px dashed #ccc';

  const files = event.dataTransfer.files;
  // console.log(files);
  handleFiles(files);
}



// function deleteImage(image){
//      if(confirm("Are you sure?You want to delete this image")){
//         image.remove();
//      }
// }


// function handleFiles(files) {
//   const previewContainer = document.getElementById('images');
//   // console.log(files);

//   for (const file of files) {
//     const reader = new FileReader();

//     reader.onload = function (e) {
//       const imageData = e.target.result;
//       const image = new Image();
//       image.addEventListener('dblclick', function () {
        
//         deleteImage(image);
//       })
//       image.src = imageData;
//       previewContainer.appendChild(image);
//     };

//     reader.readAsDataURL(file);
//   }
// }

function handleFiles(files) {
  const formData = new FormData(); // Create a FormData object to store files

  for (const file of files) {
      formData.append('file', file); // Append each file to the FormData object
      
  }

  // Send the FormData object containing all files to the server using AJAX
  fetch('/upload', {
      method: 'POST',
      body: formData
  })
  .then(response => {
      if (response.ok) {
          return response.text(); // Handle successful response
      }
      throw new Error('Network response was not ok.');
  })
  .then(data => {
      console.log(data); // Handle response data
  })
  .catch(error => {
      console.error('There was a problem with the fetch operation:', error); // Handle errors
  });
}

// You may want to add an event listener to handle the click on the drop area and trigger the file input.
document.getElementById('drop-area').addEventListener('click', function () {
  document.getElementById('file-input').click();
});



// video

const playPauseBtn = document.querySelector(".play-pause-btn")
const theaterBtn = document.querySelector(".theater-btn")
const fullScreenBtn = document.querySelector(".full-screen-btn")
const miniPlayerBtn = document.querySelector(".mini-player-btn")
const muteBtn = document.querySelector(".mute-btn")
const speedBtn = document.querySelector(".speed-btn")
const currentTimeElem = document.querySelector(".current-time")
const totalTimeElem = document.querySelector(".total-time")
const previewImg = document.querySelector(".preview-img")
const thumbnailImg = document.querySelector(".thumbnail-img")
const volumeSlider = document.querySelector(".volume-slider")
const videoContainer = document.querySelector(".video-container")
const timelineContainer = document.querySelector(".timeline-container")
const video = document.querySelector("video")

document.addEventListener("keydown", e => {
  const tagName = document.activeElement.tagName.toLowerCase()

  if (tagName === "input") return

  switch (e.key.toLowerCase()) {
    case " ":
      if (tagName === "button") return
    case "k":
      togglePlay()
      break
    case "f":
      toggleFullScreenMode()
      break
    case "t":
      toggleTheaterMode()
      break
    case "i":
      toggleMiniPlayerMode()
      break
    case "m":
      toggleMute()
      break
    case "arrowleft":
    case "j":
      skip(-5)
      break
    case "arrowright":
    case "l":
      skip(5)
      break
  }
})

// Timeline
timelineContainer.addEventListener("mousemove", handleTimelineUpdate)
timelineContainer.addEventListener("mousedown", toggleScrubbing)
document.addEventListener("mouseup", e => {
  if (isScrubbing) toggleScrubbing(e)
})
document.addEventListener("mousemove", e => {
  if (isScrubbing) handleTimelineUpdate(e)
})

let isScrubbing = false
let wasPaused
function toggleScrubbing(e) {
  const rect = timelineContainer.getBoundingClientRect()
  const percent = Math.min(Math.max(0, e.x - rect.x), rect.width) / rect.width
  isScrubbing = (e.buttons & 1) === 1
  videoContainer.classList.toggle("scrubbing", isScrubbing)
  if (isScrubbing) {
    wasPaused = video.paused
    video.pause()
  } else {
    video.currentTime = percent * video.duration
    if (!wasPaused) video.play()
  }

  handleTimelineUpdate(e)
}

function handleTimelineUpdate(e) {
  const rect = timelineContainer.getBoundingClientRect()
  const percent = Math.min(Math.max(0, e.x - rect.x), rect.width) / rect.width
  const previewImgNumber = Math.max(
    1,
    Math.floor((percent * video.duration) / 10)
  )
  const previewImgSrc = `assets/previewImgs/preview${previewImgNumber}.jpg`
  previewImg.src = previewImgSrc
  timelineContainer.style.setProperty("--preview-position", percent)

  if (isScrubbing) {
    e.preventDefault()
    thumbnailImg.src = previewImgSrc
    timelineContainer.style.setProperty("--progress-position", percent)
  }
}

// Playback Speed
speedBtn.addEventListener("click", changePlaybackSpeed)

function changePlaybackSpeed() {
  let newPlaybackRate = video.playbackRate + 0.25
  if (newPlaybackRate > 2) newPlaybackRate = 0.25
  video.playbackRate = newPlaybackRate
  speedBtn.textContent = `${newPlaybackRate}x`
}

// Duration
video.addEventListener("loadeddata", () => {
  totalTimeElem.textContent = formatDuration(video.duration)
})

video.addEventListener("timeupdate", () => {
  currentTimeElem.textContent = formatDuration(video.currentTime)
  const percent = video.currentTime / video.duration
  timelineContainer.style.setProperty("--progress-position", percent)
})

const leadingZeroFormatter = new Intl.NumberFormat(undefined, {
  minimumIntegerDigits: 2,
})
function formatDuration(time) {
  const seconds = Math.floor(time % 60)
  const minutes = Math.floor(time / 60) % 60
  const hours = Math.floor(time / 3600)
  if (hours === 0) {
    return `${minutes}:${leadingZeroFormatter.format(seconds)}`
  } else {
    return `${hours}:${leadingZeroFormatter.format(
      minutes
    )}:${leadingZeroFormatter.format(seconds)}`
  }
}

function skip(duration) {
  video.currentTime += duration
}

// Volume
muteBtn.addEventListener("click", toggleMute)
volumeSlider.addEventListener("input", e => {
  video.volume = e.target.value
  video.muted = e.target.value === 0
})

function toggleMute() {
  video.muted = !video.muted
}

video.addEventListener("volumechange", () => {
  volumeSlider.value = video.volume
  let volumeLevel
  if (video.muted || video.volume === 0) {
    volumeSlider.value = 0
    volumeLevel = "muted"
  } else if (video.volume >= 0.5) {
    volumeLevel = "high"
  } else {
    volumeLevel = "low"
  }

  videoContainer.dataset.volumeLevel = volumeLevel
})

// View Modes
theaterBtn.addEventListener("click", toggleTheaterMode)
fullScreenBtn.addEventListener("click", toggleFullScreenMode)
miniPlayerBtn.addEventListener("click", toggleMiniPlayerMode)

function toggleTheaterMode() {
  videoContainer.classList.toggle("theater")
}

function toggleFullScreenMode() {
  if (document.fullscreenElement == null) {
    videoContainer.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

function toggleMiniPlayerMode() {
  if (videoContainer.classList.contains("mini-player")) {
    document.exitPictureInPicture()
  } else {
    video.requestPictureInPicture()
  }
}

document.addEventListener("fullscreenchange", () => {
  videoContainer.classList.toggle("full-screen", document.fullscreenElement)
})

video.addEventListener("enterpictureinpicture", () => {
  videoContainer.classList.add("mini-player")
})

video.addEventListener("leavepictureinpicture", () => {
  videoContainer.classList.remove("mini-player")
})

// Play/Pause
playPauseBtn.addEventListener("click", togglePlay)
video.addEventListener("click", togglePlay)

function togglePlay() {
  video.paused ? video.play() : video.pause()
}

video.addEventListener("play", () => {
  videoContainer.classList.remove("paused")
})

video.addEventListener("pause", () => {
  videoContainer.classList.add("paused")
})
