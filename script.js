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
        { "image": "images/animals/fox.png", "name": "Fox" },
  { "image": "images/animals/rabbit.png", "name": "Rabbit" },
  { "image": "images/animals/whale.png", "name": "Whale" },
  { "image": "images/animals/dolphin.png", "name": "Dolphin" },
  { "image": "images/animals/horse.png", "name": "Horse" },
  { "image": "images/animals/parrot.png", "name": "Parrot" },
  { "image": "images/animals/owl.png", "name": "Owl" },
  { "image": "images/animals/frog.png", "name": "Frog" },
  { "image": "images/animals/tortoise.png", "name": "Tortoise" },
  { "image": "images/animals/kangaroo.png", "name": "Kangaroo" },
  { "image": "images/animals/hippopotamus.png", "name": "Hippopotamus" },
  { "image": "images/animals/crocodile.jpg", "name": "Crocodile" },
  { "image": "images/animals/shark.jpg", "name": "Shark" },
  { "image": "images/animals/squirrel.jpg", "name": "Squirrel" },
  { "image": "images/animals/sheep.jpg", "name": "Sheep" },
  { "image": "images/animals/goat.jpg", "name": "Goat" },
  { "image": "images/animals/camel.jpg", "name": "Camel" },
  { "image": "images/animals/eagle.jpg", "name": "Eagle" },
  { "image": "images/animals/bat.jpg", "name": "Bat" },
  { "image": "images/animals/panda.jpg", "name": "Panda" },
  { "image": "images/animals/wolf.jpg", "name": "Wolf" },
  { "image": "images/animals/otter.jpg", "name": "Otter" },
  { "image": "images/animals/raccoon.jpg", "name": "Raccoon" },
  { "image": "images/animals/bison.jpg", "name": "Bison" },
  { "image": "images/animals/koala.jpg", "name": "Koala" },
  { "image": "images/animals/lemur.jpg", "name": "Lemur" },
  { "image": "images/animals/porcupine.jpg", "name": "Porcupine" },
 
  { "image": "images/animals/woodpecker.jpg", "name": "Woodpecker" },
   { "image": "images/animals/orangutan.jpg", "name": "Orangutan" },
  { "image": "images/animals/chimpanzee.jpg", "name": "Chimpanzee" },
  
  { "image": "images/animals/donkey.jpg", "name": "Donkey" },
  { "image": "images/animals/buffalo.jpg", "name": "Buffalo" },
  { "image": "images/animals/jaguar.jpg", "name": "Jaguar" }
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
const loadingIndicator = document.getElementById('loading-indicator');

const categoryButtons = document.querySelectorAll('.category-btn');
const gameImage = document.getElementById('game-image');
const itemNameDisplay = document.getElementById('item-name');
const instructionsText = document.getElementById('instructions');
const timerDisplay = document.getElementById('timer');
const playAgainButton = document.getElementById('play-again-btn');
const exitButton = document.getElementById('exit-button');

const bgMusic = document.getElementById('bg-music');
const revealPictureSound = document.getElementById('reveal-picture-sound');
const revealNameSound = document.getElementById('reveal-name-sound');
const correctSound = document.getElementById('correct-sound');
const timerEndSound = document.getElementById('timer-end-sound');

// --- Game State Variables ---
let currentCategory = [];
let currentIndex = 0;
let timeLeft = 90;
let timerInterval;
let gamePhase = 0; // 0: initial (tap for picture), 1: picture shown (tap for name), 2: name shown (ready for next)
let tappedOnce = false; // To ensure only one tap per phase transition
let autoAdvanceTimer; // Timer for auto-advancing to next item
let imageCache = {}; // Cache for preloaded images
let isPreloading = false; // Flag to track if images are being preloaded

// --- Functions ---

function playSound(audioElement) {
    if (audioElement) {
        audioElement.currentTime = 0; // Reset to start
        audioElement.play().catch(e => console.warn("Sound play failed:", e));
    }
}

function preloadCategoryImages(categoryName) {
    // Preload all images for a category in the background
    const category = categoriesData[categoryName];
    
    if (!imageCache[categoryName]) {
        imageCache[categoryName] = {};
    }
    
    // Preload images asynchronously
    category.forEach((item) => {
        if (!imageCache[categoryName][item.image]) {
            const img = new Image();
            img.src = item.image;
            // Store the image in cache once it's loaded
            img.onload = () => {
                imageCache[categoryName][item.image] = img;
            };
            img.onerror = () => {
                console.warn(`Failed to preload image: ${item.image}`);
            };
        }
    });
}

function getPreloadedImage(categoryName, imagePath) {
    // Get a preloaded image from cache or return null if not yet loaded
    if (imageCache[categoryName] && imageCache[categoryName][imagePath]) {
        return imageCache[categoryName][imagePath];
    }
    return null;
}

function showScreen(screenToShow) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    screenToShow.classList.add('active');
}

function startGame(categoryName) {
    // Start preloading images immediately in background
    preloadCategoryImages(categoryName);
    
    // Show loading indicator briefly
    loadingIndicator.classList.remove('hidden');
    
    currentCategory = [...categoriesData[categoryName]]; // Copy to allow shuffling
    shuffleArray(currentCategory);
    currentIndex = 0;
    timeLeft = 90;
    gamePhase = 0;
    tappedOnce = false;

    timerDisplay.textContent = timeLeft;
    
    // Ensure image is completely hidden before starting
    gameImage.style.opacity = 0;
    gameImage.src = '';
    
    // Ensure name is hidden immediately (use display:none via .hidden) to avoid any brief flash
    itemNameDisplay.classList.add('hidden');
    itemNameDisplay.style.opacity = 0;
    itemNameDisplay.textContent = '';
    instructionsText.textContent = 'Tap to reveal picture!';

    showScreen(gameScreen);
    
    // Hide loading indicator after a brief delay
    setTimeout(() => {
        loadingIndicator.classList.add('hidden');
    }, 800);
    
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
    
    // Hide the image immediately without animation
    gameImage.style.opacity = 0;
    gameImage.style.display = 'none';
    
    const item = currentCategory[currentIndex];
    
    // Get the current category name from the shuffled array
    const categoryName = Object.keys(categoriesData).find(cat => 
        categoriesData[cat].some(i => i.image === item.image)
    );
    
    // Try to use preloaded image, otherwise set src to load it
    const preloadedImg = getPreloadedImage(categoryName, item.image);
    if (preloadedImg) {
        gameImage.src = preloadedImg.src;
    } else {
        gameImage.src = item.image;
    }
    
    // Set the name while it's hidden so it never appears briefly on load
    itemNameDisplay.classList.add('hidden');
    itemNameDisplay.style.opacity = 0;
    itemNameDisplay.textContent = item.name;

    // Reset for new item display
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
        gameImage.style.display = 'block';
        gameImage.style.opacity = 1;
        playSound(revealPictureSound); // Play picture reveal sound
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
        playSound(correctSound); // Play correct/point sound
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
    
    // Add touch event support for better mobile responsiveness
    button.addEventListener('touchstart', (event) => {
        event.preventDefault(); // Prevent default touch behavior
        const category = button.dataset.category;
        startGame(category);
    }, { passive: false });
});

// Use event delegation for the game screen tap to handle picture/name reveal
gameScreen.addEventListener('click', (event) => {
    // Don't process tap if clicking on buttons
    if (event.target.closest('button')) return;
    handleTap();
});

// Add touch event support for better mobile responsiveness
gameScreen.addEventListener('touchstart', (event) => {
    // Don't process tap if clicking on buttons
    if (event.target.closest('button')) return;
    event.preventDefault(); // Prevent default touch behavior (zoom, scroll, etc.)
    handleTap();
}, { passive: false });

playAgainButton.addEventListener('click', () => {
    showScreen(categorySelectionScreen);
});

// Exit button - support both click and touch
exitButton.addEventListener('click', exitGame);
exitButton.addEventListener('touchstart', (event) => {
    event.preventDefault();
    event.stopPropagation();
    exitGame();
}, { passive: false });
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
    timeLeft = 90;
    timerDisplay.textContent = timeLeft;
    gamePhase = 0;
    tappedOnce = false;

    // Show category selection screen
    showScreen(categorySelectionScreen);
}

// --- Initial Setup ---
// Preload sounds (optional, but good for smoother play)
bgMusic.load();
revealPictureSound.load();
revealNameSound.load();
correctSound.load();
timerEndSound.load();

// Preload all category images when page loads
Object.keys(categoriesData).forEach(categoryName => {
    preloadCategoryImages(categoryName);
});

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