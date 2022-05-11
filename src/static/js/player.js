const playIcon = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
      `,
  pauseIcon = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
      `,
  soundIcon = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
          </svg>`,
  muteIcon = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="red">
            <path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM12.293 7.293a1 1 0 011.414 0L15 8.586l1.293-1.293a1 1 0 111.414 1.414L16.414 10l1.293 1.293a1 1 0 01-1.414 1.414L15 11.414l-1.293 1.293a1 1 0 01-1.414-1.414L13.586 10l-1.293-1.293a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>`;

var [currentAudio, currentPlayer] = [null, null];

function toggleAudio(audio, playerButton) {
  if (audio.paused) {
    // If currently playing, pause the current audio and play this one
    if (currentAudio) {
      if (!currentAudio.paused) {
        currentAudio.pause();
        currentPlayer.innerHTML = playIcon;
      }
    }
    audio.play();
    playerButton.innerHTML = pauseIcon;
    currentAudio = audio;
    currentPlayer = playerButton;
  } else {
    audio.pause();
    currentAudio = audio;
    currentPlayer.innerHTML = playIcon;
    playerButton.innerHTML = playIcon;
  }
}

const playerButton = document.querySelectorAll('[id^="player-button-"]');

playerButton.forEach((button) => {
  // Get the ID of the post
  const id = button.id.split("-")[2];
  // Get audio element
  const audio = document.getElementById(`audio-${id}`);

  button.onclick = () => {
    toggleAudio(audio, button);
  };
});

function changeTimelinePosition(audio, timeline, timelineProgress) {
  const percentagePosition = (100 * audio.currentTime) / audio.duration;
  timeline.style.backgroundSize = `${percentagePosition}% 100%`;
  timeline.value = percentagePosition;

  timelineProgress.innerHTML = `${Math.floor(
    audio.currentTime / 60
  )}:${Math.floor(audio.currentTime % 60)}/${Math.floor(
    audio.duration / 60
  )}:${Math.floor(audio.duration % 60)}`;
}

const audios = document.querySelectorAll('[id^="audio-"]');

audios.forEach((audio) => {
  audio.addEventListener("timeupdate", () => {
    changeTimelinePosition(
      audio,
      document.getElementById(`timeline-${audio.id.split("-")[1]}`),
      document.getElementById(`progress-${audio.id.split("-")[1]}`)
    );
  });
});

function audioEnded(playerButton) {
  playerButton.innerHTML = playIcon;
}

audios.forEach((audio) => {
  audio.addEventListener("ended", () => {
    audioEnded(
      document.getElementById(`player-button-${audio.id.split("-")[1]}`)
    );
  });
});

function changeSeek(audio, timeline) {
  const time = (timeline.value * audio.duration) / 100;
  audio.currentTime = time;
}

const timelines = document.querySelectorAll('[id^="timeline-"]');

timelines.forEach((timeline) => {
  timeline.addEventListener("change", () => {
    changeSeek(
      document.getElementById(`audio-${timeline.id.split("-")[1]}`),
      timeline
    );
  });
});

function toggleSound(audio, soundButton) {
  audio.muted = !audio.muted;
  soundButton.innerHTML = audio.muted ? muteIcon : soundIcon;
}

const soundButtons = document.querySelectorAll('[id^="sound-button-"]');

soundButtons.forEach((soundButton) => {
  // Get the ID of the post
  const id = soundButton.id.split("-")[2];
  // Get audio element
  const audio = document.getElementById(`audio-${id}`);

  soundButton.addEventListener("click", () => {
    toggleSound(audio, soundButton);
  });
});
