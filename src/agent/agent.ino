#include <Servo.h>
#include <Timeout.h>
#include <Stepper.h>

#define KNIFE_L_PIN 18
#define KNIFE_R_PIN 19
#define COUNTDOWN_PIN 27
#define IN1 26
#define IN2 25
#define IN3 33
#define IN4 32
#define SWITCH_PIN 15

#define TOUCH_CUTOFF 46

class Knife {
public:
  Knife(int pin, int retractedDuration, int extendedDuration, int startAngle, int endAngle) : retractedDuration(retractedDuration), extendedDuration(extendedDuration), startAngle(startAngle), endAngle(endAngle) {
    servo.attach(pin);
    servo.write(startAngle); 
    timer.start(retractedDuration);
  }

  void update() {
    if (timer.time_over()) {
      if (extended) {
        timer.start(retractedDuration);
        extended = false;
        servo.write(startAngle); 
      } else {
        timer.start(extendedDuration);
        extended = true;
        servo.write(endAngle); 
      }
    }
  }

private:
    Servo servo;
    Timeout timer;
    bool extended = false;
    int retractedDuration;
    int extendedDuration;
    int startAngle;
    int endAngle;
};

class Countdown {
public: 
  Countdown(int pin, int totalTime) : totalTime(totalTime) {
    servo.attach(pin);
    initialize();
    moveIncrement = (int) (totalTime / 180);
  }

  void initialize() {
    finished = false;
    position = 180;
    servo.write(position); 
  }

  void update() {
    if (timer.periodic(moveIncrement)) {
      servo.write(position--);

      if (position <= endPosition) {
        timer.pause();
        timer.expire();
        finished = true;
      }
    }
  }

  bool isFinished() {
    return finished;
  }

  private:
    Servo servo;
    Timeout timer;
    int totalTime;
    int moveIncrement;
    int position = 180;
    const int endPosition = 0;
    bool finished = false;
};

class FingerSwitch {
public:
  FingerSwitch(int touchPin, int touchDuration): touchPin(touchPin), touchDuration(touchDuration) {
    pinMode(touchPin, INPUT_PULLUP);
    timer.start(touchDuration);
    timer.pause();
  }

  bool switchInitiated() {
    if (touchRead(touchPin) < TOUCH_CUTOFF && !prevSwitchStatus) {
      prevSwitchStatus = true;
      return true;
    }
    return false;
  }
  
  bool switchReleased() {
    if (prevSwitchStatus) {
      prevSwitchStatus = false;
      return true;
    }
    return false;
  }

  bool switchHeld() {
    int switchStatus = touchRead(touchPin);
    if (switchInitiated()) {
      timer.start(touchDuration);
      prevSwitchStatus = true;
    }
    if (switchStatus >= TOUCH_CUTOFF && prevSwitchStatus) {
      timer.pause();
      prevSwitchStatus = false;
    }
    if (timer.time_over()) {
      timer.start(touchDuration);
      timer.pause();
      return true;
    }
    return false;
  }

private:
  int touchDuration;
  Timeout timer;
  int touchPin;
  bool prevSwitchStatus = false;
};



Knife lKnife(KNIFE_L_PIN, 3000, 200, 180, 130);
Knife rKnife(KNIFE_R_PIN, 5000, 200, 65, 115);
// FingerSwitch fingerSwitch(SWITCH_PIN, 3000);
// Countdown countdown(COUNTDOWN_PIN, 300000);
// Stepper myStepper(2048, IN1, IN3, IN2, IN4);

int score = 50;
bool gameEnd = true;

// void initializeGame() {
//   score = 0;
//   gameEnd = false;
//   countdown.initialize();
//   Serial.println("START");
// }

void setup() {
  Serial.begin(9600);
}

void loop() {
  lKnife.update();
  rKnife.update();
  
  // if (Serial.available() > 0) {
  //   String incomingData = Serial.readStringUntil('\n');
  //   Serial.println(incomingData);
  //   score = incomingData.toInt();
  // }
}
 
