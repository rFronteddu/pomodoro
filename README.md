# pomodoro
This is a simple python app designed to support the pomodoro workflow.

* Choose a single task you will focus on.
* Set the timer to 25 minutes.
* Work on the task until the timer rings.
* Take a short 5 minute break.
* Work for another 25 minutes.
* After 4 work periods of 25 minutes, take a longer 20-30 minute break.

# Intalling
<code>
pyinstaller  --windowed --add-data "./pomodoro/tomato.png;." --add-data "./pomodoro/gong.wav;." main.py -n pomodoro
</code>

# Run
Start the pomodoro executable in dist\pomodoro after following the installing procedure or run the init script manually.