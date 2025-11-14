const categoriesData = {
    animals: [
        { image: 'images/animals/lion.png', name: 'Lion' },
        { image: 'images/animals/elephant.png', name: 'Elephant' },
        { image: 'images/animals/giraffe.png', name: 'Giraffe' },
        { image: 'images/animals/zebra.png', name: 'Zebra' },
        { image: 'images/animals/monkey.png', name: 'Monkey' },
        { image: 'images/animals/tiger.png', name: 'Tiger' },
        { image: 'images/animals/bear.png', name: 'Bear' },
        { image: 'images/animals/dog.png', name: 'Dog' },
        { image: 'images/animals/cat.png', name: 'Cat' },
        { image: 'images/animals/penguin.png', name: 'Penguin' },
    ],
    things: [
        { image: 'images/things/car.png', name: 'Car' },
        { image: 'images/things/ball.png', name: 'Ball' },
        { image: 'images/things/house.png', name: 'House' },
        { image: 'images/things/tree.png', name: 'Tree' },
        { image: 'images/things/book.png', name: 'Book' },
        { image: 'images/things/chair.png', name: 'Chair' },
        { image: 'images/things/table.png', name: 'Table' },
        { image: 'images/things/phone.png', name: 'Phone' },
        { image: 'images/things/umbrella.png', name: 'Umbrella' },
        { image: 'images/things/bicycle.png', name: 'Bicycle' },
    ],
    bollywood: [
        { image: 'images/bollywood/srk.png', name: 'Shah Rukh Khan' },
        { image: 'images/bollywood/amitabh.png', name: 'Amitabh Bachchan' },
        { image: 'images/bollywood/salman.png', name: 'Salman Khan' },
        { image: 'images/bollywood/deepika.png', name: 'Deepika Padukone' },
        { image: 'images/bollywood/hrithik.png', name: 'Hrithik Roshan' },
        { image: 'images/bollywood/priyanka.png', name: 'Priyanka Chopra' },
        { image: 'images/bollywood/aamir.png', name: 'Aamir Khan' },
        { image: 'images/bollywood/alia.png', name: 'Alia Bhatt' },
        { image: 'images/bollywood/ranbir.png', name: 'Ranbir Kapoor' },
        { image: 'images/bollywood/katrina.png', name: 'Katrina Kaif' },
    ]
};

// --- DOM Elements ---
const categorySelectionScreen = document.getElementById('category-selection');
const gameScreen = document.getElementById('game-screen');
const gameOverScreen = document.getElementById('game-over-screen');

const categoryButtons = document.querySelectorAll('.category-btn');
const gameImage = document.getElementById('game-image');
const itemNameDisplay = document.getElementById('item-name');
const instructionsText = document.getElementById('instructions');
const timerDisplay = document.getElementById('timer');
const scoreDisplay = document.getElementById('score');
const playAgainButton = document.getElementById('play-again-btn');
const finalScoreDisplay = document.getElementById('final-score');
const exitButton = document.getElementById('exit-button');

const bgMusic = document.getElementById('bg-music');
const timerEndSound = document.getElementById('timer-end-sound');

// --- Game State Variables ---
let currentCategory = [];
let currentIndex = 0;
let score = 0;
let timeLeft = 90;
let timerInterval;
let gamePhase = 0; // 0: initial (tap for picture), 1: picture shown (tap for name), 2: name shown (ready for next)
let tappedOnce = false; // To ensure only one tap per phase transition
let autoAdvanceTimer; // Timer for auto-advancing to next item

// --- Functions ---

function showScreen(screenToShow) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    screenToShow.classList.add('active');
}

function startGame(categoryName) {
    currentCategory = [...categoriesData[categoryName]]; // Copy to allow shuffling
    shuffleArray(currentCategory);
    currentIndex = 0;
    score = 0;
    timeLeft = 90;
    gamePhase = 0;
    tappedOnce = false;

    scoreDisplay.textContent = `Score: ${score}`;
    timerDisplay.textContent = timeLeft;
    gameImage.style.opacity = 0;
    // Ensure name is hidden immediately (use display:none via .hidden) to avoid any brief flash
    itemNameDisplay.classList.add('hidden');
    itemNameDisplay.style.opacity = 0;
    itemNameDisplay.textContent = '';
    instructionsText.textContent = 'Tap to reveal picture!';

    showScreen(gameScreen);
    loadNextItem();
    startTimer();
    playMusic();
}

function loadNextItem() {
    if (currentIndex >= currentCategory.length) {
        // Ran out of items, maybe shuffle and start again or end game
        shuffleArray(currentCategory); // For endless play, shuffle again
        currentIndex = 0;
    }
    const item = currentCategory[currentIndex];
    gameImage.src = item.image;
    // Set the name while it's hidden so it never appears briefly on load
    itemNameDisplay.classList.add('hidden');
    itemNameDisplay.style.opacity = 0;
    itemNameDisplay.textContent = item.name;

    // Reset for new item display
    gameImage.style.opacity = 0;
    instructionsText.textContent = 'Tap to reveal picture!';
    gamePhase = 0;
    tappedOnce = false;
    
    // Clear any pending auto-advance timer
    if (autoAdvanceTimer) {
        clearTimeout(autoAdvanceTimer);
        autoAdvanceTimer = null;
    }
}

function handleTap() {
    if (tappedOnce) return; // Prevent multiple taps in one phase
    tappedOnce = true;

    if (gamePhase === 0) { // First tap: show picture
        gameImage.style.opacity = 1;
        instructionsText.textContent = 'Tap again to reveal name!';
        gamePhase = 1;
        tappedOnce = false; // Reset for next phase
    } else if (gamePhase === 1) { // Second tap: show name and auto-advance
        // Remove the hidden class first so the element is displayed, then animate opacity
        itemNameDisplay.classList.remove('hidden');
        // Use requestAnimationFrame to ensure the browser registers the display change before animating
        requestAnimationFrame(() => {
            itemNameDisplay.style.opacity = 1;
        });
        score++; // Assuming every reveal is a correct guess for simplicity
        scoreDisplay.textContent = `Score: ${score}`;
        instructionsText.textContent = 'Next item loading...';
        gamePhase = 2;
        
        // Auto-advance to next item after 2 seconds
        if (autoAdvanceTimer) {
            clearTimeout(autoAdvanceTimer);
        }
        autoAdvanceTimer = setTimeout(() => {
            currentIndex++;
            loadNextItem();
        }, 2000);
    }
}

function startTimer() {
    bgMusic.currentTime = 0; // Start music from beginning
    bgMusic.volume = 0.3;    // Initial volume
    timerInterval = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;

        // Gradually increase music volume (and simulate "faster" by just increasing volume)
        if (timeLeft > 0) {
            const volumeIncreaseFactor = 0.7 / 90; // Increase by 0.7 over 90 seconds
            bgMusic.volume = Math.min(1.0, 0.3 + (90 - timeLeft) * volumeIncreaseFactor);
        }

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            endGame();
        }
    }, 1000);
}

function playMusic() {
    bgMusic.play().catch(e => console.error("Error playing background music:", e));
}

function stopMusic() {
    bgMusic.pause();
    bgMusic.currentTime = 0;
}

function endGame() {
    stopMusic();
    timerEndSound.play().catch(e => console.error("Error playing timer end sound:", e));
    clearInterval(timerInterval);
    finalScoreDisplay.textContent = score;
    showScreen(gameOverScreen);
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// --- Event Listeners ---

categoryButtons.forEach(button => {
    button.addEventListener('click', () => {
        const category = button.dataset.category;
        startGame(category);
    });
});

// Use event delegation for the game screen tap to handle picture/name reveal
gameScreen.addEventListener('click', (event) => {
    handleTap();
});

playAgainButton.addEventListener('click', () => {
    showScreen(categorySelectionScreen);
});

// Exit game while playing: stop timer/music and return to category selection
function exitGame() {
    // Clear auto-advance timer
    if (autoAdvanceTimer) {
        clearTimeout(autoAdvanceTimer);
        autoAdvanceTimer = null;
    }
    
    // Stop timer
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }

    // Stop music and reset audio
    stopMusic();

    // Reset visuals/state so when player returns later there's no leftover name/image
    gameImage.style.opacity = 0;
    itemNameDisplay.classList.add('hidden');
    itemNameDisplay.style.opacity = 0;
    itemNameDisplay.textContent = '';

    // Reset game variables
    currentIndex = 0;
    score = 0;
    scoreDisplay.textContent = `Score: ${score}`;
    timeLeft = 90;
    timerDisplay.textContent = timeLeft;
    gamePhase = 0;
    tappedOnce = false;

    // Show category selection screen
    showScreen(categorySelectionScreen);
}

exitButton.addEventListener('click', exitGame);

// --- Initial Setup ---
// Preload sounds (optional, but good for smoother play)
bgMusic.load();
timerEndSound.load();

// Show category selection on load
showScreen(categorySelectionScreen);

// Handle cases where audio might not auto-play until user interaction
document.addEventListener('DOMContentLoaded', () => {
    // Try playing a silent sound to unlock audio context, then pause.
    // This is a common workaround for browser auto-play policies.
    const silentAudio = new Audio();
    silentAudio.src = 'data:audio/mpeg;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2YzU4LjY5LjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAABuSUQzAwAAAAAAJGNvbW1lbnQAAAAAAENyZWF0ZWQgYnkgRkxBRyBNZXRhZGF0YSBUYWcgcmVhZGVyAAAAAAAAAA//tAwYAAAAHzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMZAAAAAAAAAAAAAAAoYXJuZXIgYXNpZ25zIHRoZWlyIHNlY3VyaXR5IGRhdGEgdG8gdGhlIGRhdGFiYXNlLjogc2VsZWN0IHNlY3VyaXR5X2lkLCBzZWN1cml0eV90eXBlLCBzZWN1cml0eV9hbW91bnQsIHNlY3VyaXR5X2RhdGUsIHNlY3VyaXR5X3ByaWNlIGZyb20gc2VjdXJpdGllcyB3aGVyZSBzZWN1cml0eV9pZCA9IDU7Cg==';
    silentAudio.play().then(() => {
        silentAudio.pause();
    }).catch(e => {
        console.warn("Silent audio play failed, likely browser policy:", e);
    });
});