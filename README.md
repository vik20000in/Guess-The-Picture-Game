# Guess the Picture Game

A fun and interactive web-based guessing game where players identify images from various categories within a time limit.

## Overview

Players select a category and compete against the clock to guess what's shown in pictures. The game features:
- Multiple image categories (Animals, Things, Bollywood Heroes, Indian Food, Sports & Games, Indian Monuments, and Fruits)
- Adjustable game duration (60, 90, or 120 seconds)
- Smooth animations and sound effects
- Mobile-friendly responsive design
- Background music that increases in intensity as time runs out

## Game Flow

1. **Category Selection**: Choose a category and set the game duration
2. **First Tap**: Tap to reveal the image
3. **Second Tap**: Tap again to reveal the answer
4. **Auto-Advance**: After 1.5 seconds of viewing the answer, the next image automatically appears
5. **Time's Up**: Game ends when the timer reaches zero

## Features

- **Image Preloading**: All category images are preloaded in the background for smooth gameplay
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Sound Effects**: Audio feedback for reveals and correct answers
- **Dynamic Music**: Background music adapts to game pace and remaining time
- **Local Storage**: Saves your preferred game duration selection

## Project Structure

```
Guess-The-Picture-Game/
├── index.html              # Main HTML file with game UI structure
├── script.js              # Game logic and JavaScript functionality
├── style.css              # Game styling and responsive design
├── categories.json        # Image data for all categories
├── images/                # Image assets organized by category
│   ├── animals/
│   ├── bollywood/
│   ├── food/
│   ├── fruits/
│   ├── icons/
│   ├── monuments/
│   ├── sports/
│   └── things/
├── sounds/                # Audio files for music and effects
└── README.md             # This file
```

## Files Description

### index.html
Main HTML structure including:
- Game container with three screens: category selection, game screen, and game over screen
- Audio elements for background music and sound effects
- Links to external resources (Google Fonts, CSS, JavaScript)

### script.js
Core game logic including:
- Game state management (phase tracking, timer, current item)
- Image preloading system for smooth gameplay
- Event handling for taps/clicks
- Audio playback with mobile compatibility
- Timer functionality with dynamic music intensity
- Screen transitions and game flow control

### style.css
Responsive styling with:
- Mobile-first design
- Smooth animations and transitions
- Category button styling with icons
- Game screen layout
- Timer and game over screen styling

### categories.json
Data structure containing:
- Category names and item lists
- Image file paths
- English names and Hindi translations
- Organized by category type

## How to Play

1. Open `index.html` in a web browser
2. Select a category from the available options
3. Choose your preferred game duration
4. Tap the screen to reveal the image
5. Tap again to reveal the answer
6. The next image will automatically appear after 1.5 seconds
7. Try to guess as many items as possible before time runs out!

## Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## Audio Files

The game includes:
- `background_music.wav` - Main background music that adapts to game intensity
- `reveal_picture.wav` - Sound effect when image is revealed
- `reveal_name.wav` - Sound effect when answer is revealed
- `correct.wav` - Sound effect for correct guess
- `timer_end.wav` - Sound when game time ends

## Technical Details

### Image Caching
Images are preloaded into memory using JavaScript's Image object for faster display during gameplay, reducing lag and improving user experience.

### Responsive Design
The game adapts to all screen sizes using CSS media queries and flexible layouts, ensuring optimal play on any device.

### Mobile Optimization
- Touch event handling for mobile devices
- Audio context unlocking for iOS compatibility
- Viewport configuration for app-like experience
- No zoom on input focus

## Customization

You can customize the game by modifying:

1. **Game Categories**: Edit `categories.json` to add/remove categories
2. **Images**: Replace image files in the `images/` directory
3. **Sounds**: Replace audio files in the `sounds/` directory
4. **Styling**: Modify `style.css` for custom appearance
5. **Game Duration Options**: Update the time buttons in `index.html`

## Local Development

To run locally:
1. Clone or download the project
2. Open `index.html` in a web browser
3. No build process or dependencies required - pure HTML, CSS, and JavaScript

## Performance Notes

- Image preloading happens asynchronously in the background
- Shuffle algorithm randomizes question order each game
- Music playback rate and volume adjust dynamically based on remaining time
- Optimized for minimal memory usage during gameplay

## License

See LICENSE file for details.

## Author

Created for educational entertainment purposes.
