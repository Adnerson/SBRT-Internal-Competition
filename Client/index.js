document.addEventListener('DOMContentLoaded', async (event) => {
    const joystick = document.getElementsByClassName('joystick')[0];
    const stick = document.getElementsByClassName('stick')[0];
    let radius = 75;
    let position = { x: 0, y: 0 }; // Position of the stick relative to center
    let servo = 0;
    let activeKeys = new Set(); // Track pressed keys

    // Initialize WebSocket connection
    let socket = new WebSocket("ws://192.168.1.73:80/direction");
    socket.addEventListener("open", () => {
        socket.send("Hello Server!");
    });

    // Function to reset the stick position to the center
    const resetStickPosition = () => {
        position = { x: 0, y: 0 };
        stick.style.top = '75px';
        stick.style.left = '75px';
    };

    // Function to move the stick based on position coordinates
    const moveStick = (x, y) => {
        stick.style.top = `${y + radius}px`;
        stick.style.left = `${x + radius}px`;

        console.log("x: " + x + ", y:" + y);

        // Send coordinates via WebSocket
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ x, y, servo }));
        }
    };

    // Function to handle arrow key movement with diagonal support
    const handleArrowKeyMovement = () => {
        const moveAmount = 5;
        let dx = 0, dy = 0;

        // Check active keys for movement direction
        if (activeKeys.has('ArrowUp')) dy -= moveAmount;
        if (activeKeys.has('ArrowDown')) dy += moveAmount;
        if (activeKeys.has('ArrowLeft')) dx -= moveAmount;
        if (activeKeys.has('ArrowRight')) dx += moveAmount;

        // Update position within constraints
        position.x = Math.max(-radius, Math.min(position.x + dx, radius));
        position.y = Math.max(-radius, Math.min(position.y + dy, radius));

        // Immediately move the stick without waiting for requestAnimationFrame
        moveStick(position.x, position.y);
    };

    // Main loop to constantly update position based on active keys
    const gameLoop = () => {
        handleArrowKeyMovement();
        requestAnimationFrame(gameLoop); // Keep the loop running
    };

    // Start the game loop
    requestAnimationFrame(gameLoop);

    // Listen for keydown events to add keys to the set
    document.addEventListener('keydown', (e) => {
        if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
            activeKeys.add(e.key);
        }

        //Send "OK" signal if the spacebar is pressed
        if (e.key === 'q') {
            servo = 1;
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ x, y, servo }));
            }
        }
        if (e.key == 'w') {
            servo = 0;
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ x, y, servo }));
            }
        }
    });

    // Listen for keyup events to remove keys from the set
    document.addEventListener('keyup', (e) => {
        if (activeKeys.has(e.key)) {
            activeKeys.delete(e.key);

            // If no keys are pressed, reset the joystick to center
            if (activeKeys.size === 0) {
                resetStickPosition();
            }
        }
    });
});
