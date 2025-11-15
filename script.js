// Load categories data from JSON file
let categoriesData = {};

// Fetch categories from JSON file
fetch('categories.json')
    .then(response => response.json())
    .then(data => {
        categoriesData = data;
        console.log('Categories loaded successfully:', Object.keys(categoriesData));
    })
    .catch(error => console.error('Error loading categories.json:', error));

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
let gameTime = parseInt(localStorage.getItem('gameTime')) || 90; // Load from localStorage, default to 90
let timeLeft = gameTime;
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
    timeLeft = gameTime; // Use the selected game time from localStorage
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
        instructionsText.textContent = 'Tap for next item!';
        gamePhase = 2;
        
        // Auto-advance to next item immediately instead of waiting
        if (autoAdvanceTimer) {
            clearTimeout(autoAdvanceTimer);
        }
        autoAdvanceTimer = setTimeout(() => {
            currentIndex++;
            loadNextItem();
        }, 800);
    }
}

function startTimer() {
    bgMusic.currentTime = 0; // Start music from beginning
    bgMusic.volume = 0.3;    // Initial volume
    bgMusic.playbackRate = 1.0; // Start at normal speed
    
    timerInterval = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;

        // Gradually increase music intensity over time
        if (timeLeft > 0) {
            // Increase volume gradually
            const volumeIncreaseFactor = 0.7 / gameTime; // Scale to selected game time
            bgMusic.volume = Math.min(0.8, 0.3 + ((gameTime - timeLeft) / gameTime) * 0.5);
            
            // Increase playback rate for more urgency (especially in last 30 seconds)
            if (timeLeft <= gameTime * 0.33) {
                // Last third: speed up significantly
                bgMusic.playbackRate = 1.0 + ((gameTime * 0.33 - timeLeft) / (gameTime * 0.33)) * 0.4;
            } else {
                // First two-thirds: slow speed increase
                bgMusic.playbackRate = 1.0 + ((gameTime - timeLeft) / gameTime) * 0.15;
            }
        }

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            bgMusic.playbackRate = 1.0; // Reset playback rate
            endGame();
        }
    }, 1000);
}

function playMusic() {
    // Set reasonable volume before playing
    bgMusic.volume = 0.3;
    
    // Ensure audio is unmuted (mobile sometimes mutes by default)
    bgMusic.muted = false;
    
    // Play with proper promise handling for mobile
    const playPromise = bgMusic.play();
    
    if (playPromise !== undefined) {
        playPromise
            .then(() => {
                console.log("Background music started successfully");
            })
            .catch(error => {
                console.warn("Autoplay failed, retrying:", error);
                // Retry after a short delay
                setTimeout(() => {
                    bgMusic.play().catch(e => console.error("Error playing background music:", e));
                }, 100);
            });
    }
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
    timeLeft = gameTime; // Reset to the selected game time
    timerDisplay.textContent = timeLeft;
    gamePhase = 0;
    tappedOnce = false;

    // Show category selection screen
    showScreen(categorySelectionScreen);
}

// --- Initial Setup ---
// Setup time selection buttons
const timeButtons = document.querySelectorAll('.time-btn');
timeButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent tap event from triggering game
        const selectedTime = parseInt(button.getAttribute('data-time'));
        gameTime = selectedTime;
        timeLeft = selectedTime; // Update timeLeft as well
        localStorage.setItem('gameTime', selectedTime); // Save to localStorage
        
        // Update UI: remove active class from all buttons
        timeButtons.forEach(btn => btn.classList.remove('active'));
        // Add active class to clicked button
        button.classList.add('active');
        
        console.log(`Game time set to ${selectedTime} seconds`);
    });
});

// Preload sounds (optional, but good for smoother play)
bgMusic.load();
revealPictureSound.load();
revealNameSound.load();
correctSound.load();
timerEndSound.load();

// Ensure audio is not muted and set initial volume
bgMusic.muted = false;
bgMusic.volume = 0.3;

// Preload all category images when page loads
Object.keys(categoriesData).forEach(categoryName => {
    preloadCategoryImages(categoryName);
});

// Show category selection on load
showScreen(categorySelectionScreen);

// Additional fallback: unlock audio on any user interaction
let audioUnlocked = false;
function unlockAudio() {
    if (!audioUnlocked) {
        const playPromise = bgMusic.play();
        if (playPromise !== undefined) {
            playPromise
                .then(() => {
                    bgMusic.pause();
                    bgMusic.currentTime = 0;
                    audioUnlocked = true;
                    console.log("Audio context unlocked successfully");
                })
                .catch(e => console.warn("Audio unlock attempt failed:", e));
        }
    }
}

// Unlock audio on first interaction
document.addEventListener('click', unlockAudio, { once: true });
document.addEventListener('touchstart', unlockAudio, { once: true });

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